---
title: "Decouple Managers with Observer Pattern"
id: "023"
status: "progress"
priority: 01
sprint: beta
category: CORE
description: "Replace direct manager-to-manager references with a centralized Event Bus based on the Observer pattern."
modified: "2026-06-03"
---

# Decouple Managers with Observer Pattern

## Problem
The current architecture suffers from "manager spaghetti," where managers (e.g., `LobbyManager`, `PlayerManager`, `AuthManager`) directly reference each other. This creates:
1. **Circular Dependencies:** Load-order crashes or complex initialization hacks.
2. **Fragile Changes:** Small changes in one manager cause a cascade of regressions across others.
3. **Untestability:** Unit testing a single manager requires instantiating the entire manager ecosystem.

## Solution
Implement a centralized `EventBus` (Observer Pattern) to handle all inter-manager communication.

### Implementation Details
1. **Implement `EventBus`:** Create a singleton `EventBus` to manage a registry of events and listeners.
2. **Event Definition:** Define strongly typed events (e.g., `EVENT_PLAYER_JOINED`, `EVENT_MATCH_STARTED`, `EVENT_CURRENCY_CHANGED`).
3. **Decoupling Process:**
    - Replace direct calls (e.g., `LobbyManager.player_manager.update_score()`) with `EventBus.emit("EVENT_UPDATE_SCORE", data)`.
    - Managers now "subscribe" to events during `_ready()`.
4. **Documentation:** Maintain a registry of all events, payloads, and their emitters/consumers.

## Benefits
- **Modular Architecture:** Managers become independent components that only care about events.
- **Simplified Testing:** Managers can be tested in isolation by mocking the `EventBus`.
- **Extensibility:** New features (e.g., Achievement System) can be added by subscribing to existing events without modifying existing managers.

## Acceptance Criteria
- **Zero Direct References:** Search for direct references between core managers (excluding `main.gd` initialization) returns zero results.
- **Event Bus Integrity:** All inter-manager communication is routed through `EventBus.emit()` and `EventBus.connect()`.
- **No Circular Dependencies:** Project loads without circular reference warnings or load-order crashes.
- **Documentation Completeness:** An `events.md` file exists, listing every event and its payload.
- **Functional Parity:** Verify all existing game flows (Login $\rightarrow$ Lobby $\rightarrow$ Match) function identically.
- **Test Coverage:** At least 3 critical flows are verified via unit tests using a mocked EventBus.

## Migration Checklist
- [ ] Create `scripts/managers/event_bus.gd` as an autoload singleton.
- [ ] Define the first set of core events based on current manager dependencies.
- [ ] Migrate a tightly coupled manager pair to the EventBus as a PoC.
- [ ] Systematically replace direct calls in `LobbyManager`, `PlayerManager`, and `AuthManager`.
- [ ] Create the `events.md` documentation.
- [ ] Run a full regression test of the lobby-to-match flow.
