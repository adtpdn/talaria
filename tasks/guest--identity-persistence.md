---
title: "Guest & Identity Persistence"
id: "037"
status: "progress"
priority: 01
sprint: alpha
category: SECURITY
description: "Implement a secure flow for binding Guest accounts to persistent identities (Steam, Google, Apple) without data loss."
modified: "2026-06-03"
---

# Guest & Identity Persistence

## Problem
Players starting as guests (via Device ID) risk losing progress if they change devices or clear app cache. Without a way to link guest progress to a persistent identity, user retention is impacted. Additionally, handling account conflicts (e.g., linking a guest to a Steam account that already has progress) requires careful mediation.

## Solution
Implement a "Bind Identity" workflow using Nakama's account linking system.

### Implementation Path
1. **Guest Onboarding:** Establish a default Guest login path using the device's unique identifier.
2. **Linking Interface:** Create a UI flow in the Settings/Profile panel to link accounts to Steam, Google, or Apple.
3. **Identity Merging:** Use Nakama linking RPCs to merge the guest profile with the persistent identity, prioritizing progress retention.
4. **Conflict Resolution:** Implement a "Conflict Resolution" dialog when the target identity is already linked, allowing the user to choose which progress to keep.

## Benefits
- **Higher Retention:** Users are more likely to commit if progress is backed up to a persistent account.
- **Cross-Platform Access:** Allows players to move from mobile (Guest) to PC (Steam) without starting over.
- **Security:** Reduces reliance on fragile device IDs for long-term identity management.

## Acceptance Criteria
- **Seamless Transition:** Verify a guest user can link to a Steam account and retain all XP, currency, and items.
- **Linkage Verification:** Confirm the UI correctly reflects the linked status (e.g., "Linked to Steam").
- **Conflict Handling:** Verify that linking to an already-taken identity triggers a resolution prompt instead of an automatic overwrite.
- **Identity Upgrade:** Confirm that after linking, the user is automatically logged in via the persistent identity.
- **API Integrity:** Verify `link_steam` (etc.) RPCs are called with correct parameters and errors are handled.

## Migration Checklist
- [ ] Implement Device ID login as the primary Guest path in `auth_manager.gd`.
- [ ] Build the "Link Account" UI in the Settings panel.
- [ ] Integrate Nakama's linking RPCs into the `AuthManager`.
- [ ] Implement the conflict resolution dialog and backend handling.
- [ ] Test the end-to-end flow: Guest Login $\rightarrow$ Progress $\rightarrow$ Link $\rightarrow$ Verify.
