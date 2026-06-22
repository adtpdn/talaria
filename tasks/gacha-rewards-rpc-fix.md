---
title: "Fix Gacha Pull and Daily Rewards RPC Parsing"
id: "103"
status: done
priority: 01
sprint: beta
category: BUG
description: "Gacha pull results were returning empty and daily reward claims were failing due to BackendService RPC payload parsing bug."
modified: "2026-06-22"
---
### Goal / Risk

Gacha pulls and daily reward operations were silently failing because `BackendService.api_rpc_async` did not provide parsed `"data"` dictionaries, causing the results to be ignored.

### Solution

- Fixed by the global `BackendService.api_rpc_async` JSON parse update (id: 102). Gacha and Daily Reward systems now correctly receive and display response data.

### Acceptance Criteria

- [x] Gacha pull completes and shows results (items, pity counter).
- [x] Daily reward claim succeeds and reflects in wallet.
