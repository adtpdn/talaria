---
id: "107"
title: "Admin Panel Header Refresh Counts"
status: done
priority: 2
sprint: beta
category: CLIENT
description: "Make Admin Panel header Refresh and CountLabel behave consistently across every tab."
modified: 2026-06-23
---

### Goal / Risk

Make the top Admin Panel `RefreshBtn` and `CountLabel` correctly apply to every tab instead of only some tab data views.

### Solution

- Routed the top refresh button through the active tab loader.
- Added missing count updates for Announcements and Daily Rewards.
- Added Lobby Chat count/status text.
- Kept existing count behavior for Users, Leaderboards, Mail Manager, Shop, and Chat Storage.

### Files Modified

- `scripts/ui/admin_panel.gd`

### Verification

- Ran `godot --headless --path "/home/beng/Godot/Projects/tekton-enet" --check-only --quit`.

### Acceptance Criteria

- [x] Top Refresh reloads the current Admin Panel tab.
- [x] CountLabel updates for all tabs.
- [x] Admin Panel script compiles without parse errors.
