---
title: "Implement Unified Backend Facade Pattern"
id: "002"
status: "done"
priority: 01
sprint: alpha
category: BACKEND
description: "Centralize direct Nakama client calls into a unified backend facade to improve testability and consistency."
modified: "2026-06-08"
---

# Implement Unified Backend Facade Pattern

## Problem
Direct Nakama client calls (`rpc_async`) are scattered across 20+ files (FriendManager, AdminPanel, UserProfileManager, etc.). This creates tight coupling to the Nakama SDK, makes mocking the backend for tests impossible, prevents centralized logging/metrics, and leads to inconsistent error handling across the app.

## Solution
Implement a proper Backend Facade Pattern using `BackendService` as the sole point of interaction.

### Architectural Shift
**Current:** `UI/Managers` $\rightarrow$ `NakamaManager.client`
**Proposed:** `UI/Managers` $\rightarrow$ `BackendService (Facade)` $\rightarrow$ `Nakama/Platform Adapters`

### Implementation Details
1. **Unified API Methods:** Create typed methods in `BackendService` for all common operations (e.g., `authenticate()`, `call_rpc()`, `get_leaderboard()`, `submit_score()`).
2. **Centralized RPC Handler:** Use a single `call_rpc` method to handle `rpc_async` calls, wrap them in `is_exception()` checks, and return a standardized `{"success": bool, "data": mixed}` result.
3. **Migration:** Replace all direct `NakamaManager.client` calls in managers and UI panels with calls to `BackendService`.

## Benefits
- **Decoupling:** UI and Managers are no longer tied to the Nakama SDK.
- **Testability:** The `BackendService` can be easily mocked for unit testing.
- **Consistency:** Centralized error handling and logging for all network traffic.
- **Flexibility:** Backend providers can be switched or updated without changing UI code.

## Acceptance Criteria
- **Facade Coverage:** `BackendService` implements all required RPC and session methods.
- **Zero Direct Calls:** A search for `rpc_async` outside of `BackendService` and `NakamaManager` returns zero results.
- **Unified Error Handling:** All network calls return a standardized result dictionary.
- **Functional Parity:** All existing game flows function identically after migration.

## Migration Checklist
- [ ] Implement the `BackendService` singleton with typed wrapper methods.
- [ ] Migrate `friend_manager.gd` to use the facade.
- [ ] Migrate `admin_panel.gd` to use the facade.
- [ ] Migrate `user_profile_manager.gd` and other remaining managers.
- [ ] Implement centralized logging and error mapping in `BackendService`.
- [ ] Write unit tests for the facade using a mock backend.
