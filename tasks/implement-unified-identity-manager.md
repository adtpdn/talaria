---
title: "Implement Unified Identity Manager"
id: "003"
status: todo
priority: 01
sprint: alpha
category: SECURITY
description: "Implement a unified identity manager with platform-specific auth routing (Steam/Google/Apple/TapTap) and automatic platform detection."
---

# Implement Unified Identity Manager

## Problem
The game lacks a centralized system to handle authentication across platforms. Without automatic detection and routing, users are forced into manual selection. Specifically, there is no integration for TapTap (China market) and no mechanism for cross-platform account linking.

## Solution
Implement a `UnifiedIdentityManager` that detects the platform at runtime and routes users to the appropriate Nakama authentication method.

### Technical Implementation
1. **Platform Detection:** Use `OS.has_feature()` to detect `STEAM_PC`, `GOOGLE_ANDROID`, `APPLE_IOS`, `WEB`, etc.
2. **Regional Routing:** Use `OS.get_locale()` to route Android users in China to TapTap instead of Google Play.
3. **Authentication Routing:**
    - **Steam:** Use `authenticate_steam` via `SteamworksManager` tickets.
    - **Google/Apple:** Use `authenticate_google`/`authenticate_apple` via ID tokens.
    - **TapTap:** Use `authenticate_custom` via TapTap tokens.
    - **Fallback:** Use `authenticate_device` via `OS.get_unique_id()`.
4. **Account Linking:** Implement `link_account()` to associate multiple identities with one Nakama account.

## Benefits
- **Seamless Onboarding:** Users are automatically logged in via their native platform.
- **Market Reach:** Enables official deployment on TapTap.
- **User Retention:** Cross-platform linking allows seamless device switching.
- **Robustness:** Device-ID fallback ensures accessibility if native auth fails.

## Acceptance Criteria
- **Detection Accuracy:** Verify the manager identifies the correct platform on startup.
- **Auth Flow Success:** Verify successful authentication for Steam, Android (incl. TapTap), and iOS.
- **Fallback Logic:** Verify successful fallback to Device ID when native auth is unavailable.
- **Linking Verification:** Verify a user can link a secondary account to their primary identity.

## Migration Checklist
- [ ] Create `scripts/managers/unified_identity_manager.gd`.
- [ ] Implement `_detect_platform()` with feature and locale checks.
- [ ] Implement platform-specific auth methods (`_auth_steam`, `_auth_google`, etc.).
- [ ] Implement `_auth_device_fallback`.
- [ ] Integrate `UnifiedIdentityManager` into `main.gd` startup.
- [ ] Implement `link_account` logic.
- [ ] Test the full flow on Steam, Android, and iOS.
