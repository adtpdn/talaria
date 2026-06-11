---
title: "Gauntlet: Game Mode Registration"
id: "065"
status: "in_progress"
priority: 01
sprint: alpha
category: CORE
description: "Register the 'Candy Pump Survival' mode into the game's mode system and lobby to allow selection and configuration."
modified: "2026-06-10"
---

# Gauntlet: Game Mode Registration

## Problem
The current `GameMode` system only supports FreeMode, Stop N Go, and Tekton Doors. Without registration, the Gauntlet mode cannot be selected in the lobby, its specific settings cannot be synced between host and clients, and the `main.gd` orchestrator cannot instantiate the necessary managers to start the match.

## Solution
Integrate the Gauntlet mode into the existing `GameMode` enum and `LobbyManager` configuration. **Renamed from "Candy Cannon Survival" to "Candy Pump Survival" in v2.**

### Integration Steps
1. **Enum Update:**
    - Add `GAUNTLET = 3` to `scripts/game_mode.gd`.
    - Update helper functions: `from_string()`, `mode_to_string()`, and `get_all_modes()`.
    - **Rename string from `"Candy Cannon Survival"` to `"Candy Pump Survival"`.**
2. **Lobby Integration:**
    - Add `"Candy Pump Survival"` to the `available_game_modes` list in `scripts/managers/lobby_manager.gd`.
    - Map the mode to the `"Gauntlet Arena"` area.
3. **Settings Configuration (v2 changes):**
    - `gauntlet_round_duration` (180s) — unchanged.
    - **Replace** `gauntlet_cannon_interval` with `gauntlet_growth_interval` (3s between growth ticks).
    - **Replace** `gauntlet_volley_size` with `gauntlet_cells_per_tick` (dict: phase1=[4,6], phase2=[6,8], phase3=[8,10]).
    - Create corresponding `set_gauntlet_*()` and `sync_gauntlet_*()` RPCs for network synchronization.
4. **Orchestration Hooks:**
    - Add logic to `main.gd` to instantiate `GauntletManager` when the mode is selected.

## Benefits
- **Discoverability:** Mode is visible and selectable for players in the lobby.
- **Consistency:** Host-defined match parameters are perfectly synced across the network.
- **Modular Startup:** Proper registration allows `main.gd` to load the correct manager without hardcoding logic into every mode.

## Acceptance Criteria
- **UI Verification:** Confirm "Candy Pump Survival" appears in the Game Mode dropdown and "Gauntlet Arena" is selected.
- **Network Sync:** Verify that changing `round_duration` on the host reflects instantly on all client lobbies.
- **Startup Flow:** Verify that `GauntletManager` is successfully added to `main` and `_setup_arena()` is called on start.

## Migration Checklist
- [ ] Update `scripts/game_mode.gd` enum and string mappings (rename to "Candy Pump Survival").
- [ ] Update `scripts/managers/lobby_manager.gd` with new mode name and area mapping.
- [ ] **Replace** `gauntlet_cannon_interval`/`gauntlet_volley_size` settings with `gauntlet_growth_interval`/`gauntlet_cells_per_tick`.
- [ ] Implement new `gauntlet_*` settings and RPCs in `LobbyManager`.
- [ ] Add `gauntlet_manager` instantiation block to `main.gd`'s `_init_managers()`.
- [ ] Add `gauntlet_manager._setup_arena()` branch to `main.gd`'s `_setup_host_game()`.
- [ ] Add `gauntlet_manager.start_game_mode()` branch to `main.gd`'s `_start_game()`.
