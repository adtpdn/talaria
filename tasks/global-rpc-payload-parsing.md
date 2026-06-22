---
title: "Fix Global RPC JSON Payload Parsing"
id: "102"
status: done
priority: 01
sprint: beta
category: CORE
description: "Fixed critical BackendService bug where RPC responses were returned as raw strings instead of parsed dictionaries."
modified: "2026-06-22"
---
### Goal / Risk
All systems relying on Nakama RPCs (Admin Panel, Leaderboards, Gacha, Mail) were failing silently. `BackendService.api_rpc_async` was returning the raw JSON string under `"payload"`, while consumers expected a parsed dictionary under `"data"`.

### Solution
- Updated `BackendService.api_rpc_async` to perform `JSON.parse_string(result.payload)` and return the output via the `"data"` key.
- Restored Admin Panel `_rpc` helper to use standard `result.get("data")` flow.
- Added auto-resolution for `"social_global"` to channel IDs inside the Admin Panel to easily query lobby chat.
