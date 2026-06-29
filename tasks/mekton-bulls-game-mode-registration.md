---
title: "Mekton Bulls: Game Mode Registration"
id: "134"
status: "progress"
priority: 01
sprint: alpha
category: CORE
description: "Register Mekton Bulls as a new top-level game mode — enum entry, LobbyManager string, area mapping, MektonBullsManager node, main.gd dispatch hooks."
modified: "2026-06-29"
blocking: ["135", "136", "137", "138", "139", "140", "141", "142", "143", "144", "145"]
---

# Mekton Bulls: Game Mode Registration

## Problem
The shipped game mode system (`scripts/game_mode.gd`, enum
`FREEMODE = 0`, `STOP_N_GO = 1`, `TEKTON_DOORS = 2`, `GAUNTLET = 3`)
supports exactly four modes. The dispatcher in `scenes/main.gd`
branches on `LobbyManager.game_mode == "<string>"` and conditionally
spawns the matching manager node. **Mekton Bulls** is a new mode
that is its own game — different rules, different scoring, different
manager — and must follow the same separation pattern as the other
modes (Freemode = baseline, Stop n Go and Tekton Doors each have
their own manager, Gauntlet has `GauntletManager`).

This task is the **structural skeleton** all other Mekton Bulls work
depends on: without it, none of the orchestrator hooks land in the
right place and the mode can't be selected in the lobby.

## Solution
Add Mekton Bulls as a sibling top-level mode, not a sub-flag of
Gauntlet. Mirror the registration shape of `#065` but produce a
dedicated `MektonBullsManager` rather than reusing
`GauntletManager`.

### Concrete Changes (paths under `tekton-enet/`)

1. **Enum Update — `scripts/game_mode.gd`**
    - Add `MEKTON_BULLS = 4` to `Mode` enum.
    - `from_string("Mekton Bulls") → Mode.MEKTON_BULLS`
    - `mode_to_string(Mode.MEKTON_BULLS) → "Mekton Bulls"`
    - `get_all_modes()` includes `"Mekton Bulls"`.
    - `is_restricted()` returns `true` for `Mode.MEKTON_BULLS`.

2. **Lobby Wiring — `scripts/managers/lobby_manager.gd`**
    - Add `"Mekton Bulls"` to `available_game_modes`.
    - Map `"Mekton Bulls"` → `"Mekton Bulls Arena"` area.
    - Add `mekton_bulls_round_duration: int = 120` (default 2 min, matches
      design spec).
    - Add `set_mekton_bulls_round_duration()` + `sync_mekton_bulls_round_duration()` RPC.

3. **Manager Skeleton — `scripts/managers/mekton_bulls_manager.gd`**
    - New file. Extends `Node`.
    - Stub: `func initialize(main: Node, grid: Node) -> void`.
    - Stub: `func start_game_mode() -> void`.
    - `class_name MektonBullsManager`.
    - All `#135`–`#145` task code lives here or in helpers it owns.

4. **Orchestrator Hooks — `scenes/main.gd`**
    - Inside `_init_managers()`:
      ```
      if LobbyManager.game_mode == "Mekton Bulls":
          mekton_bulls_manager = load("res://scripts/managers/mekton_bulls_manager.gd").new()
          mekton_bulls_manager.name = "MektonBullsManager"
          add_child(mekton_bulls_manager)
          mekton_bulls_manager.initialize(self, $EnhancedGridMap)
      ```
    - Declare `var mekton_bulls_manager: MektonBullsManager = null` near the
      other manager vars.
    - Add `if mekton_bulls_manager and LobbyManager.game_mode == "Mekton Bulls":`
      branches in the lifecycle hooks (score loop, goal updates, player-state
      init, arena-setup) — same shape as the `gauntlet_manager` /
      `stop_n_go_manager` / `portal_mode_manager` branches.

5. **Scene / Area — `scenes/arena/mekton_bulls_arena.tscn`** (or
   whatever the existing `Gauntlet Arena` lives at)
    - Initial empty scene with a `GridMap` sized 20×20 placeholder and an
      `Area` node so the lobby can route to it.

## Why a Separate Game Mode (not a Sub-Flag of Gauntlet)

| Mode          | Manager                | Arena rules           | Scoring          |
| ------------- | ---------------------- | --------------------- | ---------------- |
| Freemode      | (none — baseline)      | Open arena            | Free             |
| Stop n Go     | `StopNGoManager`       | Phase-based stops     | Phase timer      |
| Tekton Doors  | `PortalModeManager`    | Portal-driven         | Portal capture   |
| Gauntlet / Sugar Rush | `GauntletManager` | 18 × 18 sticky growth | Per-second + delivery |
| **Mekton Bulls** | **`MektonBullsManager`** | **Shrinking arena, bulls** | **Static placement** |

Mekton Bulls has zero overlap with Sugar Rush: no growth tick, no
head-stack, no color rotation. It changes the **arena lifetime**
(shrinks mid-match) and the **scoring system** (placement not points).
Folding it into Gauntlet would couple two genuinely different game
loops. The shipped pattern — one manager per game mode — is the
correct architectural mirror.

## Acceptance Criteria
- Lobby lists `"Mekton Bulls"` as a selectable mode.
- `GameMode.MEKTON_BULLS = 4` parses both ways
  (`from_string` / `mode_to_string`).
- `MektonBullsManager` is added to `main` only when the mode is selected.
- `mekton_bulls_round_duration` is host-configurable and RPC-synced.
- All other modes (Freemode, Stop n Go, Tekton Doors, Gauntlet) keep
  their current behaviour unchanged.
- `main.gd` lifecycle hooks do not crash when other modes are selected
  (null-checks on `mekton_bulls_manager`).

## Migration Checklist
- [ ] Add enum entry + string mapping.
- [ ] Add lobby mode + area mapping + RPC.
- [ ] Create `scripts/managers/mekton_bulls_manager.gd` skeleton.
- [ ] Wire `main.gd` to instantiate it.
- [ ] Add `var mekton_bulls_manager` declaration.
- [ ] Null-check the manager in all `main.gd` lifecycle branches.
- [ ] Stub `start_game_mode()` so a fresh mode selection doesn't crash.
- [ ] Update mode picker icon / sound (placeholder).