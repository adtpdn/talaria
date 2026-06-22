---
title: "Fix UI Overlap and Global RPC JSON Payload Parsing"
id: "101"
status: done
priority: 02
sprint: beta
category: BUG
description: "Fixed overlapping UI elements in FragmentCraftPanel and resolved a critical global issue where BackendService failed to parse JSON RPC payloads, breaking all Admin Panels, Leaderboards, Gacha, and Mail."
modified: "2026-06-22"
---
### Goal / Risk

FragmentCraftPanel UI elements were overlapping due to incorrect container settings. 
More critically, ALL systems relying on Nakama RPCs (Admin Panel, Gacha, Leaderboards, Mail) were completely broken because `BackendService.api_rpc_async` was returning the raw JSON string in the `"payload"` key, while every manager script expected a parsed Dictionary in the `"data"` key.

### Solution

- Reconfigured `CommonPanel`, `UncommonPanel`, and `RarePanel` to `PanelContainer` with `layout_mode = 2` to allow them to stretch naturally.
- Fixed missing UI node definition in `fragment_craft_panel.tscn`.
- Fixed `BackendService.api_rpc_async` to correctly parse `result.payload` with `JSON.parse_string()` and return the dictionary in the `"data"` key, instantly fixing all dependent systems across the game.
- Auto-resolve the `"social_global"` channel name to the actual Nakama `channel_id` directly in the Admin Panel Chat UI.

### Acceptance Criteria

- [x] Fragment craft UI panels stack correctly without overlapping.
- [x] `BackendService` correctly supplies parsed `"data"` objects to all managers.
- [x] Admin Panel successfully fetches and lists users without error.
- [x] Admin Panel successfully fetches and lists chat messages for "social_global".
- [x] Wipe chat and purge old chat buttons successfully resolve "social_global" ID.
- [x] Unnecessary tracking of AI cache folders (.claude, .agent) removed.
