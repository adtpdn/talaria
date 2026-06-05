---
title: "Shop & Receipt Validations"
id: "040"
status: done
priority: 01
sprint: alpha
category: ECONOMY
description: "Integrate shop UI with server-side IAP validation - remove client-side granting logic and ensure all purchases flow through backend validation."
---
### Goal / Risk

Move IAP receipt verification to Nakama IAP module. Prevent client-spoofed receipt unlocks.

### Files / Areas

server/modules/iap.ts, shop_manager.gd

### Execution Checklist

- [ ] Disable/remove client-side IAP granting logic.
- [ ] Implement Nakama Apple/Google/Steam receipt validation endpoints.
- [ ] Ensure server grants items ONLY after receiving valid receipt payload from provider.
### AI Execution Prompt

```plain text
Implement server-side receipt validation for IAPs. Review scripts/managers/shop_manager.gd and server/modules/iap.ts. Remove client-side item granting for real-money purchases. Set up Nakama IAP hooks to accept Apple/Google/Steam receipts, validate them against the provider endpoints, and grant the authoritative inventory/wallet payload only upon successful validation. Acceptance: client cannot grant itself premium currency by mocking success callbacks; all IAP flows require a provider-validated receipt token.
```

### Testing / Auto-Check

AI AUTO-CHECK: Submit invalid/dummy receipt token from client. Assert server rejects with 4xx error and grants no premium currency.

### MS Teams Daily Report

```plain text
**Completed [PRD-P0-2]: Shop & Receipt Validations**\n- **Goal:** Move IAP receipt verification to Nakama IAP module. Prevent client-spoofed receipt unlocks.\n- **Status:** Integrated & verified. Code changes applied to: server/modules/iap.ts, shop_manager.gd
```
