---
title: "Auth & Secrets Lockdown"
id: "034"
status: done
priority: 01
sprint: alpha
category: SECURITY
description: "Remove insecure Steam ticket fallbacks, block raw client account creation, and lock API keys."
---

# Auth & Secrets Lockdown

## Problem
The authentication system contained several "debug" and "fallback" paths that created significant security vulnerabilities:
1. **Steam Fallbacks:** Insecure paths allowed authentication without valid tickets, potentially allowing identity spoofing.
2. **Raw Account Creation:** The client could request account creation directly, bypassing server-side validation.
3. **Secret Exposure:** Production API keys were occasionally bundled in client exports or stored as hardcoded strings.

## Solution
Implement a strict "Zero-Trust" authentication flow where every identity claim is validated server-side.

### Security Hardening
1. **Audit `auth_manager.gd`:** Remove all "mock" or "fallback" login paths that bypass Steam/Nakama ticket verification.
2. **Enforce Server-Side Auth:** Ensure clients cannot initiate account creation without a third-party verified token.
3. **Secrets Scrubbing:** Move all server-side keys to environment variables or secure Nakama config files; remove them from the Godot client bundle.
4. **Validation Loop:** Implement strict server-side validation for all login methods (Steam, Device, Custom).

## Benefits
- **Identity Integrity:** Prevents identity spoofing and account theft via token manipulation.
- **Production Readiness:** Ensures the client bundle is safe for distribution without leaking administrative keys.
- **Reduced Attack Surface:** Removes "backdoors" intended for local development.

## Acceptance Criteria
- **Zero-Fallback Policy:** Verify that `scripts/managers/auth_manager.gd` contains zero occurrences of "mock" or "fallback" in production paths.
- **Client-Side Secret Audit:** Perform a string search on the final exported production binary for known secrets; results must be empty.
- **Auth-Flow Validation:** Confirm a user cannot create an account via the client if the server requires a verified Steam account.
- **RPC Integrity:** Verify all authentication requests are routed through the official Nakama API.

## Migration Checklist
- [x] Audit `scripts/managers/auth_manager.gd` for insecure fallbacks.
- [x] Remove hardcoded production secrets from all client scripts.
- [x] Configure Nakama server to reject non-validated account creation requests.
- [x] Verify the production export bundle using a binary string search.
- [x] Test the login flow with an invalid Steam ticket to ensure server rejection.
