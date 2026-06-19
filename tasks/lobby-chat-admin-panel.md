---
title: "Lobby Chat Admin Panel (Config + Wipe + Purge)"
id: "099"
status: done
priority: 02
sprint: beta
category: ADMIN
description: "Add Lobby Chat admin tab with system prefix, max messages, wipe, purge old, save config."
modified: "2026-06-19"
---
### Goal / Risk

Admin panel had no controls for lobby chat management. Admins needed system prefix, message limit, bulk wipe, and age-based purge.

### Solution

- Added 3 backend RPCs: admin_get_chat_config, admin_set_chat_config, admin_purge_old_messages
- New Lobby Chat tab (index 6) in admin_panel.tscn with all controls
- Bridge methods in lobby.gd: admin_wipe_chat(), admin_purge_chat()
- lobby_chat.gd fetches config on join, applies max_messages and prefix

### Acceptance Criteria

- [x] Lobby Chat tab visible at index 6 in admin panel
- [x] System prefix field saved to and loaded from Nakama storage
- [x] Max messages spinner controls history fetch limit
- [x] Wipe Chat button deletes all messages
- [x] Purge Old button deletes messages older than N days
- [x] Save Config persists to config/lobby_chat in Nakama storage
