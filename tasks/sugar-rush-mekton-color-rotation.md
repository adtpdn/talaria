---
title: "Sugar Rush: Mekton Color Rotation Telegraph"
id: "114"
status: "todo"
priority: 02
sprint: alpha
category: CORE
description: "Replace the floor-telegraph VFX with a Mekton face-color rotation. The Mekton cycles through 4 colors on a timer; only matching-color candies deliver."
modified: "2026-06-29"
supersedes: ["069"]
---

# Sugar Rush: Mekton Color Rotation Telegraph

## Problem
`sync_growth_telegraph(cells)` highlights which floor cells will turn sticky
next. In Sugar Rush, the timing signal shifts from the floor to the **Mekton
face** — its visible color rotates on a timer and dictates which candy colors
are accepted.

## Solution
Drop the floor telegraph. Add a Mekton color state machine and a face-color
indicator.

### Changes
1. Remove `sync_growth_telegraph(cells)` RPC and its VFX.
2. Add `MektonFace` enum: `{RED, BLUE, GREEN, YELLOW}` (4 colors).
3. Add `current_mekton_color: MektonFace` state on `gauntlet_manager.gd` (or
   on the Mekton node itself if you have one).
4. Add `mekton_rotation_interval: float = 6.0` config (host-tunable).
5. Add `_rotate_mekton_color()` timer that cycles on `mekton_rotation_interval`.
6. Add `sync_mekton_color(color)` RPC + VFX to flip the Mekton face.
7. Add `current_mekton_color_matches(candy_color: Color) -> bool` helper.

## Acceptance Criteria
- Mekton face visibly changes color every 6 s.
- `current_mekton_color` is networked (host → clients).
- `current_mekton_color_matches()` returns true only for the active color.
- Old telegraph RPC is gone (or deprecated; clients ignore it for one release).

## Migration Checklist
- [ ] Add `MektonFace` enum.
- [ ] Add `mekton_rotation_interval` config + RPC.
- [ ] Implement `_rotate_mekton_color()` timer.
- [ ] Implement `sync_mekton_color()` RPC.
- [ ] Replace `sync_growth_telegraph` VFX with Mekton face-color VFX.
- [ ] Hook delivery rules (#128) to the new color state.