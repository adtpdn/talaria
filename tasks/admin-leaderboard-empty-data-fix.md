---
id: "109"
title: "Admin Leaderboard Empty Data Fix"
status: done
priority: 1
sprint: beta
category: CLIENT
description: "Fix Admin Leaderboards tab when leaderboard RPC returns empty or dictionary-shaped data."
modified: 2026-06-23
---

### Goal / Risk

Fix Admin Panel Leaderboards tab showing no data when the server RPC returns leaderboard data as a dictionary or an empty object.

### Solution

- Added client-side type handling for leaderboard responses returned as either `Array` or `Dictionary`.
- Added native Nakama leaderboard fallback in Admin Panel when `get_leaderboard_stats` returns empty data.
- Fixed Lua RPC iteration from `ipairs` to `pairs` for native leaderboard records.

### Files Modified

- `scripts/ui/admin_panel.gd`
- `server/nakama/lua/leaderboard.lua`

### Verification

- Confirmed `get_leaderboard_stats` returned `leaderboard: {}` via MCP before fix.
- Ran `godot --headless --path "/home/beng/Godot/Projects/tekton-enet" --check-only --quit`.

### Acceptance Criteria

- [x] Leaderboard response accepts both array and dictionary shapes.
- [x] Admin Panel falls back to native Nakama leaderboard records.
- [x] Lua RPC can iterate map-shaped leaderboard records after Nakama restart.
