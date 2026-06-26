---
id: "110"
title: "Admin User Detail Management"
status: done
priority: 1
sprint: beta
category: ADMIN
description: "Expand Admin Users tab with account editing and detailed user inspection for friends, purchases, subscriptions, and storage."
modified: 2026-06-23
---

### Goal / Risk

Expand Admin Panel Users tab so admins can inspect and manage a selected account beyond role/ban state.

### Solution

- Added `admin_get_user_detail` RPC for account info, friends, receipts, wallet ledger, subscription metadata, and known storage collections.
- Added `admin_update_user_identity` RPC for username and display name updates.
- Added `admin_set_user_password` RPC for email-account password updates when supported by Nakama runtime.
- Expanded the Edit User dialog with username, display name, email status display, password field, role, and ban controls.
- Expanded the History dialog into a richer user detail view with account, friends, purchases, logins, wallet ledger, matches, and storage sections.

### Files Modified

- `scripts/ui/admin_panel.gd`
- `server/nakama/lua/admin.lua`

### Verification

- Ran `godot --headless --path "/home/beng/Godot/Projects/tekton-enet" --check-only --quit`.

### Acceptance Criteria

- [x] Admin can view detailed account information for one selected user.
- [x] Admin can edit username and display name from the Users tab.
- [x] Admin can request password update for email-backed accounts.
- [x] Admin can inspect friends, purchase receipts, wallet ledger, subscription metadata, and known storage collections.

### Notes

- New Lua RPCs require a Nakama server restart before they are available.
- Email verified status depends on fields exposed by the running Nakama account object.
