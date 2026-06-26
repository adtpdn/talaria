---
id: "108"
title: "Admin Chat Storage Load More and Delete"
status: done
priority: 1
sprint: beta
category: CLIENT
description: "Fix Admin Chat Storage loading for social_global and add cursor pagination plus multi-select deletion."
modified: 2026-06-23
---

### Goal / Risk

Fix Admin Panel Chat Storage so admins can list `social_global` history, page through messages, and delete multiple selected rows.

### Solution

- Renamed the lower Chat Storage refresh button to `Load More`.
- Made the top refresh reload the current tab while `Load More` fetches the next cursor page.
- Added `social_global` resolution via active lobby channel or socket join.
- Added fallback to direct Nakama `list_channel_messages_async` when the admin RPC returns an empty dictionary.
- Normalized direct Nakama `ApiChannelMessage` objects into dictionaries before adding table rows.
- Added checkbox multiselect support and bulk delete for selected chat messages.
- Kept selected-row delete fallback when no checkbox is checked.

### Files Modified

- `scenes/ui/admin_panel.tscn`
- `scripts/ui/admin_panel.gd`
- `server/nakama/lua/admin.lua`

### Verification

- Confirmed with Godot MCP that `2...social_global` contains stored messages.
- Ran `godot --headless --path "/home/beng/Godot/Projects/tekton-enet" --check-only --quit`.

### Acceptance Criteria

- [x] `social_global` loads stored lobby chat messages.
- [x] Direct Nakama message objects render in the Chat Storage table.
- [x] `Load More` uses cursor pagination instead of full reload.
- [x] Admin can delete one or multiple selected chat messages.
