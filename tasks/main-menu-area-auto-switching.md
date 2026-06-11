---
title: "Main Menu Area Auto-Switching"
id: "087"
status: done
priority: 02
sprint: beta
category: UI
description: "Fixed lobby area selector to visually update when game mode changes."
modified: "2026-06-11"
---
### Goal / Risk

When selecting a game mode in the lobby, the internal area changed but the UI label didn't update to show it.

### Solution

- lobby_manager.gd — set_game_mode() and sync_game_mode() now force-switch the area when invalid.
- lobby_room.gd — _on_game_mode_changed() now immediately updates area_name_label.text to reflect the auto-switched area. Added _sync_room_profile_card() on area change.
