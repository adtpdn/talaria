---
title: "Fix Shop Purchase and Mail RPC Parsing"
id: "104"
status: done
priority: 01
sprint: beta
category: BUG
description: "Shop item purchases and mail operations were broken because BackendService RPC responses were not parsed into dictionaries."
modified: "2026-06-22"
---
### Goal / Risk

Purchasing items from the shop and claiming/deleting mail were failing silently. The wallet wasn't updating after purchases, and mail actions appeared to do nothing.

### Solution

- Fixed by the global `BackendService.api_rpc_async` JSON parse update (id: 102). All wallet, inventory, and mail operations now correctly process server responses.

### Acceptance Criteria

- [x] Shop purchase deducts currency and adds item to inventory.
- [x] Mail claim reward applies to wallet.
- [x] Mail delete removes the mail entry.
