---
title: "Tekton Animation Pack Overhaul"
id: "090"
status: done
priority: 01
sprint: beta
category: ASSETS
description: "Rebuild animation-pack with original Blender bone names, remove dasher-pack, add holding_walk blend."
modified: "2026-06-15"
---

### Goal / Risk

Replace old dasher-pack with unified animation-pack using original Blender bone names. No retarget indirection.

### Solution

1. Renamed rig root in character GLBs (Bob, Oldpop, Masbro, Gatot) to "Character"
2. Rebuilt animation-pack.res from animation-0.glb with original bone names (no retarget indirection)
3. Removed all dasher-pack assets (res, tres, GLBs)
4. Set holding_1 to loop mode for continuous carry animation
5. Created holding_walk blend (walk_forward legs + holding_1 arms) in build script

### Files Modified

- tools/build_animation_pack.gd — no rest-pose correction, holding_1 loop, holding_walk blend generation
- tools/rename_rig_in_glb.py — new tool for GLB rig rename
- assets/characters/animations/animation-pack.res — rebuilt with 16 animations (15 original + holding_walk)
- assets/characters/animations/*.res — individual clip exports
- assets/characters/{Bob,Oldpop,Masbro,Gatot}.glb — rig root renamed to Character
- tools/README.md — updated docs
