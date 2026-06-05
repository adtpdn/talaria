---
title: "Project-wide Code Quality Audit & Refactoring Plan"
id: "033"
status: todo
priority: 01
sprint: beta
category: CORE
description: "Address bloater classes, manageritis, and tight coupling through systemic refactoring."
---

# Project-wide Code Quality Audit & Refactoring Plan

## Problem
The project has accumulated significant technical debt that threatens stability and velocity:
1. **Bloater Classes:** `main.gd`, `player.gd`, and `lobby.gd` exceed 2,600 lines, handling everything from networking to VFX.
2. **Manageritis:** Over 70 managers create complex circular dependencies and a "switch-statement smell" in logic.
3. **Tight Coupling:** Managers are too intimate with specific node instances, preventing reusability and making unit testing nearly impossible.

## Solution
Execute a three-pronged refactoring strategy to decompose the architecture.

### Refactoring Strategy
1. **Class Decomposition:** Extract visual and utility logic from `main`, `player`, and `lobby` into specialized child components or services (e.g., `GridService`).
2. **Polymorphism via Strategy:** Replace hardcoded match statements for game modes and effects with the Strategy Pattern to make the system extensible.
3. **Observer Pattern Integration:** Decouple managers from actors using a centralized Event Bus (Signals) and Dependency Injection.

## Benefits
- **Reduced Regression Risk:** Smaller classes are easier to reason about and change without breaking unrelated systems.
- **Increased Extensibility:** New game modes or effects can be added without modifying core manager logic.
- **Improved Testability:** Decoupled components can be unit-tested in isolation.

## Acceptance Criteria
- **Class Size Reduction:** `main.gd`, `player.gd`, and `lobby.gd` are reduced in size by at least 40%.
- **Logic Decoupling:** Core managers no longer hold direct references to other managers' internal state.
- **Pattern Adoption:** At least 3 core systems are migrated from switch-statements to Strategy/State patterns.
- **Testing Baseline:** Ability to instantiate and test a manager without initializing the rest of the project.

## Migration Checklist
- [ ] Complete the a-priori audit of all classes > 1,000 lines.
- [ ] Extract `GridService` from `main.gd`.
- [ ] Migrate `special_tiles_manager.gd` logic to Strategy patterns.
- [ ] Implement the centralized `EventBus` and migrate the first 3 manager pairs.
- [ ] Document the new architectural boundaries in the project README.
