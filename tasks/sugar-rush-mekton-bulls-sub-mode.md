---
title: "Sugar Rush: Mekton Bulls Sub-Mode Flag"
id: "132"
status: "halt"
halt_reason: "need confirmation"
priority: 02
sprint: alpha
category: CORE
description: "Register Mekton Bulls as a sub-mode flag on GameMode.GAUNTLET — share orchestrator and lifecycle, override arena rules."
modified: "2026-06-29"
---

# Sugar Rush: Mekton Bulls Sub-Mode Flag

## Problem
Mekton Bulls is a Sugar Rush sub-mode with a shrinking arena and roaming
bulls (see #133). It needs to share the same orchestrator
(`gauntlet_manager.gd`) and lobby registration but with a flag that swaps
arena behavior.

## Solution
Add a `mekton_bulls_enabled: bool` flag on `GameMode` config.

### Changes
1. Add `mekton_bulls_enabled: bool` to `ModeConfig`.
2. Add `is_mekton_bulls_mode() -> bool` helper.
3. In `start_game_mode()`:
    - If `is_mekton_bulls_mode()` → call `_start_mekton_bulls()` (#133).
    - Otherwise → call `_start_sugar_rush()` (current behavior).
4. Lobby UI: sub-mode checkbox when "Sugar Rush" is selected.

## Acceptance Criteria
- Toggling Mekton Bulls in lobby enables the sub-mode.
- The flag is networked.
- Sub-mode picks the correct startup routine.
- Bots and humans work in both modes.

## Migration Checklist
- [ ] Add `mekton_bulls_enabled` flag.
- [ ] Add `is_mekton_bulls_mode()` helper.
- [ ] Branch `start_game_mode` on the flag.
- [ ] Add lobby UI checkbox.