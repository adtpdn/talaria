---
title: "Implement Server-Side IAP Receipt Validation"
id: "007"
status: done
priority: 01
sprint: alpha
category: NETWORKING
description: "Implement server-to-server receipt validation with Steam/Google/Apple APIs to prevent IAP fraud."
---

# Implement Server-Side IAP Receipt Validation

## Problem
The project currently lacks server-side receipt validation. Without the 4-step async verification topology (Client $\rightarrow$ Platform $\rightarrow$ Server $\rightarrow$ Grant), the system is vulnerable to fake receipts, refund fraud, and violates app store requirements, leading to potential revenue loss.

## Solution
Implement the complete IAP validation flow as documented in the Monetization Architecture.

### Technical Implementation
1. **Server-Side Validation:** Implement a `validatePurchase` function in Nakama Lua that routes receipts to the respective platform APIs:
    - **Steam:** POST to `ISteamMicroTxn/FinalizeTxn/v2`.
    - **Google:** POST to Google Play Developer API.
    - **Apple:** POST to `verifyReceipt`.
2. **Idempotency:** Use a `transactions` storage collection to store `transactionId` and prevent duplicate grants.
3. **Client-Side Integration:** Implement `ShopManager.purchase_item()` to:
    - Get the signed receipt from the platform SDK.
    - Send the receipt to the server via the `validate_purchase` RPC.
    - Grant items only upon server confirmation.

## Benefits
- **Fraud Prevention:** Eliminates the ability to spoof purchases or exploit refund loopholes.
- **Store Compliance:** Meets the mandatory security requirements for the App Store and Google Play.
- **Reliable Granting:** Ensures items are only granted after successful financial confirmation.

## Acceptance Criteria
- **Validation Success:** Verify server-side receipt validation for Steam, Google Play, and Apple.
- **Deduplication:** Confirm that submitting the same receipt twice does not grant items twice.
- **Logging:** Verify every transaction is logged in the database.
- **Client-Side Security:** Confirm the client never grants items directly without server validation.
- **Error Handling:** Verify that network failures during validation are handled via retry logic.

## Migration Checklist
- [x] Implement `validatePurchase` and platform-specific validators in Nakama Lua.
- [x] Set up the `transactions` storage collection for idempotency.
- [x] Implement `ShopManager.purchase_item()` in GDScript.
- [x] Integrate platform SDKs for receipt retrieval.
- [x] Test end-to-end purchase flow on all three platforms.
- [x] Implement refund webhook listeners.
