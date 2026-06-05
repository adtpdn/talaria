#!/usr/bin/env python3
"""
check_task.py — Spawn Hermes to verify (and optionally execute) a Talaria task
against its target project.

Usage:
    python3 scripts/check_task.py --task-id <id> --project-id <id>
        [--auto] [--profile <name>] [--model <id>] [--apply-status <s>]

Outputs (stdout):
    - progress lines (streamed, picked up by server.py SSE)
    - a final block:
          __RESULT__
          {"implemented": true|false|null, "summary": "...", "suggested_status": "done|progress|todo"}

Modes:
    default       Verify implementation only. Do not modify files.
    --auto        If not implemented: move task to 'progress', then spawn
                  Hermes again with a "do the work" prompt, then move to 'done'
                  on success. Already-implemented tasks skip the work run.
    --apply-status Move the task to the given status and exit (no Hermes run).

Config is read from data/agent_config.json for profile/model selection
(category_profile_map + default_profile + model). CLI flags override config.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────────
_HERE     = Path(__file__).resolve().parent
_BASE     = _HERE.parent
DATA_DIR  = _BASE / 'data'
TASKS_FILE  = DATA_DIR / 'tasks.json'
PROJ_FILE   = DATA_DIR / 'projects.json'
CONFIG_FILE = DATA_DIR / 'agent_config.json'

# ── helpers ───────────────────────────────────────────────────────────────────

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def find_task(task_id):
    """Find a task by id in tasks.json (id may be int or str)."""
    tasks = load_json(TASKS_FILE, [])
    for t in tasks:
        if str(t.get('id')) == str(task_id):
            return t
    return None


def find_project(project_id):
    projects = load_json(PROJ_FILE, [])
    for p in projects:
        if p.get('id') == project_id:
            return p
    return None


def update_task_status(task_id, new_status, halt_reason=None):
    """Set the status (and optionally halt_reason) on a task in tasks.json."""
    tasks = load_json(TASKS_FILE, [])
    for t in tasks:
        if str(t.get('id')) == str(task_id):
            t['status'] = new_status
            if halt_reason is not None:
                t['halt_reason'] = halt_reason
            break
    else:
        # task not found; add a stub so the change is visible
        tasks.append({
            'id': int(task_id) if str(task_id).isdigit() else task_id,
            'status': new_status,
            'halt_reason': halt_reason,
        })
    save_json(TASKS_FILE, tasks)


def load_agent_config():
    return load_json(CONFIG_FILE, {
        'default_profile': 'default',
        'category_profile_map': {},
        'model': 'kr/auto',
        'provider': 'custom',
    })


def pick_profile(task, cfg, override=None):
    if override:
        return override
    cat = (task.get('category') or '').upper()
    cmap = cfg.get('category_profile_map') or {}
    if cat in cmap:
        return cmap[cat]
    return cfg.get('default_profile') or 'default'


def pick_model(cfg, override=None):
    if override:
        return override
    return cfg.get('model') or 'kr/auto'


def log(msg):
    """Print a single SSE-style progress line and flush."""
    print(msg, flush=True)


def run_hermes(prompt, profile, model, cwd, worktree=False):
    """
    Run `hermes -z <prompt> --yolo --profile <p> -m <m>` in cwd.
    Stream stdout line-by-line. Returns (returncode, full_output, result_json).
    """
    cmd = ['hermes', '-z', prompt, '--yolo', '--profile', profile, '-m', model]
    if worktree:
        cmd.append('--worktree')

    log(f'[check_task] $ cd {cwd} && hermes -z <prompt> --yolo --profile {profile} -m {model}')
    log(f'[check_task] [profile={profile}] [model={model}]')

    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, cwd=str(cwd)
        )
    except FileNotFoundError:
        log('[check_task] ERROR: hermes CLI not found in PATH')
        return 127, '', None
    except Exception as e:
        log(f'[check_task] ERROR: failed to spawn hermes: {e}')
        return 1, '', None

    full = []
    capture_next = False
    result_json = None

    try:
        for line in proc.stdout:
            line = line.rstrip('\n')
            full.append(line)
            # forward everything except the result marker as progress
            if line == '__RESULT__':
                capture_next = True
                continue
            if capture_next:
                try:
                    result_json = json.loads(line)
                except Exception:
                    pass
                capture_next = False
                continue
            log(line)
    except Exception as e:
        log(f'[check_task] [stream error] {e}')

    rc = proc.wait()
    return rc, '\n'.join(full), result_json


# ── prompt builders ───────────────────────────────────────────────────────────

CHECK_PROMPT = """\
You are verifying whether a Talaria task is already implemented in a project.

PROJECT: {project_name}  ({project_path})
TASK ID: {task_id}
TITLE: {title}
CATEGORY: {category}
PRIORITY: {priority}

DESCRIPTION:
{description}

FULL CONTENT (markdown, includes acceptance criteria + migration checklist):
{content}

YOUR JOB
=======
1. cd into the project at {project_path}
2. Use read_file / search_files / terminal to inspect the codebase.
3. Determine whether each acceptance criterion in CONTENT is already met.
4. Cross-check the migration checklist items.
5. Decide: implemented | partially | not_implemented

OUTPUT FORMAT (mandatory)
=========================
At the very end of your response, emit EXACTLY this block (no other text after):

__RESULT__
{{"implemented": <true|false|null>, "summary": "<2-3 sentence verdict>", "suggested_status": "<done|progress|todo>", "evidence": ["<file:line or fact>", "..."]}}

Rules:
- `implemented: true`  → all acceptance criteria met → suggested_status "done"
- `implemented: false` → none or barely any criteria met → suggested_status "todo" (will be implemented)
- `implemented: null`  → partial / in progress / unclear → suggested_status "progress"
- `summary` is short and concrete (no fluff).
- `evidence` lists the specific files/lines you inspected.
- Do NOT modify any files. Read-only inspection.
"""


DO_PROMPT = """\
You are implementing a Talaria task inside an existing project.

PROJECT: {project_name}  ({project_path})
TASK ID: {task_id}
TITLE: {title}
CATEGORY: {category}

DESCRIPTION:
{description}

FULL CONTENT (markdown — follow the "Solution" section + acceptance criteria):
{content}

YOUR JOB
=======
1. cd into {project_path}
2. Implement the task per the Solution section and Migration Checklist.
3. Match the existing code style (GDScript conventions, project layout).
4. Verify each acceptance criterion as you go.
5. Run any obvious sanity checks (syntax, project loads).
6. Report what you did.

OUTPUT FORMAT (mandatory)
=========================
At the very end of your response, emit EXACTLY this block (no other text after):

__RESULT__
{{"implemented": <true|false>, "summary": "<what you did + final state>", "suggested_status": "<done|progress|halt>", "evidence": ["<file created/modified>", "..."], "halt_reason": "<only if suggested_status=halt>"}}

Rules:
- `suggested_status: "done"` when the task is complete and verified.
- `suggested_status: "progress"` when partial work was done but more is needed.
- `suggested_status: "halt"` only if blocked (missing dependency, conflicting design, etc.) — explain in halt_reason.
- You MAY edit/create files. You may NOT push, commit, or open PRs.
"""


# ── main flow ─────────────────────────────────────────────────────────────────

def check_only(task, project, profile, model):
    prompt = CHECK_PROMPT.format(
        project_name=project.get('name', project.get('id', '')),
        project_path=project.get('path', ''),
        task_id=task.get('id', ''),
        title=task.get('title', ''),
        category=task.get('category', ''),
        priority=task.get('priority', ''),
        description=task.get('description', ''),
        content=(task.get('content') or '')[:8000],
    )

    project_path = project.get('path', '')
    if not project_path or not Path(project_path).exists():
        log(f'[check_task] ERROR: project path missing: {project_path!r}')
        return {
            'implemented': None,
            'summary': f'Project path not accessible: {project_path}',
            'suggested_status': 'halt',
            'evidence': [],
            'halt_reason': 'project_path_unreachable',
        }

    rc, _out, result = run_hermes(prompt, profile, model, cwd=project_path)

    if result is None:
        log(f'[check_task] hermes exited rc={rc} without __RESULT__ block')
        return {
            'implemented': None,
            'summary': f'Hermes exited (rc={rc}) without producing a structured result.',
            'suggested_status': 'progress',
            'evidence': [],
        }

    # fill in sensible defaults
    result.setdefault('implemented', None)
    result.setdefault('summary', '')
    result.setdefault('suggested_status',
                      'done' if result['implemented'] is True
                      else 'todo' if result['implemented'] is False
                      else 'progress')
    result.setdefault('evidence', [])
    return result


def do_work(task, project, profile, model):
    prompt = DO_PROMPT.format(
        project_name=project.get('name', project.get('id', '')),
        project_path=project.get('path', ''),
        task_id=task.get('id', ''),
        title=task.get('title', ''),
        category=task.get('category', ''),
        description=task.get('description', ''),
        content=(task.get('content') or '')[:8000],
    )

    project_path = project.get('path', '')
    if not project_path or not Path(project_path).exists():
        log(f'[check_task] ERROR: project path missing: {project_path!r}')
        return {
            'implemented': False,
            'summary': f'Project path not accessible: {project_path}',
            'suggested_status': 'halt',
            'evidence': [],
            'halt_reason': 'project_path_unreachable',
        }

    rc, _out, result = run_hermes(prompt, profile, model, cwd=project_path)
    if result is None:
        return {
            'implemented': False,
            'summary': f'Hermes exited (rc={rc}) without producing a structured result.',
            'suggested_status': 'progress',
            'evidence': [],
        }
    result.setdefault('implemented', False)
    result.setdefault('summary', '')
    result.setdefault('suggested_status', 'progress')
    result.setdefault('evidence', [])
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--task-id',        required=True)
    p.add_argument('--project-id',     required=True)
    p.add_argument('--auto',           action='store_true',
                   help='If not implemented, also do the work + flip status.')
    p.add_argument('--profile',        default=None)
    p.add_argument('--model',          default=None)
    p.add_argument('--apply-status',   default=None,
                   help='Skip Hermes; just set tasks.json status and exit.')
    p.add_argument('--halt-reason',    default=None)
    p.add_argument('--worktree',       action='store_true')
    args = p.parse_args()

    log(f'[check_task] task={args.task_id} project={args.project_id} '
        f'auto={args.auto} apply={args.apply_status}')

    # ── pure status-apply path (no Hermes) ────────────────────────────────
    if args.apply_status:
        if args.apply_status not in ('done', 'progress', 'todo', 'halt'):
            log(f'[check_task] ERROR: invalid --apply-status {args.apply_status!r}')
            sys.exit(2)
        update_task_status(args.task_id, args.apply_status, args.halt_reason)
        result = {
            'applied_status': args.apply_status,
            'changed': True,
        }
        print('__RESULT__')
        print(json.dumps(result))
        return

    # ── load task + project + config ─────────────────────────────────────
    task = find_task(args.task_id)
    if not task:
        log(f'[check_task] ERROR: task {args.task_id} not found in tasks.json')
        print('__RESULT__')
        print(json.dumps({
            'implemented': None,
            'summary': f'Task {args.task_id} not found',
            'suggested_status': 'halt',
            'evidence': [],
            'halt_reason': 'task_not_found',
        }))
        sys.exit(1)

    project = find_project(args.project_id)
    if not project:
        log(f'[check_task] ERROR: project {args.project_id} not found')
        print('__RESULT__')
        print(json.dumps({
            'implemented': None,
            'summary': f'Project {args.project_id} not found',
            'suggested_status': 'halt',
            'evidence': [],
            'halt_reason': 'project_not_found',
        }))
        sys.exit(1)

    cfg = load_agent_config()
    profile = pick_profile(task, cfg, args.profile)
    model   = pick_model(cfg, args.model)
    log(f'[check_task] task.category={task.get("category")!r} → profile={profile}, model={model}')

    # ── phase 1: check ───────────────────────────────────────────────────
    log('[check_task] ── phase 1: check implementation ──')
    check_result = check_only(task, project, profile, model)
    log(f'[check_task] check verdict: implemented={check_result.get("implemented")} '
        f'suggested={check_result.get("suggested_status")}')

    # ── auto mode: do the work if not already implemented ─────────────────
    if args.auto and check_result.get('implemented') is not True:
        log('[check_task] not implemented → flipping to progress and running do-work')
        update_task_status(args.task_id, 'progress', None)

        log('[check_task] ── phase 2: do the work ──')
        work_result = do_work(task, project, profile, model)
        log(f'[check_task] work verdict: implemented={work_result.get("implemented")} '
            f'suggested={work_result.get("suggested_status")}')

        # apply final status
        final_status = work_result.get('suggested_status') or 'progress'
        halt_reason  = work_result.get('halt_reason') if final_status == 'halt' else None
        # map 'halt' back to a real kanban status: keep as 'halt' if supported
        if final_status == 'halt':
            update_task_status(args.task_id, 'halt', halt_reason)
        elif final_status == 'done' and work_result.get('implemented') is True:
            update_task_status(args.task_id, 'done', None)
        else:
            update_task_status(args.task_id, 'progress', None)

        # merge evidence, keep check summary + work summary
        merged = dict(work_result)
        merged['check_summary']  = check_result.get('summary', '')
        merged['phase']          = 'auto'
        result = merged
    else:
        # pure check: optionally reflect status onto the task
        result = dict(check_result)
        result['phase'] = 'check'

    # ── emit final result ────────────────────────────────────────────────
    print('__RESULT__')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
