---
title: "Admin Panel: JSON Type Safety & User History View"
id: "042"
status: done
priority: 01
sprint: beta
category: CLIENT
description: "Fix JSON type mismatch crashes ({}) and implement the User History audit view in the Admin Panel."
---

# Admin Panel: JSON Type Safety & User History View

## Problem
The Admin Panel encountered two critical failures:
1. **Runtime Crashes:** Nakama's Lua backend serializes empty arrays as JSON objects (`{}`) instead of arrays (`[]`). Godot's strictly typed `Array` variables crashed when assigned these objects, causing total UI failure.
2. **Audit Blindness:** Admins lacked a frontend interface to view user-specific audit trails (logins, wallet ledger, match records), despite the backend RPC (`admin_get_user_history`) being available.

## Solution
Implement a safe type-casting pattern for all server responses and build a dedicated History modal in the Admin Panel.

### Technical Implementation
1. **Safe Casting:** Replace direct assignments with conditional checks: `var records: Array = raw if raw is Array else []`.
2. **UI Integration:** Add a "HISTORY" button to the `UserActionBar` in `admin_panel.tscn`.
3. **Audit Modal:** Create a `HistoryDialog` (AcceptDialog) with a `ScrollContainer` and `RichTextLabel`.
4. **RPC Integration:** Implement `_on_history_pressed()` to fetch and format data via `admin_get_user_history`.

## Benefits
- **Stability:** Eliminates critical crashes during empty-state transitions.
- **Observability:** Provides admins direct access to user behavior and financial audit trails.
- **UX:** Implements proper error handling for invalid user selection (0 or 2+ users).

## Acceptance Criteria
- **Empty-State Stability:** Verify that Users, Leaderboards, Mail, and Banners tabs load correctly when the server returns `{}`.
- **Audit UI Flow:** Confirm "HISTORY" button is visible and opens the `HistoryDialog` when exactly one user is selected.
- **Data Accuracy:** Verify that the `HistoryDialog` correctly displays Logins, Wallet Ledger, and Match History sections.
- **RPC Reliability:** Confirm that RPC failures are caught and displayed via the status bar as "Failed: [error]".

## Migration Checklist
- [x] Audit `scripts/ui/admin_panel.gd` for `result.get(..., [])` calls and apply safe casts.
- [x] Add `HistoryBtn` to `scenes/ui/admin_panel.tscn` within the `UserActionBar` node.
- [x] Add `HistoryDialog` and `RichTextLabel` to the root of `scenes/ui/admin_panel.tscn`.
- [x] Implement the `_on_history_pressed()` handler in `scripts/ui/admin_panel.gd`.
- [x] Connect the `pressed` signal of `HistoryBtn` to the handler method.
- [x] Test with large history data to verify `ScrollContainer` functionality.
