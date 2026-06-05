---
title: "Implement Proactive Session Management"
id: "010"
status: "progress"
priority: 01
sprint: alpha
category: SECURITY
description: "Transition from reactive to proactive session refresh to prevent mid-game disconnects and unnecessary re-logins."
modified: "2026-06-03"
---

# Implement Proactive Session Management

## Problem
The current session refresh logic is reactive: it only attempts to refresh the token *after* the session has already expired. This leads to gameplay interruptions, fragile recovery from network glitches, and a lack of resilience in session health monitoring.

## Solution
Implement a dedicated `SessionManager` that proactively monitors session expiry and handles renewals in the background.

### Technical Implementation
1. **Proactive Refresh Timer:** Implement a background timer checking every 60s; trigger refresh when the session is within 5 minutes (`REFRESH_BEFORE_EXPIRY`) of expiration.
2. **Background Renewal:** Perform `session_refresh_async` silently, updating `NakamaManager.session` without interrupting the game loop.
3. **Exponential Backoff Retry:** In case of failure, implement a retry loop (3 attempts: 1s, 2s, 4s delay) to resolve transient issues.
4. **Graceful Expiry Handling:** If all retries fail or the session expires completely, trigger a `session_expired` signal and present a `ReloginDialog`.

## Benefits
- **Zero Interruption:** Players remain authenticated without seeing "Session Expired" messages mid-game.
- **Increased Stability:** Automated retries handle most network-related authentication hiccups silently.
- **Enhanced UX:** Re-login becomes a last resort rather than a common occurrence.

## Acceptance Criteria
- **Proactive Trigger:** Verify the session refreshes automatically when time until expiry drops below 300 seconds.
- **Silent Update:** Confirm `NakamaManager.session` updates in the background without kicking the user to the login screen.
- **Retry Resilience:** Simulate a network outage during refresh and verify recovery via exponential backoff.
- **Expiry Flow:** Verify that once a session is truly expired, the `ReloginDialog` appears and redirects the user to `login_screen.tscn`.
- **Signal Integrity:** Confirm `session_refreshed` and `session_expired` signals are emitted correctly.

## Migration Checklist
- [ ] Implement `scripts/managers/session_manager.gd` as an autoload singleton.
- [ ] Integrate the session check timer and `_refresh_session()` logic.
- [ ] Implement the `_retry_refresh()` method with exponential backoff.
- [ ] Create the `scenes/ui/relogin_dialog.tscn` and its corresponding script.
- [ ] Connect `SessionManager` to `AuthManager` to save tokens to disk after each refresh.
- [ ] Test the flow by manually shortening session expiry in a debug build.
