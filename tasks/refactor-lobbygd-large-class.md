---
title: "Refactor lobby.gd (Large Class)"
id: "020"
status: done
priority: 01
sprint: beta
category: CORE
description: "Refactor lobby.gd to reduce complexity. Extract UI, matchmaking, and networking into separate classes."
---

# Refactor lobby.gd (Large Class)

## Problem
`lobby.gd` had become a "God Object," handling UI updates, matchmaking logic, network communication, and player list management in a single file. This resulted in high cyclomatic complexity, making the file difficult to test and prone to regressions.

## Solution
Decompose `lobby.gd` by extracting its responsibilities into four specialized helper classes.

### Decomposition Plan
1. **UI Manager:** Handles all visibility, label updates, and modal transitions.
2. **Matchmaking Controller:** Manages room search, join/leave logic, and queue state.
3. **Player List Manager:** Tracks connected players, their profiles, and slot assignments.
4. **Network Interface:** Handles the raw RPCs and session sync specific to the lobby.

## Benefits
- **Maintainability:** Responsibilities are clearly divided, reducing the risk of "ripple effect" bugs.
- **Reduced Complexity:** Class size is significantly reduced, improving readability.
- **Testability:** Matchmaking and networking logic can now be unit-tested independently of the UI.

## Acceptance Criteria
- **Size Reduction:** `lobby.gd` size is reduced by 50% or more.
- **Responsibility Split:** No UI-specific calls (e.g., `get_node("Label")`) exist in the matchmaking or network classes.
- **Functional Parity:** All lobby features (joining, leaving, updating profiles) function identically to the original.
- **Performance:** No measurable impact on lobby load times or network latency.

## Migration Checklist
- [x] Extract UI management into a separate class.
- [x] Extract matchmaking logic into a separate class.
- [x] Extract player list management into a separate class.
- [x] Extract network communication into a separate class.
- [x] Reduce method complexity by delegating to the new classes.
- [x] Verify no regression in functionality via integration tests.
