---
title: "Powerup Floor VFX (Freeze, Block, Scatter)"
id: "095"
status: done
priority: 01
sprint: beta
category: CLIENT
description: "Added floor/UI VFX for the freeze-area and block-wall powerups, and a playerboard scatter VFX for Stop n Go, using template nodes under vfxController."
modified: "2026-06-18"
---

# Powerup Floor VFX (Freeze, Block, Scatter)

## Problem
Powerups lacked area-coverage VFX. The freeze powerup only showed a 1×1 initiator on the player; the block wall had no per-tile VFX; the Stop n Go tile-scatter penalty had no UI feedback.

## Solution

### Freeze area VFX
- New `Main.play_freeze_floor_vfx(center_x, center_z, radius, duration)` (RPC) — duplicates the hidden `vfxController/AnimatedSprite3D` (`freeze_floor` clip), scales it from its measured AABB to span the full `(2*radius+1)` tile area (with `AREA_SIZE_FACTOR` oversize tunable), centers it on the frozen cell, plays for the freeze duration, then frees it. Height/Y is taken from the template node so it can be tuned in the editor.
- Triggered from `special_tiles_manager.gd _execute_area_freeze`.
- Removed the old blue layer-0 highlight tiles (purely visual; slow effect is driven by `active_freeze_zones` / layer-2 checks, not those tiles) so only the VFX shows.

### Block wall VFX
- New `Main.play_block_floor_vfx(cells, duration)` (RPC) — spawns one `vfxController/box_block` per blocked cell (1×1 each), positioned at cell centers, with `DUPLICATE_USE_INSTANTIATION` so each glb's AnimationPlayer is carried. `_autoplay_vfx_animation()` plays the clip once (one-shot, `LOOP_NONE`). Frees all after `BLOCK_DURATION`.
- Triggered from `special_tiles_manager.gd _execute_block_floor`, passing the collected wall cells.

### Playerboard scatter VFX (Stop n Go)
- New `Main.play_playerboard_scatter_vfx()` (plain helper) — one-shot `scatter` clip over `PlayerBoardUI/AnimatedSprite2D`.
- Routed via player-node RPC `player.gd play_playerboard_scatter()` (`any_peer, call_local`), which self-filters to the local human (`name == str(get_unique_id())`, skip bots) — because the player-node name is not a valid network peer ID for `rpc_id` under the Nakama bridge.
- Triggered from `stop_n_go_manager.gd _scatter_player_tiles` via `player_node.rpc("play_playerboard_scatter")`.

## Files Modified
- scenes/main.gd — `play_freeze_floor_vfx`, `play_block_floor_vfx`, `_autoplay_vfx_animation`, `play_playerboard_scatter_vfx`.
- scripts/managers/special_tiles_manager.gd — freeze VFX call + removed blue highlight tiles; block VFX call with per-cell list.
- scenes/player.gd — `play_playerboard_scatter()` RPC (local-only filter).
- scripts/managers/stop_n_go_manager.gd — trigger scatter VFX via player-node RPC.

## Acceptance Criteria
- [x] Freeze powerup shows a flat animated overlay covering the 5×5 frozen area; no blue highlight tiles.
- [x] Block wall spawns one animated box per wall tile, one-shot, lasting the wall duration.
- [x] Stop n Go scatter shows the one-shot scatter animation only on the caught player's own board UI.
- [x] Scatter no longer throws "unknown peer ID" (routed via player-node RPC, not rpc_id).
