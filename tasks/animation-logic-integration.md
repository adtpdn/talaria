---
title: "Animation Logic Integration"
id: "091"
status: done
priority: 01
sprint: beta
category: CODE
description: "Wire up animation hooks: holding blend while carrying, bot grab fallback, movement_finished idle transition."
modified: "2026-06-15"
---

### Goal / Risk

Integrate new animation-pack into gameplay logic. Bot grab animation not playing, no idle transition after movement, no leg blend while carrying.

### Solution

1. Added holding_walk/holding_1 idle logic in play_idle_animation and play_walk_animation
2. Fixed bot tekton grab — added offline fallback for sync_grab_tekton/sync_snatch_tekton
3. Connected movement_finished signal to play_idle_animation so animation transitions correctly after movement

### Files Modified

- scenes/player.gd — added holding_walk/holding_1 idle logic, connected movement_finished, fixed bot grab fallback
- scenes/player.tscn — removed dasher-pack library, updated UIDs
