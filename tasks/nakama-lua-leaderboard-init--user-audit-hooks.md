---
title: "Nakama Lua: Leaderboard Init & User Audit Hooks"
id: "043"
status: done
priority: 01
sprint: alpha
category: BACKEND
description: "Implement auto-init for leaderboards and user audit tracking hooks in Nakama Lua."
---

# Nakama Lua: Leaderboard Init & User Audit Hooks

## Problem
Two critical gaps existed in the modular Lua backend:
1. **Leaderboard Initialization:** The `global_high_score` leaderboard was not initialized on startup, causing the Admin Panel's Leaderboard tab to appear empty.
2. **Audit Blindness:** No mechanism existed to track user login history or aggregate wallet/match data for administrative auditing.

## Solution
Initialize leaderboards via `pcall` on module load and implement `afterAuthenticate` hooks for metadata tracking.

### Technical Implementation
1. **Auto-Initialization:** Implement a `pcall` check in `leaderboard.lua` to create the `global_high_score` leaderboard if it doesn't exist.
2. **Login Tracking:** Use the `afterAuthenticate` hook in `user.lua` to write login metadata (timestamp, IP) to a `history` storage collection.
3. **Audit RPC:** Implement the `admin_get_user_history` RPC to aggregate wallet ledger, login history, and match records for a specific user.
4. **Access Control:** Enforce admin-only access to the history RPC using `utils.require_admin(ctx)`.

## Benefits
- **Immediate Availability:** Leaderboards are ready upon server start without manual intervention.
- **Accountability:** Detailed audit trails allow admins to track suspicious login patterns or wallet anomalies.
- **Centralized Audit:** Single RPC providing a comprehensive view of user history.

## Acceptance Criteria
- **Auto-Creation:** Verify `global_high_score` is created on server startup.
- **History Logging:** Confirm login history (timestamp + IP) is written to storage after every authentication.
- **RPC Functionality:** Verify `admin_get_user_history` returns correct wallet, login, and match data.
- **Security:** Confirm non-admin users receive a permission error when calling the history RPC.

## Migration Checklist
- [x] Implement `pcall` leaderboard creation in `server/nakama/lua/leaderboard.lua`.
- [x] Register `afterAuthenticate` hooks in `server/nakama/lua/user.lua`.
- [x] Implement the `admin_get_user_history` RPC in `server/nakama/lua/user.lua`.
- [x] Add `utils.require_admin` check to the history RPC.
- [x] Verify all changes in the `main.lua` module entrypoint.
