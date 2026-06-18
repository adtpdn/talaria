---
title: "Fix 'Cannot create match when state is JOINING'"
id: "094"
status: done
priority: 01
sprint: beta
category: CLIENT
description: "Hosting a Nakama room twice (double-click on mode button) re-entered create_match() while the bridge was still JOINING, throwing an error and failing to host."
modified: "2026-06-18"
---

# Fix 'Cannot create match when state is JOINING'

## Problem
Hosting a Nakama room (e.g. clicking the Freemode/Stop n Go mode button) could throw:
`NakamaMultiplayerBridge.gd:70 @ create_match(): Cannot create match when state is JOINING`
and fail to create the match.

## Root Cause
`create_match()` rejects any call where `_match_state != DISCONNECTED`. The host flow is async with no re-entry guard:
1. Mode buttons had no guard — a double-click fired `host_room()` twice.
2. The 2nd pass hit `connect_to_nakama_async()`, which early-returns when the socket is already connected **without** rebuilding the bridge — reusing the bridge still stuck in `JOINING` from the first attempt.
3. `bridge.create_match()` on a `JOINING` bridge → error.

## Solution (defense in depth)
1. `NakamaManager.host_game()` — guard on bridge state: ignore if already `CONNECTED`; if stranded mid-`JOINING`, `await bridge.leave()` to reset to `DISCONNECTED` before creating. Removed dead `result.is_exception()` check (`create_match()` returns void).
2. `lobby_main_menu.gd host_room()` — `_is_hosting` re-entry flag; a 2nd press returns immediately while the first flow is in flight.
3. `lobby.gd` — declared `_is_hosting`; cleared on every terminal outcome: `room_joined`, `room_left`, `match_join_error`, `connection_failed`, and the synchronous LAN-failure path.

## Files Modified
- scripts/nakama_manager.gd — `host_game()` bridge-state guard + self-reset; removed dead exception check.
- scenes/ui/lobby_main_menu.gd — `host_room()` `_is_hosting` re-entry guard; reset on LAN failure.
- scenes/lobby.gd — `_is_hosting` flag + signal connections to clear it on host-flow completion/failure.

## Acceptance Criteria
- [x] Rapid double-click on a mode button no longer throws the JOINING error; match still creates cleanly.
- [x] A bridge stranded in JOINING self-heals on the next host attempt.
