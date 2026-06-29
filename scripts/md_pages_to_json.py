#!/usr/bin/env python3
"""
Convert markdown page files to JSON + render static HTML for GitHub Pages.

Inputs :  pages/*.md
Outputs:  data/pages.json        — list of page metadata (slug, title, file)
          docs/<slug>/index.html — rendered permalink page for each entry
          docs/pages.json        — same JSON, for the nav dropdown on /
          docs/index.html-pages-snippet.html — unused, kept for symmetry

The rendered HTML uses the same theme + Markdown pipeline as html/index.html
so the look-and-feel is identical to the main board.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ── Paths ────────────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent.resolve()
_ROOT = _HERE.parent
PAGES_DIR = _ROOT / "pages"
HTML_DIR = _ROOT / "html"
DOCS_DIR = _ROOT / "docs"
DATA_DIR = _ROOT / "data"

PAGE_TEMPLATE = _HERE / "page_template.html"


# ── Frontmatter parser (same shape as md_to_json.py) ─────────────────────────
_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    match = _FRONT_MATTER_RE.match(content)
    if not match:
        return {}, content
    fm_text, body = match.group(1), match.group(2)
    fm: Dict[str, Any] = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.lower() in ("null", "none", ""):
            value = None
        elif value.isdigit():
            value = int(value)
        fm[key] = value
    return fm, body.strip()


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "untitled"


# ── Tiny Markdown renderer (mirrors the look in index.html) ──────────────────
# We deliberately keep the renderer inline + dependency-free so the build script
# runs anywhere with just Python 3. The output matches the .markdown-body class
# styling already in html/index.html.

_INLINE_RE = re.compile(
    r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))"
)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITAL_RE = re.compile(r"\*([^*]+)\*")
_CODE_RE = re.compile(r"`([^`]+)`")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_inline(text: str) -> str:
    # Order matters: links first so the resulting href isn't escaped
    text = _LINK_RE.sub(lambda m: f'<a href="{esc(m.group(2))}">{esc(m.group(1))}</a>', text)
    text = _CODE_RE.sub(lambda m: f"<code>{esc(m.group(1))}</code>", text)
    text = _BOLD_RE.sub(lambda m: f"<strong>{esc(m.group(1))}</strong>", text)
    text = _ITAL_RE.sub(lambda m: f"<em>{esc(m.group(1))}</em>", text)
    return text


def render_markdown(md: str) -> str:
    lines = md.split("\n")
    out: List[str] = []
    in_code = False
    code_buf: List[str] = []
    list_open: List[str] = []  # 'ul' / 'ol'

    def close_lists():
        nonlocal list_open
        while list_open:
            out.append(f"</{list_open.pop()}>")

    i = 0
    n = len(lines)

    def is_list_item(s: str) -> bool:
        return bool(re.match(r"^\s*[-*]\s+", s)) or bool(re.match(r"^\s*\d+\.\s+", s))

    def is_list_continuation(s: str) -> bool:
        # Two or more leading spaces inside an open list = continuation of
        # the previous list item (CommonMark).
        return bool(re.match(r"^\s{2,}\S", s))

    while i < n:
        line = lines[i]
        # fenced code block
        if line.strip().startswith("```"):
            if list_open:
                close_lists()
            if in_code:
                out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # table (very small: header + separator + body)
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            if list_open:
                close_lists()
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            body_rows: List[List[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                body_rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(
                "<table><thead><tr>"
                + "".join(f"<th>{render_inline(esc(c))}</th>" for c in header_cells)
                + "</tr></thead><tbody>"
            )
            for row in body_rows:
                out.append(
                    "<tr>" + "".join(f"<td>{render_inline(esc(c))}</td>" for c in row) + "</tr>"
                )
            out.append("</tbody></table>")
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if list_open:
                close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{render_inline(esc(m.group(2)))}</h{level}>")
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            if list_open:
                close_lists()
            quote_lines: List[str] = []
            while i < n and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip(">").lstrip())
                i += 1
            out.append("<blockquote>" + render_markdown("\n".join(quote_lines)) + "</blockquote>")
            continue

        # unordered list
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if m:
            if list_open and list_open[-1] != "ul":
                out.append(f"</{list_open.pop()}>")
            if not list_open or list_open[-1] != "ul":
                out.append("<ul>")
                list_open.append("ul")
            out.append("<li>" + render_inline(esc(m.group(2))))
            i += 1
            # consume continuation lines (indented ≥ 2 spaces, or blank+indented)
            while i < n:
                cont = lines[i]
                if is_list_continuation(cont):
                    out.append(" " + render_inline(esc(cont.strip())))
                    i += 1
                elif cont.strip() == "" and i + 1 < n and is_list_continuation(lines[i + 1]):
                    i += 1  # eat blank between continuation lines
                else:
                    break
            out.append("</li>")
            continue

        # ordered list
        m = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if m:
            if list_open and list_open[-1] != "ol":
                out.append(f"</{list_open.pop()}>")
            if not list_open or list_open[-1] != "ol":
                out.append("<ol>")
                list_open.append("ol")
            out.append("<li>" + render_inline(esc(m.group(2))))
            i += 1
            while i < n:
                cont = lines[i]
                if is_list_continuation(cont):
                    out.append(" " + render_inline(esc(cont.strip())))
                    i += 1
                elif cont.strip() == "" and i + 1 < n and is_list_continuation(lines[i + 1]):
                    i += 1
                else:
                    break
            out.append("</li>")
            continue

        # blank line — close any open list, skip
        if line.strip() == "":
            if list_open:
                close_lists()
            i += 1
            continue

        # horizontal rule — close lists first
        if re.match(r"^\s*---\s*$", line):
            if list_open:
                close_lists()
            out.append("<hr>")
            i += 1
            continue

        # paragraph: collect contiguous non-blank lines that are NOT
        # structural (headings, lists, blockquote, code, hr, table).
        if list_open:
            close_lists()
        para: List[str] = [line]
        i += 1
        while (
            i < n
            and lines[i].strip() != ""
            and not re.match(r"^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|>|```|\s*---)", lines[i])
            and "|" not in lines[i]
        ):
            para.append(lines[i])
            i += 1
        out.append("<p>" + render_inline(esc(" ".join(para))) + "</p>")

    # close dangling lists / code fences
    close_lists()
    if in_code:
        out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")

    return "\n".join(out)


# ── Page rendering ───────────────────────────────────────────────────────────
def render_page(slug: str, title: str, body_html: str, description: str = "") -> str:
    if not PAGE_TEMPLATE.exists():
        raise SystemExit(f"missing template: {PAGE_TEMPLATE}")
    tmpl = PAGE_TEMPLATE.read_text(encoding="utf-8")
    nav_links = build_nav_links(slug)
    return (
        tmpl
        .replace("{{TITLE}}", esc(title))
        .replace("{{DESCRIPTION}}", esc(description))
        .replace("{{SLUG}}", esc(slug))
        .replace("{{BODY}}", body_html)
        .replace("{{NAV_LINKS}}", nav_links)
    )


def build_nav_links(current_slug: str) -> str:
    pages = load_pages_metadata()
    items: List[str] = []
    for p in pages:
        active = ' class="active"' if p["slug"] == current_slug else ""
        href = f"{p['slug']}/"
        items.append(f'<a href="{href}"{active}>{esc(p["title"])}</a>')
    return "\n".join(items)


def load_pages_metadata() -> List[Dict[str, Any]]:
    pages: List[Dict[str, Any]] = []
    for md_file in sorted(PAGES_DIR.glob("*.md")):
        fm, _ = parse_frontmatter(md_file.read_text(encoding="utf-8"))
        if not fm:
            continue
        slug = str(fm.get("slug") or slugify(md_file.stem))
        pages.append(
            {
                "slug": slug,
                "title": str(fm.get("title", slug)),
                "description": str(fm.get("description", "")),
                "modified": str(fm.get("modified", "")),
                "file": md_file.name,
            }
        )
    return pages


# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    if not PAGES_DIR.exists():
        print(f"[pages] no pages/ directory at {PAGES_DIR}")
        return

    DOCS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    pages = load_pages_metadata()

    # 1) write data/pages.json (source of truth)
    (DATA_DIR / "pages.json").write_text(
        json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 2) mirror to docs/pages.json for the static nav dropdown
    (DOCS_DIR / "pages.json").write_text(
        json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3) render each page to docs/<slug>/index.html
    for md_file in sorted(PAGES_DIR.glob("*.md")):
        fm, body = parse_frontmatter(md_file.read_text(encoding="utf-8"))
        if not fm:
            continue
        slug = str(fm.get("slug") or slugify(md_file.stem))
        title = str(fm.get("title", slug))
        description = str(fm.get("description", ""))

        body_html = render_markdown(body)
        page_html = render_page(slug, title, body_html, description)

        out_dir = DOCS_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page_html, encoding="utf-8")
        print(f"[pages] rendered /{slug}/  ({md_file.name})")

    print(f"[pages] {len(pages)} page(s) generated → {DOCS_DIR}")


if __name__ == "__main__":
    main()