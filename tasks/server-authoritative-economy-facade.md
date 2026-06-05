---
title: "Server-Authoritative Economy Facade"
id: "018"
status: done
priority: 01
sprint: alpha
category: ECONOMY
description: "Move all economy/wallet mutations from client RPC to server-side authority. Remove client-side price submissions."
---
## Background / Context

The economy system previously allowed client-side RPCs to pass price arguments to the server, which could potentially be exploited by spoofing prices or artificially increasing wallet balances. This required a migration to a fully server-authoritative model where all pricing and catalog checks are executed exclusively on the server.

## Technical Design & Implementation

- `server/nakama/lua/economy.lua` relies on a hardcoded, authoritative `SHOP_CATALOG_DEFS` table to calculate item costs on the server without any client input.
- The server utilizes `nk.wallet_update(..., true)` to perform atomic wallet updates, ensuring users cannot spend more currency than they possess. If funds are insufficient, a `NotEnoughFunds` error is correctly thrown and caught.
- `scripts/managers/user_profile_manager.gd` has been updated to use safe RPC endpoints (`purchase_item`, `buy_currency`), sending only the `item_id` and relying on the server to acknowledge the result.
## Acceptance Criteria

- [x] Remove raw client.rpc_async calls for purchasing/spending that pass prices/items from client
- [x] Implement server-side RPC (e.g., purchase_item) that reads item cost from authoritative catalog/storage
- [x] Ensure server validates wallet balance before deducting and awarding items
- [x] Update UI to call new safe RPCs and await server acknowledgment
## Files Modified

- `server/nakama/lua/economy.lua` — Authoritative purchase logic and wallet mutation
- `scripts/managers/user_profile_manager.gd` — Updated client purchase flow to use safe RPCs
## References

- Nakama Wallet Update Documentation
- Server-Authoritative Game Design Principles
