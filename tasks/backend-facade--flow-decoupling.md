---
title: "Backend Facade & Flow Decoupling"
id: "038"
status: "progress"
priority: 01
sprint: alpha
category: BACKEND
description: "Decouple game flows from direct backend calls by implementing a centralized facade with retry policies and error mapping."
assignee: "default"
cron_job: "pending"
modified: "2026-06-03"
---

# Backend Facade & Flow Decoupling

## Problem
Many UI panels and managers call `NakamaManager.client.rpc_async` directly. This creates tight coupling between the UI and network layers, making it impossible to implement global retry policies, central error handling, or switch backend providers without modifying dozens of files. It also leads to "silent failures" where the UI doesn't react correctly to specific backend error codes.

## Solution
Implement a unified `BackendService` facade that acts as the sole owner for all Nakama RPC, socket, and session calls.

### Implementation Details
1. **Centralize RPCs:** Migrate all `client.rpc_async` calls from UI scripts into typed methods within `BackendService`.
2. **Typed Error Mapping:** Implement a system to translate raw Nakama error codes into domain-specific errors (e.g., `ERR_INSUFFICIENT_FUNDS`) for UI interpretation.
3. **Retry Policy:** Implement a configurable retry mechanism (e.g., exponential backoff) within the facade for transient network failures.
4. **Graceful Degradation:** Ensure the facade provides fallback values or "offline" states to prevent UI hard-crashes.

## Benefits
- **Maintainability:** API changes only require updates in one file (`backend_service.gd`).
- **Reliability:** Automated retries reduce failed requests caused by momentary packet loss.
- **UX Consistency:** Uniform error messaging across the entire application.

## Acceptance Criteria
- **No Direct RPCs:** A codebase search for `rpc_async` outside of `backend_service.gd` and `nakama_manager.gd` returns zero results.
- **Retry Verification:** Simulated network failure during a profile fetch demonstrates the `BackendService` retrying the request.
- **Error Handling:** Verify that a known backend error (e.g., 403 Forbidden) is correctly mapped to a user-friendly error message.
- **Stability:** Confirm the UI remains responsive when the backend service is unreachable.

## Migration Checklist
- [ ] Identify all remaining `client.rpc_async` calls in UI/Manager scripts.
- [ ] Define typed method signatures in `BackendService` for each identified flow.
- [ ] Migrate calls from UI panels to the new `BackendService` methods.
- [ ] Implement the `error_map` dictionary and retry loop in `BackendService`.
- [ ] Verify high-traffic flows: Profile, Social, and Daily Rewards.
