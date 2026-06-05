#!/usr/bin/env python3
import curses
import json
import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def load_tasks():
    tasks_file = DATA_DIR / "tasks.json"
    if not tasks_file.exists():
        # Try to generate
        os.system(f"python3 {BASE_DIR}/scripts/md_to_json.py > /dev/null 2>&1")
    
    if tasks_file.exists():
        with open(tasks_file, 'r') as f:
            return json.load(f)
    return []

def draw_board(stdscr, tasks):
    curses.curs_set(0)
    stdscr.nodelay(False)
    
    # Categorize tasks
    cols = {"todo": [], "in_progress": [], "done": []}
    for t in tasks:
        st = t.get("status", "todo").lower()
        if st in ["todo", "pending", "open", "backlog"]:
            cols["todo"].append(t)
        elif st in ["in_progress", "inprogress", "doing", "active"]:
            cols["in_progress"].append(t)
        elif st in ["done", "completed", "closed", "resolved"]:
            cols["done"].append(t)
        else:
            cols["todo"].append(t) # Default

    max_items = max(len(cols["todo"]), len(cols["in_progress"]), len(cols["done"]))
    scroll_pos = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Header
        title = " Talaria TUI - Hermes Style (Press 'q' to quit, Up/Down to scroll) "
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(0, 0, title.center(width))
        stdscr.attroff(curses.A_REVERSE)

        col_width = width // 3
        
        # Column titles
        stdscr.addstr(2, 0, f" TODO ({len(cols['todo'])}) ".center(col_width), curses.A_BOLD)
        stdscr.addstr(2, col_width, f" IN PROGRESS ({len(cols['in_progress'])}) ".center(col_width), curses.A_BOLD)
        stdscr.addstr(2, col_width * 2, f" DONE ({len(cols['done'])}) ".center(col_width), curses.A_BOLD)
        
        # Draw tasks
        for row in range(height - 4):
            task_idx = row + scroll_pos
            if task_idx < max_items:
                # Todo
                if task_idx < len(cols["todo"]):
                    t = cols["todo"][task_idx]
                    title_str = f"[{t.get('priority', '-')}] {t.get('title', 'Unknown')}"[:col_width-2]
                    stdscr.addstr(row + 4, 1, title_str)
                # In Progress
                if task_idx < len(cols["in_progress"]):
                    t = cols["in_progress"][task_idx]
                    title_str = f"[{t.get('priority', '-')}] {t.get('title', 'Unknown')}"[:col_width-2]
                    stdscr.addstr(row + 4, col_width + 1, title_str)
                # Done
                if task_idx < len(cols["done"]):
                    t = cols["done"][task_idx]
                    title_str = f"[{t.get('priority', '-')}] {t.get('title', 'Unknown')}"[:col_width-2]
                    stdscr.addstr(row + 4, col_width * 2 + 1, title_str)

        stdscr.refresh()
        
        # Input handling
        try:
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            elif key == curses.KEY_DOWN or key == ord('j'):
                if scroll_pos < max_items - (height - 4):
                    scroll_pos += 1
            elif key == curses.KEY_UP or key == ord('k'):
                if scroll_pos > 0:
                    scroll_pos -= 1
        except Exception:
            pass

def main():
    tasks = load_tasks()
    curses.wrapper(draw_board, tasks)

if __name__ == "__main__":
    main()
