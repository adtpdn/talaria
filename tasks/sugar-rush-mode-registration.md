---
title: "Sugar Rush: Mode Registration"
id: "111"
status: "todo"
priority: 01
sprint: alpha
category: CORE
description: "Rename the shipped 'Candy Pump Survival' mode string to 'Sugar Rush' and document the new mode identity on the GameMode enum."
modified: "2026-06-29"
supersedes: ["065"]
---

# Sugar Rush: Mode Registration

## Problem
The shipped mode (`GameMode.GAUNTLET = 3`) currently displays in the lobby as
**"Candy Pump Survival"** (see `scripts/game_mode.gd` `mode_to_string()`).
The next iteration of the mode — built on Speed / Points / Knock / Survive —
should display as **"Sugar Rush"** to match the design pillar.

## Solution
Rename the mode display string, keep the enum value, and document the
Sugar Rush identity.

### Changes
1. `scripts/game_mode.gd`
    - `from_string("Sugar Rush") → Mode.GAUNTLET`
    - `mode_to_string(Mode.GAUNTLET) → "Sugar Rush"`
    - `get_all_modes()` returns `["Freemode", "Stop n Go", "Tekton Doors", "Sugar Rush"]`
    - `is_restricted()` still returns `true` for `Mode.GAUNTLET`.
2. `scripts/managers/lobby_manager.gd`
    - Add `"Sugar Rush"` to `available_game_modes` (replacing `"Candy Pump Survival"`).
    - Map mode → `"Gauntlet Arena"` area (unchanged).
3. `main.gd`
    - `GauntletManager` is still the orchestrator (no rename).

## Acceptance Criteria
- Lobby lists the mode as **"Sugar Rush"**.
- `GameMode.GAUNTLET` enum value remains `3`.
- Old `"Candy Pump Survival"` string still parses to `Mode.GAUNTLET` for
  legacy save data (`from_string` accepts both for one release).
- `main.gd` still instantiates `GauntletManager`.

## Migration Checklist
- [ ] Update `GameMode.mode_to_string()`.
- [ ] Update `GameMode.from_string()` (legacy alias).
- [ ] Update `LobbyManager.available_game_modes`.
- [ ] Update README/CHANGELOG.
- [ ] Verify save files still load.