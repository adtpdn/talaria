---
title: "Make take_powerup VFX One-Shot (No Loop)"
id: "097"
status: done
priority: 02
sprint: beta
category: VFX
description: "Disable looping on take_powerup animation so it plays once and auto-hides."
modified: "2026-06-19"
---
### Goal / Risk

The take_powerup animation was set to loop (loop: true), but play_skill_vfx uses await animation_finished — a looping animation never emits that signal, so the VFX would play forever.

### Solution

Changed loop: true to loop: false in assets/graphics/vfx/effects/powerup.tres.

### Acceptance Criteria

- [x] take_powerup plays once (30 frames @ 15 FPS = 2s)
- [x] Emits animation_finished so play_skill_vfx hides it
- [x] No visual glitches or leftover sprite after playback
