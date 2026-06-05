---
title: "Implement Comprehensive Error Handling"
id: "001"
status: "done"
priority: 01
sprint: alpha
category: CORE
description: "Establish a unified error classification and recovery system for all asynchronous operations, including retries and user notifications."
modified: "2026-06-03"
---

# Implement Comprehensive Error Handling

## Problem
Asynchronous operations currently lack a standardized error handling strategy, leading to:
1. **Silent Failures:** Operations like `get_account_async` return empty dictionaries on failure, leaving the UI inconsistent.
2. **Generic Feedback:** Users receive vague "Failed to connect" messages instead of specific reasons (timeout vs. expired session).
3. **Lack of Resilience:** Transient network glitches cause immediate failure instead of attempting a retry.
4. **Developer Friction:** Inconsistent error checking across managers leads to bloated code and missed edge cases.

## Solution
Implement a centralized `ErrorHandler` system that classifies errors, manages retries, and dictates the UI response.

### Implementation Details
1. **Error Classification:** Create a `GameError` object with `ErrorType` (e.g., `NETWORK_TIMEOUT`, `AUTH_EXPIRED`) and `ErrorSeverity` (INFO, WARNING, ERROR, CRITICAL).
2. **Retry Orchestrator:** Implement a `retry_async_operation` wrapper using a configurable policy (e.g., 3 attempts with exponential backoff).
3. **Unified UI Response:** Map severity to UI components:
    - `INFO` $\rightarrow$ Toast.
    - `WARNING` $\rightarrow$ Banner.
    - `ERROR` $\rightarrow$ Modal Dialog with "Retry".
    - `CRITICAL` $\rightarrow$ Full-screen Error Overlay.
4. **Standardized Return Shape:** Enforce a return pattern: `{"success": bool, "error": GameError, "data": mixed}`.

## Benefits
- **Increased Reliability:** Transient network issues are resolved automatically.
- **Improved UX:** Users receive clear, actionable instructions instead of generic errors.
- **Cleaner Codebase:** Boilerplate error checking is moved from managers to the `ErrorHandler` facade.
- **Better Observability:** Centralized handling allows for easy logging of production failures.

## Acceptance Criteria
- **System Integrity:** Verify `ErrorHandler` singleton is accessible globally and all `ErrorType`s have default messages.
- **Retry Logic Validation:** Simulate `NETWORK_TIMEOUT` and verify the operation retries exactly the configured number of times.
- **UI Responsiveness:** Trigger different severity levels and verify the correct UI component appears.
- **Refactor Coverage:** Verify `AuthManager`, `UserProfileManager`, `GachaManager`, and `NakamaManager` route failures through `ErrorHandler`.
- **Offline Handling:** Verify total connectivity loss triggers a `CRITICAL` error and redirects to a "Connection Lost" screen.

## Migration Checklist
- [ ] Implement `scripts/utils/error_handler.gd` with `GameError` and `ErrorType` definitions.
- [ ] Implement the `retry_async_operation` wrapper logic.
- [ ] Create the UI components for Toasts, Banners, and Error Dialogs.
- [ ] Refactor `auth_manager.gd` to use the new error handling for socket and login flows.
- [ ] Refactor `user_profile_manager.gd` and `gacha_manager.gd` async calls.
- [ ] Integrate `ErrorHandler` with `AnalyticsService` to log `ERROR` and `CRITICAL` events.
- [ ] Write unit tests for retry logic and error classification.
