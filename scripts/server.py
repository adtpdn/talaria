#!/usr/bin/env python3
"""
API backend for Talaria
Endpoints:
  GET  /api/tasks                    — tasks.json
  GET  /api/projects                 — projects.json
  POST /api/projects                 — add/update a project
  GET  /api/tasks/:id/check/last     — latest check log for a task
  POST /api/tasks/:id/check          — run check_task.py (streaming SSE)
  POST /api/tasks/:id/check/apply    — apply suggested status after check
  GET  /api/agents                   — agent_state.json merged with task data
  GET  /api/agents/:id/log           — last 200 lines of task log
  POST /api/agents/:id/assign        — reassign task to a different profile
  POST /api/agents/:id/trigger       — fire cron job now (hermes cron run)
  POST /api/agents/sync              — run agent_sync.py --once
  GET  /api/report/preview           — HTML preview
  POST /api/report/send              — send report to Teams
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import html
import json
import subprocess
import tempfile
import time
import os
import re
from datetime import datetime
from pathlib import Path
import http.server

# Resolve paths relative to this script so it works both locally and in Docker
_HERE = Path(__file__).parent.resolve()
_BASE = _HERE.parent

HTML_DIR = _BASE / "html"

# ── Configuration ──────────────────────────────────────────────────────────────
CONFIG_FILE = _BASE / "config.json"

def load_config():
    defaults = {
        "hermes": {
            "mode": os.getenv("HERMES_MODE", "remote"),
            "remote_url": os.getenv("HERMES_REMOTE_URL", "http://localhost:8642"),
            "terminal_url": "http://localhost:8643"
        },
        "paths": {
            "data_dir": "./data",
            "tasks_dir": "./tasks",
            "scripts_dir": "./scripts"
        },
        "api": {
            "host": "0.0.0.0",
            "port": 8080
        }
    }
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            for key in defaults:
                if key not in config:
                    config[key] = defaults[key]
            # Override with env vars
            config["hermes"]["mode"] = os.getenv("HERMES_MODE", config["hermes"].get("mode", "remote"))
            config["hermes"]["remote_url"] = os.getenv("HERMES_REMOTE_URL", config["hermes"].get("remote_url", "http://localhost:8642"))
            return config
    return defaults

CONFIG = load_config()

import threading
TERMINAL_SESSIONS = {}
TERMINAL_LOCK = threading.Lock()

TASKS_FILE    = str(_BASE / CONFIG["paths"]["data_dir"] / 'tasks.json')
PROJ_FILE     = _BASE / CONFIG["paths"]["data_dir"] / 'projects.json'
STATE_FILE    = str(_BASE / CONFIG["paths"]["data_dir"] / 'agent_state.json')
AGENT_CONFIG  = str(_BASE / CONFIG["paths"]["data_dir"] / 'agent_config.json')
LOGS_DIR      = _BASE / CONFIG["paths"]["data_dir"] / 'agent_logs'
CHECK_LOGS    = _BASE / CONFIG["paths"]["data_dir"] / 'check_logs'
REPORT_SCRIPT = str(_HERE / 'report_to_teams.sh')
SYNC_SCRIPT   = str(_HERE / 'agent_sync.py')
CHECK_SCRIPT  = str(_HERE / 'check_task.py')
TASKS_DIR     = _BASE / CONFIG["paths"]["tasks_dir"]

# ── helpers ───────────────────────────────────────────────────────────────────

def _load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def _task_log_tail(task_id, lines=200):
    log_file = LOGS_DIR / f"task-{task_id}.log"
    if not log_file.exists():
        return []
    with open(log_file) as f:
        return f.readlines()[-lines:]

def _run(cmd, timeout=15):
    r = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=timeout)
    return r.stdout.strip(), r.returncode

def _update_task_md_field(task_file, key, value):
    md_path = TASKS_DIR / task_file
    if not md_path.exists():
        return False
    text = md_path.read_text()
    if not text.startswith('---'):
        return False
    parts = text.split('---', 2)
    if len(parts) < 3:
        return False
    fm, body = parts[1], parts[2]
    pattern = rf'^{re.escape(key)}:.*$'
    new_fm, n = re.subn(pattern, f'{key}: "{value}"', fm, flags=re.MULTILINE)
    if n == 0:
        new_fm = fm.rstrip() + f'\n{key}: "{value}"\n'
    md_path.write_text(f'---{new_fm}---{body}')
    return True


# ── handler ───────────────────────────────────────────────────────────────────

class TalariaAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HTML_DIR), **kwargs)

    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length else {}

    # ── routing ───────────────────────────────────────────────────────────────

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        p = self.path.split('?')[0]
        if re.match(r'^/task/\d+$', p):
            # Permalink: serve index.html for SPA routing
            self._set_headers(200, 'text/html')
            self.wfile.write(HTML_DIR.joinpath('index.html').read_bytes())
        elif p == '/api/tasks':
            self._json(_load_json(TASKS_FILE, []))
        elif p == '/api/projects':
            self._projects_list()
        elif re.match(r'^/api/tasks/[^/]+/md$', p):
            task_id = p.split('/')[3]
            self._task_md(task_id)
        elif re.match(r'^/api/tasks/[^/]+/check/last$', p):
            task_id = p.split('/')[3]
            self._check_last(task_id)
        elif p == '/api/agents':
            self._agents_list()
        elif p == '/api/agents/config':
            self._agents_config_get()
        elif p == '/api/agents/status':
            self._agents_status()
        elif p == '/api/agents/profiles':
            self._agents_profiles()
        elif p == '/api/agents/hermes-status':
            self._agents_hermes_status()
        elif p == '/api/agents/hermes-local-config':
            self._agents_hermes_local_config()
        elif p == '/api/agents/models':
            if self.command == "POST": self._agents_models_impl(self._read_body())
            else: self._agents_models()
        elif p == '/api/agents/sessions':
            self._agents_sessions()
        elif re.match(r'^/api/agents/sessions/[^/]+/messages$', p):
            session_id = p.split('/')[4]
            self._agents_session_messages(session_id)
        elif re.match(r'^/api/agents/[^/]+/log$', p):
            task_id = p.split('/')[3]
            self._agent_log(task_id)
        elif p == '/api/report/preview':
            self._preview_report()
        elif p == '/api/agents/terminal/profiles':
            self._terminal_profiles()
        elif p == '/api/agents/terminal/models':
            self._terminal_models()
        elif p == '/api/agents/terminal/config':
            self._terminal_config_get()
        elif re.match(r'^/api/agents/terminal/[^/]+/status$', p):
            tid = p.split('/')[4]
            self._terminal_status(tid)
        else:
            if p.startswith('/api/'):
                self._json({'error': 'Not found'}, 404)
            else:
                super().do_GET()

    def do_POST(self):
        p = self.path.split('?')[0]
        if p == '/api/projects':
            self._projects_save()
        elif p == '/api/tasks/regenerate':
            self._regenerate_tasks()
        elif re.match(r'^/api/tasks/[^/]+/status$', p):
            task_id = p.split('/')[3]
            self._task_status_update(task_id)
        elif re.match(r'^/api/tasks/[^/]+/md$', p) and self.command == 'PUT':
            task_id = p.split('/')[3]
            self._task_md_save(task_id)
        elif p == '/api/agents/config':
            self._agents_config_save()
        elif p == '/api/agents/daemon/start':
            self._agents_daemon_start()
        elif p == '/api/agents/daemon/stop':
            self._agents_daemon_stop()
        elif re.match(r'^/api/tasks/[^/]+/check/apply$', p):
            task_id = p.split('/')[3]
            self._check_apply(task_id)
        elif re.match(r'^/api/tasks/[^/]+/check$', p):
            task_id = p.split('/')[3]
            self._check_task(task_id)
        elif p == '/api/report/send':
            self._send_report()
        elif p == '/api/agents/sync':
            self._trigger_sync()
        elif p == '/api/agents/models':
            if self.command == "POST": self._agents_models_impl(self._read_body())
            else: self._agents_models()
        elif p == '/api/agents/index':
            self._trigger_index()
        elif re.match(r'^/api/agents/[^/]+/assign$', p):
            task_id = p.split('/')[3]
            self._assign_agent(task_id)
        elif re.match(r'^/api/agents/[^/]+/trigger$', p):
            task_id = p.split('/')[3]
            self._trigger_task(task_id)
        elif re.match(r'^/api/agents/[^/]+/cron/enable$', p):
            task_id = p.split('/')[3]
            self._enable_cron(task_id)
        elif re.match(r'^/api/agents/[^/]+/cron/disable$', p):
            task_id = p.split('/')[3]
            self._disable_cron(task_id)
        elif p == '/api/agents/terminal/start':
            self._terminal_start()
        elif p == '/api/agents/terminal/config':
            self._terminal_config_save()
        elif re.match(r'^/api/agents/terminal/[^/]+/chat$', p):
            tid = p.split('/')[4]
            self._terminal_chat(tid)
        elif re.match(r'^/api/agents/terminal/[^/]+/stop$', p):
            tid = p.split('/')[4]
            self._terminal_stop(tid)
        elif re.match(r'^/api/agents/terminal/session/[^/]+/end$', p):
            sid = p.split('/')[5]
            self._terminal_session_end(sid)
        elif re.match(r'^/api/agents/terminal/session/[^/]+/delete$', p):
            sid = p.split('/')[5]
            self._terminal_session_delete(sid)
        else:
            self._json({'error': 'Not found'}, 404)

    def do_DELETE(self):
        p = self.path.split('?')[0]
        if re.match(r'^/api/agents/sessions/[^/]+$', p):
            session_id = p.split('/')[4]
            self._session_delete_gateway(session_id)
        else:
            self._json({'error': 'Not found'}, 404)

    # ── /api/projects ─────────────────────────────────────────────────────────

    def _projects_list(self):
        self._json(_load_json(str(PROJ_FILE), []))

    def _regenerate_tasks(self):
        try:
            script_path = _BASE / "scripts" / "md_to_talaria.sh"
            result = subprocess.run(
                [str(script_path)],
                cwd=str(_BASE),
                capture_output=True,
                text=True,
                timeout=30
            )
            self._json({
                "status": "ok" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
        except subprocess.TimeoutExpired:
            self._json({"error": "Script timeout"}, 500)
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _task_md(self, task_id):
        # task_id might be a numeric ID or a slug
        tasks = _load_json(TASKS_FILE, [])
        task = next((t for t in tasks if str(t.get('id')) == str(task_id) or
                     str(t.get('id')).lstrip('0') == str(task_id).lstrip('0') or
                     t.get('slug') == str(task_id)), None)

        if task is None:
            self._json({'error': 'Task not found'}, 404)
            return

        # Find the MD file that has this ID in frontmatter
        md_content = None
        task_internal_id = str(task.get('id', ''))
        if TASKS_DIR.exists() and task_internal_id:
            for md_file in TASKS_DIR.glob('*.md'):
                text = md_file.read_text(errors='replace')
                id_match = re.search(r'^id:\s*["\']?([^"\'\n]+)["\']?', text, re.MULTILINE)
                if id_match and str(id_match.group(1)).lstrip('0') == task_internal_id.lstrip('0'):
                    md_content = text
                    break
        if md_content:
            self._json({'task_id': task_id, 'md': md_content})
        else:
            # Fall back to task JSON fields
            self._json({'task_id': task_id, 'md': None, 'task': task})

    def _task_md_save(self, task_id):
        """Save full markdown content for a task. Body: {"md": "..."}."""
        body = self._read_body()
        md_content = body.get('md', '')
        if not md_content:
            self._json({'error': 'md content required'}, 400)
            return
        # Find the task file
        task_file = None
        for md_file in TASKS_DIR.glob('*.md'):
            text = md_file.read_text(errors='replace')
            id_match = re.search(r'^id:\s*["\']?([^"\'\n]+)["\']?', text, re.MULTILINE)
            if id_match and str(id_match.group(1)).lstrip('0') == str(task_id).lstrip('0'):
                task_file = md_file
                break
        if not task_file:
            self._json({'error': f'Task {task_id} file not found'}, 404)
            return
        task_file.write_text(md_content)
        # Also update tasks.json metadata from frontmatter
        try:
            now = datetime.now().strftime('%Y-%m-%d')
            tasks = _load_json(TASKS_FILE, [])
            for t in tasks:
                tid = str(t.get('id'))
                if tid == str(task_id) or tid.lstrip('0') == str(task_id).lstrip('0'):
                    # Parse title from first heading
                    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
                    if title_match:
                        t['title'] = title_match.group(1).strip()
                    # Parse status from frontmatter
                    status_match = re.search(r'^status:\s*["\']?(\w+)["\']?', md_content, re.MULTILINE)
                    if status_match:
                        t['status'] = status_match.group(1)
                    # Parse description from frontmatter
                    desc_match = re.search(r'^description:\s*["\'](.+?)["\']', md_content, re.MULTILINE)
                    if desc_match:
                        t['description'] = desc_match.group(1)
                    t['modified'] = now
                    break
            Path(TASKS_FILE).write_text(json.dumps(tasks, indent=2))
        except Exception:
            pass  # Frontmatter saved, JSON sync is best-effort
        self._json({'success': True, 'task_id': task_id})

    def _task_status_update(self, task_id):
        """Update a task's status directly in tasks.json. Body: {"status": "todo|progress|done"}."""
        body = self._read_body()
        new_status = body.get('status', '').strip().lower()
        if new_status not in ('todo', 'progress', 'done', 'halt'):
            self._json({'error': 'status must be todo|progress|done|halt'}, 400)
            return
        try:
            now = datetime.now().strftime('%Y-%m-%d')
            tasks = _load_json(TASKS_FILE, [])
            updated = False
            task_file = None
            for t in tasks:
                tid = str(t.get('id'))
                if tid == str(task_id) or tid.lstrip('0') == str(task_id).lstrip('0'):
                    t['status'] = new_status
                    t['modified'] = now
                    task_file = t.get('file')
                    updated = True
                    break
            if not updated:
                self._json({'error': f'Task {task_id} not found'}, 404)
                return
            Path(TASKS_FILE).write_text(json.dumps(tasks, indent=2))
            # Write back to .md frontmatter
            if task_file:
                _update_task_md_field(task_file, 'status', new_status)
                _update_task_md_field(task_file, 'modified', now)
            self._json({'success': True, 'task_id': task_id, 'status': new_status, 'modified': now})
        except Exception as e:
            self._json({'error': str(e)}, 500)

    def _projects_save(self):
        body = self._read_body()
        # body can be one project object or an array
        projects = _load_json(str(PROJ_FILE), [])
        if isinstance(body, list):
            projects = body
        else:
            pid = body.get('id', '').strip()
            if not pid:
                self._json({'error': 'id required'}, 400)
                return
            proj_path = body.get('path', '').strip()
            if proj_path and not Path(proj_path).exists():
                self._json({'error': f'path does not exist: {proj_path}'}, 400)
                return
            existing = next((p for p in projects if p['id'] == pid), None)
            if existing:
                existing.update(body)
            else:
                projects.append(body)
        PROJ_FILE.write_text(json.dumps(projects, indent=2))
        self._json({'success': True, 'projects': projects})

    # ── /api/tasks/:id/check ─────────────────────────────────────────────────

    def _check_last(self, task_id):
        """Return the most recent check log for this task (any project)."""
        CHECK_LOGS.mkdir(parents=True, exist_ok=True)
        logs = sorted(
            CHECK_LOGS.glob(f'task-{task_id}-*.json'),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        # Skip apply-logs (they have no 'log' field)
        for lf in logs:
            if '-apply.json' in lf.name:
                continue
            try:
                data = json.loads(lf.read_text())
                if 'implemented' in data:
                    data['_log_file'] = lf.name
                    self._json(data)
                    return
            except Exception:
                continue
        self._json({'task_id': task_id, 'implemented': None, 'summary': 'No check run yet.'})

    def _check_task(self, task_id):
        """
        Run check_task.py for this task + the active project.

        NOTE: This runs inside Docker, but check_task.py needs access to project files
        on the host. The project path must be accessible from inside the container,
        OR this should delegate to a host-side service.

        For now, we return an error directing users to run the check on the host.
        """
        body       = self._read_body()
        project_id = body.get('project_id', '').strip()

        if not project_id:
            projects = _load_json(str(PROJ_FILE), [])
            active   = next((p for p in projects if p.get('active')), None)
            if not active:
                self._json({'error': 'No active project. Set project_id.'}, 400)
                return
            project_id = active['id']

        # Load project to get path
        projects = _load_json(str(PROJ_FILE), [])
        project = next((p for p in projects if p.get('id') == project_id), None)

        if not project:
            self._json({'error': f'Project {project_id} not found'}, 404)
            return

        project_path = project.get('path', '')

        # Check if path is accessible from Docker
        if not Path(project_path).exists():
            self._json({
                'error': f'Project path not accessible from Docker container',
                'task_id': task_id,
                'project_id': project_id,
                'project_path': project_path,
                'note': 'Run check on host: python3 scripts/check_task.py --task-id {} --project-id {}'.format(task_id, project_id)
            }, 400)
            return

        # If we get here, path is accessible - run the check
        accept = self.headers.get('Accept', '')
        use_sse = 'text/event-stream' in accept
        auto = body.get('auto', False)

        cmd = [
            'python3', CHECK_SCRIPT,
            '--task-id',    task_id,
            '--project-id', project_id,
        ]
        if auto:
            cmd.append('--auto')

        if use_sse:
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            def send_event(data: str):
                for line in data.splitlines():
                    self.wfile.write(f'data: {line}\n'.encode())
                self.wfile.write(b'\n')
                self.wfile.flush()

            try:
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, cwd=str(_BASE)
                )
                result_json = None
                capture_next = False
                for line in proc.stdout:
                    line = line.rstrip('\n')
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
                    send_event(line)
                proc.wait()
                if result_json:
                    self.wfile.write(
                        f'event: result\ndata: {json.dumps(result_json)}\n\n'.encode()
                    )
                    self.wfile.flush()
                self.wfile.write(b'event: done\ndata: {}\n\n')
                self.wfile.flush()
            except Exception as e:
                send_event(f'[ERROR] {e}')
                self.wfile.write(b'event: done\ndata: {}\n\n')
                self.wfile.flush()
        else:
            # Blocking JSON response
            import subprocess as sp
            r = sp.run(cmd, capture_output=True, text=True, cwd=str(_BASE), timeout=360)
            full = r.stdout + (r.stderr or '')
            result = None
            lines = full.splitlines()
            for i, line in enumerate(lines):
                if line == '__RESULT__' and i + 1 < len(lines):
                    try:
                        result = json.loads(lines[i + 1])
                    except Exception:
                        pass
                    break
            if result:
                self._json(result)
            else:
                self._json({'error': 'No result from check', 'log': full}, 500)

    def _check_apply(self, task_id):
        """Apply the suggested status change after user confirmation."""
        body       = self._read_body()
        project_id = body.get('project_id', '').strip()
        status     = body.get('status', '').strip()
        if status not in ('done', 'progress', 'todo'):
            self._json({'error': 'status must be done|progress|todo'}, 400)
            return

        if not project_id:
            projects = _load_json(str(PROJ_FILE), [])
            active   = next((p for p in projects if p.get('active')), None)
            project_id = active['id'] if active else 'unknown'

        cmd = [
            'python3', CHECK_SCRIPT,
            '--task-id',      task_id,
            '--project-id',   project_id,
            '--apply-status', status,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=str(_BASE), timeout=30)

        # Stamp modified date in tasks.json + .md
        try:
            now = datetime.now().strftime('%Y-%m-%d')
            tasks = _load_json(TASKS_FILE, [])
            for t in tasks:
                tid = str(t.get('id'))
                if tid == str(task_id) or tid.lstrip('0') == str(task_id).lstrip('0'):
                    t['modified'] = now
                    task_file = t.get('file')
                    if task_file:
                        _update_task_md_field(task_file, 'modified', now)
                    break
            Path(TASKS_FILE).write_text(json.dumps(tasks, indent=2))
        except Exception:
            pass
        try:
            result = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            result = {'applied_status': status, 'changed': False, 'raw': r.stdout}
        self._json(result)

    # ── /api/report ───────────────────────────────────────────────────────────

    def _preview_report(self):
        try:
            tasks = _load_json(TASKS_FILE, [])
            report_tasks = [t for t in tasks if t.get('status') in ('done', 'progress')]
            self._json({
                'header_html': self._build_report_header(),
                'tasks': [
                    {'id': t.get('id'), 'html': self._build_task_block_html(t)}
                    for t in report_tasks
                ],
                'footer_html': self._build_report_footer(),
            })
        except Exception as e:
            self._json({'error': str(e)}, 500)

    def _build_report_header(self):
        today = datetime.now().strftime('%B %d, %Y')
        return f'''
        <div class="adaptive-card">
            <div class="card-header">
                <img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/godot.png" alt="icon">
                <div class="card-header-text">
                    <h3>ADT Report : Tekton Dash</h3>
                    <p>{today}</p>
                </div>
            </div>'''

    def _build_task_block_html(self, task):
        title    = str(task.get('title', 'Untitled'))
        desc     = str(task.get('description') or '')[:150]
        task_id  = task.get('id', '')
        status   = str(task.get('status', ''))
        assignee = str(task.get('assignee', ''))
        ftitle   = f'[#{task_id}] {html.escape(title)}' if task_id != '' else html.escape(title)
        if status == 'progress':
            icon  = 'https://cdn-icons-png.flaticon.com/512/833/833602.png'
            color = '#0078d4'
        else:
            icon  = 'https://cdn-icons-png.flaticon.com/512/190/190411.png'
            color = '#107c10'
        agent_tag = f'<small style="color:#888">🤖 {html.escape(assignee)}</small>' if assignee else ''
        return f'''
                <div class="task-item">
                    <img src="{html.escape(icon, quote=True)}" alt="status">
                    <div class="task-content">
                        <h4 style="color:{html.escape(color, quote=True)}">{ftitle}</h4>
                        <p>{html.escape(desc)}</p>
                        {agent_tag}
                    </div>
                </div>'''

    def _build_report_footer(self):
        return f'''
            <div style="margin-top:16px;padding-top:16px;border-top:1px solid #edebe9">
                <a href="http://localhost:8080" style="color:#0078d4;text-decoration:none;font-weight:600">→ Open Talaria Board</a>
            </div>
        </div>'''

    def _send_report(self):
        tmp_path = None
        try:
            body = self._read_body()
            selected_ids = body.get('task_ids', []) or []
            webhook = body.get('webhook', 'coding-dev')  # 'coding-dev' or 'dev-test'

            if selected_ids:
                all_tasks = _load_json(TASKS_FILE, [])
                ids_str = {str(i) for i in selected_ids}
                filtered = [t for t in all_tasks if str(t.get('id')) in ids_str]
                if not filtered:
                    self._json({'success': False, 'error': 'No matching tasks'}, 400)
                    return
                tmp = tempfile.NamedTemporaryFile(
                    mode='w', suffix='.json', delete=False, dir='/tmp',
                    prefix='talaria_report_'
                )
                json.dump(filtered, tmp)
                tmp.close()
                tmp_path = tmp.name

            cmd = [REPORT_SCRIPT, webhook] if tmp_path is None else [REPORT_SCRIPT, tmp_path, webhook]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if r.returncode == 0:
                self._json({'success': True, 'message': 'Report sent', 'output': r.stdout})
            else:
                self._json({'success': False, 'error': r.stderr or 'script failed'}, 500)
        except subprocess.TimeoutExpired:
            self._json({'success': False, 'error': 'timeout'}, 500)
        except Exception as e:
            self._json({'success': False, 'error': str(e)}, 500)
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

    # ── /api/agents ───────────────────────────────────────────────────────────

    def _agents_config_get(self):
        default = {
            "execution_mode": "local",
            "remote_url": "",
            "project_target": "tekton-enet",
            "category_profile_map": {
                "CORE": "dev",
                "CLIENT": "dev",
                "BACKEND": "dev",
                "SECURITY": "default",
                "TESTING": "default",
                "DEVOPS": "default",
                "ANALYTICS": "default",
                "NETWORKING": "dev"
            },
            "default_profile": "default",
            "provider": "openai",
            "base_url": "",
            "api_key": "",
            "model": ""
        }
        self._json(_load_json(AGENT_CONFIG, default))

    def _agents_config_save(self):
        data = self._read_body()
        _save_json(AGENT_CONFIG, data)
        self._json({'status': 'ok'})

    def _agents_models(self):
        body = {}
        if self.command == "POST":
            body = self._read_body() or {}
        self._agents_models_impl(body)

    def _agents_models_impl(self, body):
        import urllib.request
        import urllib.error
        config = _load_json(AGENT_CONFIG, {})
        provider = body.get("provider") or config.get("provider", "openai")
        base_url = body.get("base_url") or config.get("base_url", "")
        # Always use the body api_key if provided, otherwise fall back to config
        api_key = body.get("api_key") if "api_key" in body else config.get("api_key", "")
        if api_key is None:
            api_key = ""

        print(f"[models] provider={provider} base_url={base_url} api_key_set={bool(api_key)}", flush=True)

        if not api_key and provider not in ("ollama", "custom"):
            self._json({"models": [], "error": "No API key configured"})
            return

        # Build list of URLs to try
        urls_to_try = []
        if provider == "ollama":
            urls_to_try.append((base_url or "http://localhost:11434").rstrip("/") + "/api/tags")
        elif base_url:
            base = base_url.rstrip("/")
            
            # Use urllib.request directly without adding extra endpoints first to see if base is already the direct models endpoint.
            # But normally we just guess.
            urls_to_try.extend([
                base,
                base + "/models",
            ])
            if base.endswith("/v1"):
                urls_to_try.extend([
                    base[:-3] + "/models",
                    base[:-3] + "/api/tags",
                ])
            else:
                urls_to_try.extend([
                    base + "/v1/models",
                    base + "/api/tags",
                    base + "/models?limit=100",
                ])
        elif provider == "openai":
            urls_to_try.append("https://api.openai.com/v1/models")
        elif provider == "anthropic":
            urls_to_try.append("https://api.anthropic.com/v1/models")
        elif provider == "google":
            urls_to_try.append("https://generativelanguage.googleapis.com/v1/models")

        if not urls_to_try:
            self._json({"models": [], "error": f"No endpoint for provider: {provider}"})
            return

        import urllib.request
        import urllib.error
        
        def try_url(url):
            print(f"[models] trying URL: {url}", flush=True)
            try:
                req = urllib.request.Request(url, headers={"Accept": "application/json"})
                
                # Check 9router explicit empty key rule
                is_9router = "20128" in url
                
                if api_key:
                    if provider == "google":
                        url += ("&" if "?" in url else "?") + f"key={api_key}"
                        # Re-create request to include URL query param update
                        req = urllib.request.Request(url, headers={"Accept": "application/json"})
                    else:
                        req.add_header("Authorization", f"Bearer {api_key}")
                else:
                    if provider == "custom":
                        # Some local servers mock OpenAI but expect the Authorization header to be literally present,
                        # even if empty or dummy. Let's send a dummy one just in case they're lazy auth-checkers.
                        if is_9router:
                            # Actually, 9router will just reject dummy. We MUST omit it to get a 401? No, 401 means it rejected it.
                            # Wait, 9router explicitly says "API key required for remote API access". We CANNOT fetch models from it without a key.
                            pass
                        else:
                            req.add_header("Authorization", "Bearer dummy")
                            req.add_header("x-goog-api-key", "dummy")
                # Anthropic handles their own specific header, if user chose custom, we shouldn't add anthropic specific headers.
                if provider == "anthropic":
                    req.add_header("anthropic-version", "2023-06-01")
                
                resp = urllib.request.urlopen(req, timeout=10)
                
                return json.loads(resp.read().decode())
            except urllib.error.HTTPError as e:
                # Capture the actual HTTP error body if possible to help debug Custom endpoints returning 401s
                try:
                    body = e.read().decode()
                    print(f"[models] HTTP Error {e.code} body: {body}", flush=True)
                except Exception:
                    pass
                raise e

        last_error = None
        for url in urls_to_try:
            try:
                raw = try_url(url)
                print(f"[models] success from {url}, response keys: {list(raw.keys()) if isinstance(raw, dict) else type(raw)}", flush=True)
                models = []
                if isinstance(raw, list):
                    models = sorted([m.get("id") or m.get("name", "") for m in raw if m.get("id") or m.get("name")])
                elif isinstance(raw, dict):
                    if "data" in raw and isinstance(raw["data"], list):
                        models = sorted([m.get("id") or m.get("name", "") for m in raw["data"] if m.get("id") or m.get("name")])
                    elif "models" in raw and isinstance(raw["models"], list):
                        models = sorted([m.get("id") or m.get("name", "") for m in raw["models"] if m.get("id") or m.get("name")])
                if models:
                    self._json({"models": models, "debug": f"Fetched from {url}"})
                    return
            except Exception as e:
                last_error = str(e)
                print(f"[models] failed {url}: {last_error}", flush=True)
                continue

        self._json({"models": [], "error": f"All endpoints failed. Last: {last_error}. Tried: {', '.join(urls_to_try)}"})

    def _agents_profiles(self):
        try:
            profiles_file = _BASE / 'data' / 'hermes_profiles.json'
            if profiles_file.exists():
                profiles = json.loads(profiles_file.read_text())
                if profiles and profiles != ['default']:
                    self._json(profiles)
                    return
        except Exception:
            pass
        # Fallback: aggregate from agent state
        state = _load_json(STATE_FILE, {'tasks': {}})
        task_profiles = set()
        for tid, entry in state.get('tasks', {}).items():
            p = entry.get('assignee', 'default')
            if p and len(p) > 1:
                task_profiles.add(p)
        profiles = ['default', *sorted(task_profiles - {'default'})] if task_profiles else ['default']
        self._json(profiles)

    def _agents_hermes_status(self):
        """Live Hermes connectivity check."""
        import platform
        import urllib.request
        import urllib.error

        system = platform.system()
        mode = CONFIG["hermes"]["mode"]
        remote_url = CONFIG["hermes"]["remote_url"]

        if mode == "remote":
            # Real HTTP check against gateway
            candidates = [remote_url]
            if "localhost" not in remote_url and "127.0.0.1" not in remote_url:
                candidates.append("http://localhost:8642")

            last_error = None
            for url in candidates:
                try:
                    req = urllib.request.Request(f"{url}/api/sessions?limit=1", headers={"Accept": "application/json"})
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        data = json.loads(resp.read().decode())
                        sessions = data.get("data", [])
                        profiles_file = _BASE / 'data' / 'hermes_profiles.json'
                        try:
                            profiles = json.loads(profiles_file.read_text()) if profiles_file.exists() else ['default']
                        except Exception:
                            profiles = ['default']
                        self._json({
                            'available': True,
                            'mode': 'remote',
                            'url': url,
                            'platform': system,
                            'profiles': len(profiles),
                            'sessions': len(sessions),
                            'live': True
                        })
                        return
                except Exception as e:
                    last_error = str(e)
                    continue

            # Gateway unreachable from this container. Check if agent-sync has cached data.
            sessions_file = _BASE / 'data' / 'hermes_sessions.json'
            if sessions_file.exists():
                mtime = sessions_file.stat().st_mtime
                age = time.time() - mtime
                if age < 600:  # cache < 10 min old
                    profiles_file = _BASE / 'data' / 'hermes_profiles.json'
                    try:
                        profiles = json.loads(profiles_file.read_text()) if profiles_file.exists() else ['default']
                    except Exception:
                        profiles = ['default']
                    self._json({
                        'available': True,
                        'mode': 'remote',
                        'url': remote_url,
                        'platform': system,
                        'profiles': len(profiles),
                        'live': True,
                        'cached': True
                    })
                    return

            self._json({
                'available': False,
                'mode': 'remote',
                'url': remote_url,
                'platform': system,
                'error': last_error or 'Gateway unreachable',
                'live': True
            })
            return

        # Local mode: check CLI
        import shutil
        hermes_path = shutil.which('hermes')
        if hermes_path:
            try:
                out, _ = subprocess.run([hermes_path, '--version'], capture_output=True, text=True, timeout=5)
                version = out.strip()
            except Exception:
                version = ''
            self._json({
                'available': True,
                'mode': 'local',
                'path': hermes_path,
                'version': version,
                'platform': system,
                'live': True
            })
            return

        self._json({
            'available': False,
            'mode': 'local',
            'platform': system,
            'error': 'hermes CLI not found in PATH',
            'live': True
        })

    def _agents_hermes_local_config(self):
        """Read ~/.hermes/config.yaml and return provider/model settings."""
        import yaml
        config_path = Path.home() / '.hermes' / 'config.yaml'
        if not config_path.exists():
            self._json({'error': 'config not found'}, 404)
            return
        try:
            data = yaml.safe_load(config_path.read_text()) or {}
        except Exception as e:
            self._json({'error': str(e)}, 500)
            return
        model_cfg = data.get('model', {})
        self._json({
            'provider': model_cfg.get('provider', 'custom'),
            'base_url': model_cfg.get('base_url', ''),
            'api_key': model_cfg.get('api_key', ''),
            'model': model_cfg.get('default', ''),
        })


    def _terminal_profiles(self):
        pd = Path.home() / ".hermes" / "profiles"
        profs = ["default"]
        if pd.is_dir():
            profs.extend(d.name for d in pd.iterdir() if d.is_dir() and not d.name.startswith("."))
        self._json(sorted(profs))

    def _terminal_config_get(self):
        """Return saved terminal default model/provider config."""
        cfg_file = _BASE / 'data' / 'terminal_config.json'
        cfg = _load_json(str(cfg_file), {
            'model': 'kr/claude-sonnet-4.5',
            'provider_url': 'http://127.0.0.1:20821',
        })
        self._json(cfg)

    def _terminal_config_save(self):
        """Save terminal default model/provider config."""
        body = self._read_body()
        cfg_file = _BASE / 'data' / 'terminal_config.json'
        existing = _load_json(str(cfg_file), {})
        existing.update({k: v for k, v in body.items() if k in ('model', 'provider_url')})
        _save_json(str(cfg_file), existing)
        self._json({'success': True, 'config': existing})

    def _terminal_models(self):
        """Fetch model list from provider URLs."""
        import urllib.request, urllib.error
        cfg_file = _BASE / 'data' / 'terminal_config.json'
        cfg = _load_json(str(cfg_file), {})
        provider_url = cfg.get('provider_url', 'http://127.0.0.1:20821')

        # Try both known local provider ports
        candidates = [provider_url]
        for port in ['20821', '20128']:
            url = f'http://127.0.0.1:{port}'
            if url != provider_url:
                candidates.append(url)

        for base_url in candidates:
            try:
                req = urllib.request.Request(
                    f'{base_url}/v1/models',
                    headers={'Accept': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    models = [m.get('id') or m.get('name', '') for m in data.get('data', [])]
                    models = sorted([m for m in models if m])
                    self._json({'models': models, 'provider_url': base_url})
                    return
            except Exception:
                continue

        self._json({'models': [], 'error': 'Could not reach any provider URL'})

    def _terminal_start(self):
        body = self._read_body()
        profile = body.get("profile", "dev")
        import uuid
        import time
        now = time.localtime()
        prefix = time.strftime("%Y%m%d_%H%M%S", now)
        sid = f"{prefix}_{uuid.uuid4().hex[:6]}"

        # Load saved terminal config for default model
        cfg_file = _BASE / 'data' / 'terminal_config.json'
        saved_cfg = _load_json(str(cfg_file), {})
        default_model = saved_cfg.get('model', 'kr/claude-sonnet-4.5')

        with TERMINAL_LOCK:
            model = body.get("model") or default_model
            TERMINAL_SESSIONS[sid] = {
                "profile": profile,
                "model": model,
                "task_id": body.get("task_id"),
                "project": body.get("project"),
                "history": [],
                "created": time.time()
            }
        
        self._json({
            "id": sid,
            "hermes_session_id": sid,
            "profile": profile,
            "model": model,
            "task_id": body.get("task_id"),
            "project": body.get("project"),
            "history": []
        })

    def _terminal_chat(self, tid):
        body = self._read_body()
        message = body.get("message", "").strip()
        if not message:
            return self._json({"error": "Empty message"}, 400)
            
        with TERMINAL_LOCK:
            s = TERMINAL_SESSIONS.get(tid)
            if not s:
                return self._json({"error": "Session not found"}, 404)
            profile = s["profile"]
            
        import subprocess
        # If hermes_session_id equals tid, it means it's a fake ID we just generated.
        # So we don't pass --resume, which allows Hermes to create a new session.
        cmd = ["hermes", "--profile", profile, "chat", "-Q", "-q", message]
        if s.get("model"):
            cmd.extend(["-m", s["model"]])
        if s.get("hermes_session_id") and s.get("hermes_session_id") != tid:
            cmd.extend(["--resume", s["hermes_session_id"]])
            
        if s.get("project"):
            cwd = s["project"]
        else:
            cwd = str(_BASE)
            
        try:
            res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)

            # Extract session ID from stderr if present
            new_sid = None
            for line in res.stderr.split("\n"):
                if "session_id:" in line:
                    new_sid = line.split("session_id:")[-1].strip()

            if new_sid:
                s["hermes_session_id"] = new_sid

            if res.returncode == 0:
                out = res.stdout.strip()
                s.setdefault("history", []).append({"role": "user", "content": message})
                s["history"].append({"role": "assistant", "content": out})

                # Auto-transition logic
                if "done" in out.lower() and s.get("task_id"):
                    import json
                    try:
                        tasks = json.loads(Path(TASKS_FILE).read_text())
                        for t in tasks:
                            if str(t.get("id")) == str(s["task_id"]) or str(t.get("id")).lstrip("0") == str(s["task_id"]).lstrip("0"):
                                t["status"] = "Done"
                                break
                        Path(TASKS_FILE).write_text(json.dumps(tasks, indent=2))
                    except: pass
                    
                self._json({"response": out, "hermes_session_id": s.get("hermes_session_id") or tid})
            else:
                err_msg = res.stderr.strip() or res.stdout.strip() or "Hermes command failed"
                self._json({"error": err_msg}, 500)
        except subprocess.TimeoutExpired as e:
            # Return whatever partial output was captured before timeout
            partial = (e.stdout or b'').decode('utf-8', errors='replace').strip()
            partial_err = (e.stderr or b'').decode('utf-8', errors='replace').strip()
            out = partial or partial_err or 'Hermes timed out (600s). Task may still be in progress.'
            s.setdefault("history", []).append({"role": "user", "content": message})
            s["history"].append({"role": "assistant", "content": out})
            self._json({"response": out, "hermes_session_id": s.get("hermes_session_id") or tid, "timeout": True})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _terminal_stop(self, tid):
        self._json({"ok": True})

    def _terminal_session_end(self, sid):
        with TERMINAL_LOCK:
            TERMINAL_SESSIONS.pop(sid, None)
        self._json({"ok": True})

    def _terminal_session_delete(self, sid):
        with TERMINAL_LOCK:
            TERMINAL_SESSIONS.pop(sid, None)
        self._json({"ok": True})

    def _terminal_status(self, tid):
        with TERMINAL_LOCK:
            s = TERMINAL_SESSIONS.get(tid)
            if not s:
                return self._json({"running": False}, 200)
            self._json({
                "running": True,
                "profile": s.get("profile", ""),
                "model": s.get("model", ""),
                "task_id": s.get("task_id"),
                "project": s.get("project"),
                "hermes_session_id": tid,
                "history_count": len(s.get("history", [])),
                "created": s.get("created"),
            })


    def _gateway_proxy(self, path, method="GET", body=None, fallback=None):
        import urllib.request
        import json
        gateway_url = "http://localhost:8642"
        api_url = f"{gateway_url}{path}"
        try:
            req = urllib.request.Request(api_url, method=method)
            if body:
                req.add_header("Content-Type", "application/json")
                req.data = json.dumps(body).encode()
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                self._json(data)
        except Exception as e:
            if fallback is not None:
                self._json(fallback)
            else:
                self._json({"error": "Gateway unreachable: " + str(e)}, 502)

    def _agents_list(self): self._gateway_proxy("/api/agents", fallback=[])
    def _agents_status(self): self._gateway_proxy("/api/agents/status", fallback={"gateway": "offline"})
    


    def _get_api_key(self):
        return ""

    def _agents_sessions(self):
        """Fetch live sessions from the Hermes gateway API."""
        import subprocess
        import os
        from pathlib import Path
        try:
            profiles = ["default"]
            prof_dir = Path.home() / ".hermes" / "profiles"
            if prof_dir.exists():
                for p in prof_dir.iterdir():
                    if p.is_dir():
                        profiles.append(p.name)
            
            sessions = []
            for prof in profiles:
                cmd = ["hermes"]
                if prof != "default":
                    cmd.extend(["--profile", prof])
                cmd.extend(["sessions", "list", "--limit", "100"])
                
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if res.returncode != 0:
                    continue
                
                out_lines = res.stdout.split("\n")
                if len(out_lines) > 2:
                    for l in out_lines[2:]:
                        if len(l) < 88: continue
                        title = l[:33].strip()
                        preview = l[33:74].strip()
                        last_active = l[74:88].strip()
                        sid = l[88:].strip()
                        if title == "—" or not title:
                            title = preview if preview else sid
                        sessions.append({
                            "id": sid,
                            "title": title,
                            "preview": preview,
                            "last_active_fmt": last_active,
                            "profile": prof
                        })
            self._json({"sessions": sessions})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _session_delete_gateway(self, session_id):
        """Delete a session via hermes CLI.

        Uses list-then-delete-then-verify flow because hermes returns
        rc=0 for both real deletes and "not found" cases.
        """
        import subprocess
        import re
        from pathlib import Path

        SID_RE = re.compile(r"^\d{8}_\d{6}_[0-9a-f]+$")

        # Collect profiles to search
        profiles = ["default"]
        prof_dir = Path.home() / ".hermes" / "profiles"
        if prof_dir.exists():
            for p in prof_dir.iterdir():
                if p.is_dir() and p.name not in profiles:
                    profiles.append(p.name)

        def _hermes(args, prof):
            cmd = ["hermes"]
            if prof != "default":
                cmd.extend(["--profile", prof])
            cmd.extend(args)
            return subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        def _list_ids(prof):
            """Return set of session ids owned by the given profile."""
            try:
                res = _hermes(["sessions", "list", "--limit", "500"], prof)
            except Exception:
                return set()
            if res.returncode != 0:
                return set()
            ids = set()
            for line in res.stdout.split("\n")[2:]:
                clean = re.sub(r"\x1b\[[0-9;]*m", "", line)
                if len(clean) < 89:
                    continue
                sid = clean[88:].strip()
                if SID_RE.match(sid):
                    ids.add(sid)
            return ids

        # 1. Find which profile (if any) owns the id
        owners = [prof for prof in profiles if session_id in _list_ids(prof)]
        if not owners:
            self._json({"error": f"Session {session_id} not found"}, 404)
            return

        prof = owners[0]
        # 2. Delete via that profile
        try:
            del_res = _hermes(["sessions", "delete", "--yes", session_id], prof)
        except Exception as e:
            self._json({"error": f"Delete failed: {e}"}, 500)
            return

        # 3. Verify the id is actually gone from that profile's store
        if session_id in _list_ids(prof):
            self._json({
                "error": f"Session {session_id} still present after delete",
                "stdout": del_res.stdout.strip(),
                "stderr": del_res.stderr.strip(),
            }, 500)
            return

        # 4. Drop from in-memory map
        with TERMINAL_LOCK:
            TERMINAL_SESSIONS.pop(session_id, None)
        self._json({"success": True, "session_id": session_id, "profile": prof})

    def _agents_session_messages(self, session_id):
        import subprocess
        import json
        from pathlib import Path
        try:
            profiles = ["default"]
            prof_dir = Path.home() / ".hermes" / "profiles"
            if prof_dir.exists():
                for p in prof_dir.iterdir():
                    if p.is_dir():
                        profiles.append(p.name)
            
            for prof in profiles:
                cmd = ["hermes"]
                if prof != "default":
                    cmd.extend(["--profile", prof])
                cmd.extend(["sessions", "export", "--session-id", session_id, "-"])
                
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if res.returncode == 0:
                    try:
                        data = json.loads(res.stdout.strip())
                        self._json({"messages": data.get("messages", [])})
                        return
                    except json.JSONDecodeError:
                        pass
            
            self._json({"error": "Failed to fetch session messages: Session not found in any profile"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)

from socketserver import ThreadingMixIn
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    
def run_server(port=8080):
    server = ThreadingHTTPServer(('', port), TalariaAPIHandler)
    print(f"Talaria API Server running at http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    run_server()
