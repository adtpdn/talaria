---
title: "Client Backend Facade"
id: "039"
status: "progress"
priority: 01
sprint: alpha
category: BACKEND
description: "Migrate all client-side RPC and session calls to use the unified BackendService facade, eliminating direct Nakama calls in UI and managers."
assignee: "default"
cron_job: "pending"
modified: "2026-06-03"
---

# Client Backend Facade

## Problem
The client codebase suffers from "RPC scatter," where networking calls are distributed across numerous UI panels and managers. This lack of ownership leads to duplicated bootstrap code, inconsistent session handling, and a high risk of bugs when updating backend API signatures, as changes must be propagated manually across the entire project.

## Solution
Enforce a strict architectural boundary where the `BackendService` is the sole entity allowed to interact with the `NakamaManager.client`.

### Implementation Path
1. **Ownership Consolidation:** Consolidate session, socket, and RPC ownership into a single typed facade.
2. **UI Migration:** Systematically remove all `client.rpc_async` calls from `scripts/ui/` and `scripts/managers/` (Economy, Auth, Mail, Gacha, and Social flows).
3. **Typed Interface:** Replace raw JSON RPC calls with strongly typed methods in the facade (e.g., `fetch_user_profile()`).
4. **Bootstrap Cleanup:** Remove duplicate authentication and connection logic, delegating all bootstrap responsibilities to the facade.

## Benefits
- **Simplified Debugging:** All network traffic can be logged or intercepted at a single point.
- **Architectural Clarity:** Clear separation between UI logic and network communication.
- **Reduced Code Duplication:** Eliminates redundant session-check and error-handling boilerplate.

## Acceptance Criteria
- **Zero UI RPCs:** A global search for `client.rpc_async` within `scripts/ui/` returns zero results.
- **Unified Session Ownership:** `NakamaManager.client` is accessed exclusively by `BackendService` (or `AuthManager`), with no other scripts holding direct references.
- **Typed Method Verification:** Core flows (Gacha, Mail, Social) use named methods returning typed results or known error objects.
- **Bootstrap Validation:** Confirm the game startup sequence calls a single initialization method in the facade.

## Migration Checklist
- [ ] Map all current `rpc_async` calls in the project to intended functionality.
- [ ] Implement typed wrappers in `BackendService` for each identified function.
- [ ] Replace direct calls in `scripts/ui/` with facade method calls.
- [ ] Audit `scripts/managers/auth_manager.gd` and `scripts/nakama_manager.gd` to remove redundant session code.
- [ ] Verify all migrated flows function correctly and handle errors via the facade.
