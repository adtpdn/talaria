---
title: "Mode Config Completeness"
id: "036"
status: done
priority: 01
sprint: alpha
category: CORE
description: "Remove duplicated/inconsistent option toggles. Add schema-driven validation."
---

# Mode Config Completeness

## Problem
Lobby mode configurations are inconsistent between game modes. Duplicated and fragile control toggles in `main.gd` and lobby scripts lead to state desyncs and potential crashes during match bootstrap. There is no shared validation schema, allowing invalid configs to be passed to the game server.

## Solution
Standardize mode configurations using a shared schema and host-authoritative synchronization.

### Implementation Path
1. **Toggles Cleanup:** Remove duplicated and fragile control toggles in the lobby UI and `main.gd`.
2. **Tekton Doors Parity:** Implement Tekton Doors options using the same host-authoritative lock and sync callbacks as Stop N Go.
3. **Schema-Driven Validation:** Introduce a shared validation schema used by the host, client display logic, and match bootstrap.
4. **Host Authority:** Ensure non-host clients always mirror host values and that invalid configs are rejected before match start.

## Benefits
- **Reliability:** Prevents "invalid config" crashes during match start.
- **Consistency:** Unified UI/UX for configuring different game modes.
- **Reduced Complexity:** Removes redundant logic and fragile toggles from the codebase.

## Acceptance Criteria
- **Config Parity:** Both Stop N Go and Tekton Doors expose full validated configurations in the lobby.
- **Authority Sync:** Verify that any change made by the host is instantly mirrored on all clients.
- **Validation Gate:** Attempt to spoof a mode config via RPC; verify the host rejects the change.
- **Bootstrap Integrity:** Confirm the match starts only after a valid config is validated by the host.

## Migration Checklist
- [x] Remove duplicated control toggles in `main.gd` and lobby scripts.
- [x] Implement Tekton Doors options with host-lock and sync callbacks.
- [x] Create the shared configuration validation schema.
- [x] Integrate schema validation into the match bootstrap flow.
- [x] Test spoofing attempts to verify host authority.
