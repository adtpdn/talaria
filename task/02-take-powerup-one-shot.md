# take_powerup VFX One-Shot (No Loop)

**Status:** Done

## Context
The `take_powerup` animation was set to loop (`"loop": true`), but `play_skill_vfx` uses `await vfx.animation_finished` — a looping animation never emits that signal, so the VFX would play forever and never hide.

## Changes

### `assets/graphics/vfx/effects/powerup.tres`
- Changed `"loop": true` → `"loop": false` on the `take_powerup` animation

## Result
Animation plays once (30 frames @ 15 FPS = 2s), emits `animation_finished`, `play_skill_vfx` hides it. Clean one-shot on pickup.
