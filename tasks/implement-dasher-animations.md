---
title: "Implement Dasher Animations"
id: "088"
status: in_progress
priority: 02
sprint: beta
category: ASSETS
description: "Integrate new dasher animations from assets/characters/dashers/ into the player animation-pack library."
modified: "2026-06-18"
---
### Goal / Risk

New character animations provided as separate .glb files in assets/characters/dashers/ need to be integrated into the player rig.

### Solution

Added _load_dasher_animations() to player.gd that dynamically loads dasher_*.glb files via GLTFDocument and appends them to the animation-pack library at runtime.

### Animations Loaded

- dasher_getting_hit
- dasher_hit
- dasher_hold
- dasher_put
- dasher_stun
- dasher_take

### Developer Note (For Tomorrow)

Hook these up to gameplay events:
- apply_stagger() -> dasher_stun or dasher_getting_hit
- enter_charged_strike() / try_push() / knock_tekton() -> dasher_hit
- grab_tekton() / set_carried() -> dasher_take, dasher_hold, dasher_put

Call with: anim_player.play("animation-pack/dasher_hit")
