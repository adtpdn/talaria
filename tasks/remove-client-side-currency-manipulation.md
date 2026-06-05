---
title: "Remove Client-Side Currency Manipulation"
id: "006"
status: done
priority: 01
sprint: alpha
category: ECONOMY
description: "gacha_manager.gd and gacha_panel.gd directly modify wallet balances client-side. This allows cheating and must be moved to server-side validation."
---
## Problem

File: scripts/managers/gacha_manager.gd line 45

```javascript
UserProfileManager.wallet[currency] = bal - cost
```

File: scripts/ui/gacha_panel.gd lines 85-87

```javascript
UserProfileManager.wallet["star"] = 3200
UserProfileManager.wallet["gold"] = 1500
```

Currency balances are modified directly on the client without server validation. This is a critical economy vulnerability:

- Players can modify memory to get infinite currency
- No server-side transaction logging
- No fraud detection possible
- Violates app store policies
## Solution

1. Create server-side RPC function perform_gacha_pull
1. Server validates currency balance
1. Server deducts currency and grants items
1. Server returns results to client
1. Client only displays results, never modifies wallet
## Server Implementation (Nakama)

```typescript
// server/modules/gacha.ts
function performGachaPull(ctx: nkruntime.Context, logger: nkruntime.Logger, nk: nkruntime.Nakama, payload: string): string {
  const request = JSON.parse(payload);
  const userId = ctx.userId;
  
  // Read wallet from Nakama wallet system
  const wallet = nk.walletRead(userId);
  const currency = request.currency;
  const cost = request.cost;
  
  if (wallet[currency] < cost) {
    throw new Error('Insufficient currency');
  }
  
  // Deduct currency
  const changeset = {};
  changeset[currency] = -cost;
  nk.walletUpdate(userId, changeset, {}, true);
  
  // Perform gacha logic server-side
  const results = rollGacha(request.banner_id, request.count);
  
  // Grant items
  grantItems(userId, results);
  
  return JSON.stringify({success: true, results: results});
}
```

## Client Changes

```javascript
func pull(banner_id: String, count: int) -> Array:
    var payload = JSON.stringify({
        "banner_id": banner_id,
        "count": count
    })
    
    var result = await NakamaManager.client.rpc_async(
        NakamaManager.session,
        "perform_gacha_pull",
        payload
    )
    
    if result.is_exception():
        push_error("Gacha pull failed: " + result.get_exception().message)
        return []
    
    var data = JSON.parse_string(result.payload)
    return data.get("results", [])
```

## Acceptance Criteria

- [ ] All currency modifications happen server-side
- [ ] Client cannot modify wallet directly
- [ ] Server validates all transactions
- [ ] Transaction logging implemented
- [ ] Tested with memory editors (cheat detection)
- [ ] Remove debug currency grants from gacha_panel.gd
