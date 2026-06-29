---
title: "Mekton Bulls: HUD — Bull Tracker, Power Picker, Placement"
id: "143"
status: "todo"
blocked_by: ["136", "139", "140"]
priority: 03
sprint: alpha
category: UI
description: "Build the Mekton Bulls HUD — bull tracker arrow, freeze/knock power picker, current placement, and the end-of-match placement overlay."
modified: "2026-06-29"
---

# Mekton Bulls: HUD — Bull Tracker, Power Picker, Placement

## Problem
Mekton Bulls is a fast mode with three new HUD surfaces:
1. **Bull tracker** — arrow / minimap pin pointing at the bull when
   it's off-screen.
2. **Power picker** — Freeze / Knock radial choice the moment a 3 × 3
   blueprint is completed.
3. **Placement overlay** — end-of-match table sorted by elimination
   order.

Sugar Rush's HUD (`tasks/sugar-rush-polish-rush-bar.md` -> `#120`) is
the wrong shape: it has a ×N stack badge and a red rush bar, neither
of which exist in Mekton Bulls.

## Solution
Build a Mekton-Bulls-specific HUD scene and wire it from
`main.gd`.

### Concrete Changes
1. New scene — `scenes/ui/mekton_bulls_hud.tscn` (sibling of
   `scenes/gauntlet_hud.tscn`):
    - `BullTracker` Control: arrow + minimap marker, follows the
      nearest `MektonBull`.
    - `PowerPicker` Control: radial that pops on
      `_on_blueprint_completed` (`#138`). Two slices: Freeze, Knock.
    - `PowerCounters` Control: shows current `player_power[pid]` counts.
    - `PlacementPanel` Control: hidden by default; revealed by
      `_on_round_ended` (`#140`).
2. `gauntlet_hud.tscn` is gated in `main.gd` by
   `LobbyManager.game_mode == "Candy Pump Survival"` — the same gate
   for the new HUD: `LobbyManager.game_mode == "Mekton Bulls"`.
3. `MektonBullsManager` exposes:
    - `signal blueprint_completed(pid: int)`
    - `signal round_ended(placements: Dictionary)`
    - `signal power_used(pid: int, power: String)`
4. End-of-match placement overlay lists:
    - Rank 1 — first eliminated (lowest points).
    - ... players in elimination order …
    - Rank N — last standing (highest points).

## Acceptance Criteria
- Bull tracker arrow points at the bull when off-screen.
- Power picker appears on blueprint completion and disappears after
  a choice.
- Power counters update as Freeze / Knock are used.
- Placement overlay appears at round end with all players ranked.
- HUD layout fits 720p and 1080p.

## Migration Checklist
- [ ] Create `scenes/ui/mekton_bulls_hud.tscn`.
- [ ] Add `BullTracker` + `PowerPicker` + `PlacementPanel` Controls.
- [ ] Wire signals from `MektonBullsManager`.
- [ ] Hook HUD activation in `main.gd`.
- [ ] Verify at 720p / 1080p.
- [ ] Localization strings ready for HUD text.