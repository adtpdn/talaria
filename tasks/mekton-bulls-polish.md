---
title: "Mekton Bulls: Polish — Bull SFX + Knock Burst"
id: "144"
status: "todo"
blocked_by: ["136", "137", "142"]
priority: 03
sprint: alpha
category: POLISH
description: "Final polish pass for Mekton Bulls — bull charge SFX, freeze VFX, knock burst, water-flood splash, and arena shrink camera effect."
modified: "2026-06-29"
---

# Mekton Bulls: Polish — Bull SFX + Knock Burst

## Problem
The shipped `gauntlet_manager` polish (`#076`, now `#120 Sugar Rush`)
covers rush-bar VFX and ×N badge for Sugar Rush. Mekton Bulls has a
distinct visual signature that the existing polish does not cover:

- Bull charge-up roar SFX.
- Bull ground-shake on charge release.
- Freeze VFX on the bull (ice-blue overlay).
- Knock burst on a player-vs-player shove.
- Water-flood splash + tide-rise audio.
- Arena shrink camera dolly-in (optional).

## Solution
Add Mekton-Bulls-specific polish assets and SFX hooks.

### Concrete Changes
1. Add `assets/audio/mekton_bulls/`:
    - `bull_charge.wav` — bull roar as it locks onto a target.
    - `bull_impact.wav` — heavy thud when the bull knocks a player out.
    - `freeze_burst.wav` — ice crackle.
    - `knock_burst.wav` — shove whoosh.
    - `water_flood.wav` — tide rising + splash.
2. Add `scenes/vfx/` for the new particles:
    - `freeze_overlay.tscn`
    - `knock_burst.tscn`
    - `water_flood.tscn`
3. Hook each from `MektonBullsManager`:
    - `_on_bull_charge_started()` → `bull_charge.wav`.
    - `_on_bull_impact(player)` → `bull_impact.wav` + camera shake.
    - `_use_freeze(target_bull)` → freeze VFX + SFX on bull node.
    - `_use_knock_on_player()` → knock_burst VFX + SFX at target.
    - `_trigger_water_flood()` → water_flood VFX + SFX.
4. Optional arena-shrink camera dolly (3 s ease).
5. Default volumes wired via `SettingsManager`.

## Acceptance Criteria
- Bull charge plays a distinct SFX.
- Bull impact shakes the camera.
- Freeze on a bull renders a visible ice overlay.
- Water flood has a splash + audio.
- Knock burst distinct from bull impact.

## Migration Checklist
- [ ] Add SFX assets (or placeholder paths).
- [ ] Add VFX scenes.
- [ ] Wire to all bull / freeze / knock / flood events.
- [ ] Add camera shake hook (reuse `#079`).
- [ ] Add settings defaults.
- [ ] Localization strings for HUD overlays.