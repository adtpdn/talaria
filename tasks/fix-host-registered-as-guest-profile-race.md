---
title: "Fix Host Registered as Guest (Profile Load Race)"
id: "093"
status: done
priority: 01
sprint: beta
category: CLIENT
description: "Logged-in host's player name registered as 'Guest' when hosting Freemode quickly, due to a race with async profile loading."
modified: "2026-06-18"
---

# Fix Host Registered as Guest (Profile Load Race)

## Problem
When a logged-in (non-guest) host started solo play and entered Freemode quickly, the `Name` Label3D on `player.tscn` registered with a guest name. Waiting a moment (or clicking through ready/play) gave the correct display name.

## Root Cause
`host_room()` sets `LobbyManager.local_player_name = UserProfileManager.get_display_name()`. That getter returned its `"Guest"` fallback whenever `is_profile_loaded` was still `false`. That flag only flips true at the **end** of `UserProfileManager.load_profile()`, which awaits a chain of Nakama calls (account → storage → inventory → stats → fragments). Acting before that chain finished hit the fallback.

## Solution
When the full profile isn't loaded yet, fall back to `AuthManager.current_user["display_name"]` instead of `"Guest"`. That field is populated synchronously inside `_load_user_profile()` **before** `auth_completed` fires, so the real name is available well before the rest of the profile. Degrades to `"Guest"` only when genuinely nothing is loaded.

## Files Modified
- scripts/managers/user_profile_manager.gd — `get_display_name()` falls back to `AuthManager.current_user["display_name"]` before the guest fallback.

## Acceptance Criteria
- [x] Logged-in user can host Freemode immediately and see their display name on the player label.
- [x] Still degrades to "Guest" only when no profile/auth data is loaded at all.
