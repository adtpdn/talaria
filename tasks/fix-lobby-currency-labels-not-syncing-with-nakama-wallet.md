---
title: "Fix Lobby Currency Sync"
id: "064"
status: progress
priority: 01
sprint: alpha
category: CLIENT
description: "Synchronize Username, GoldLabel, and StarLabel in lobby ProfileCards with real-time Nakama wallet values."
assignee: "dev"
cron_job: "pending"
---

# Fix Lobby Currency Sync

## Problem
The `ProfileCard` UI in `lobby.tscn` was displaying stale or default currency values. The `Username`, `GoldLabel`, and `StarLabel` did not update when the user's wallet changed on the server, leading to a disconnect between the UI and the actual account balance.

## Solution
Implement a reactive synchronization loop between `UserProfileManager` and the `ProfileCard` UI components.

### Implementation Path
1. **Update Sync Logic:** Modify `_sync_room_profile_card()` to pull current wallet values from `UserProfileManager.wallet` instead of relying on initial load data.
2. **Event-Driven Updates:** Connect the `ProfileCard` update logic to the `profile_loaded` and `profile_updated` signals in `UserProfileManager`.
3. **Label Binding:** Ensure that every time a profile is synced or updated, the corresponding labels in the UI are explicitly refreshed.

## Benefits
- **Data Accuracy:** Players see their real-time balance, reducing confusion and support tickets.
- **UI Responsiveness:** Currency updates (e.g., after a purchase) are reflected instantly in the lobby without requiring a scene reload.

## Acceptance Criteria
- **Real-time Sync:** Changing a user's currency value in the Nakama console results in an automatic update of the `GoldLabel` and `StarLabel` in the lobby UI.
- **Initialization Accuracy:** Upon joining a room, the `ProfileCard` correctly displays the current wallet values for all players.
- **Signal Verification:** Verify that firing the `profile_updated` signal in `UserProfileManager` triggers an immediate UI refresh on the `ProfileCard`.
- **Edge Case Handling:** Confirm that labels handle empty or null wallet values gracefully (e.g., displaying "0").

## Migration Checklist
- [x] Update `_sync_room_profile_card()` in `lobby.gd` to read from `UserProfileManager.wallet`.
- [x] Connect `UserProfileManager.profile_loaded` signal to the UI update method.
- [x] Connect `UserProfileManager.profile_updated` signal to the UI update method.
- [x] Verify that labels are updated for both the local player and other room members.
- [x] Test with multiple currency types (Gold, Stars) to ensure no cross-contamination.
