---
title: "Sugar Rush: Mekton Color Beacon (Replaces Floor Telegraph Highlight)"
id: "123"
status: "todo"
priority: 03
sprint: alpha
category: POLISH
description: "Replace the floor telegraph highlight with a Mekton face-color beacon — a glowing aura around the Mekton matching the active delivery color."
modified: "2026-06-29"
supersedes: ["081"]
---

# Sugar Rush: Mekton Color Beacon

## Problem
`_spawn_telegraph_highlight(pos)` paints a highlight on a floor cell that
will turn sticky next. Sugar Rush removes floor telegraph — the timing
signal now lives on the Mekton face (#114). The visual should move with it.

## Solution
Replace the floor highlight with a Mekton-face beacon.

### Changes
1. Remove `_spawn_telegraph_highlight()` (and any `_telegraph_highlight_*`
   resources).
2. Add `_spawn_mekton_beacon(color: Color)`:
    - Spawns a glowing ring / aura around the Mekton node.
    - Color matches `current_mekton_color`.
    - Pulses softly while active.
3. Re-call on `sync_mekton_color()` (see #114).
4. Audio cue on rotation (SFX: `mekton_color_change.wav`).

## Acceptance Criteria
- Mekton has a visible colored aura matching its current face color.
- Aura flashes / pulses softly.
- Rotation triggers SFX cue.
- No stray floor-telegraph highlights remain on the arena.

## Migration Checklist
- [ ] Remove `_spawn_telegraph_highlight` and its scene resources.
- [ ] Add `_spawn_mekton_beacon`.
- [ ] Wire to `sync_mekton_color`.
- [ ] Add SFX cue.
- [ ] Verify aura scales correctly at 18×18 camera distance (#112).