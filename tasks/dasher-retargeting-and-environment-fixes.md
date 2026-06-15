---
title: "Dasher Animation Retargeting & Environment Fixes"
id: "089"
status: done
priority: 01
sprint: beta
category: CORE
description: "Fixed dasher animation converter (bone remap, rest-pose correction), Rokoko addon for Blender 5.1, Blender MCP install, Blender 4.3 install, multiplayer peer null guards, and Rokoko desktop shortcuts."
---

# Dasher Animation Retargeting & Environment Fixes

## Problem
Dasher character animations (dasher_hit, dasher_hold, dasher_take, etc.) were visually broken — arms twisted, hands in wrong direction. Root causes:
1. BONE_REMAP mapped `spine` to `Spine` instead of `Hips` (root bone)
2. Position/scale tracks kept on all bones instead of only Hips
3. No rest-pose correction between Blender rig and Mixamo rig
4. ANIM_PICK substring matching picked wrong source animations
5. Rokoko addon broken on Blender 5.1 (API changes)
6. No Blender 4.3 installed for Rokoko retargeting
7. Multiplayer peer null crashes on game mode exit

## Solution

### Animation Converter Fixes
- Fixed BONE_REMAP: `spine` → `Hips`, `spine.001` → `Spine`
- Track filtering: position/scale only on Hips bone
- Added rest-pose correction: `corrected = target_rest.inverse() * source_rest * keyframe_rotation`
- Fixed ANIM_PICK: exact middle-segment matching instead of substring
- Updated `dasher_take` mapping to `bob ani` (no Take animation in GLB)

### Rokoko Blender 5.1 Fix
- Patched `detection_manager.py`: replaced `action.fcurves` with channelbag system
- Patched `retargeting.py`: added `_get_action_fcurves()` and `_get_channelbag()` helpers, fixed `bone.select` → `bone.select_set()`

### Environment Setup
- Installed Blender 4.3.2 at `~/blender-4.3.2/`
- Installed Blender MCP addon (ahujasid/blender-mcp)
- Created separate desktop shortcuts: Blender 4.3, Blender 5.1

### Multiplayer Fixes
- Added peer null guards to `gauntlet_manager.gd` and `stop_n_go_manager.gd` `_process()`

## Files Changed
- `tools/convert_dasher_animations_headless.gd` — BONE_REMAP, track filtering, rest-pose correction, ANIM_PICK
- `tools/convert_dasher_animations.gd` — same fixes for EditorScript variant
- `assets/characters/animations/dasher_*.res` — regenerated with fixed converter
- `assets/characters/animations/dasher-pack.res` — rebuilt
- Rokoko addon: `detection_manager.py`, `retargeting.py`
- `~/.local/share/applications/blender-4.3.desktop`, `blender-5.1.desktop`
- Blender MCP addon installed at `~/.var/app/org.blender.Blender/config/blender/5.1/scripts/addons/blender_mcp.py`

## Status
Converter patched with full rest-pose correction. Animations rebuilt. Awaiting manual Rokoko retargeting in Blender 4.3 for final arm/hand fix.
