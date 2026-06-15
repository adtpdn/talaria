### Goal / Risk

Freemode arena fishing tektons don't animate — all 3 instances of `tekton_fishing_animation.glb` sit static. Static tekton throw in free mode doesn't face direction or play throw animation.

### Solution

1. Created `tekton_fishing_autoplay.gd` — plays both GLB animations (tekton body + fishing hook) simultaneously and loops them via AnimationPlayer
2. Attached script to all 3 fishing animation instances in `freemode.tscn`
3. Fixed static tekton throw: player now faces tekton toward throw direction and plays throw animation
4. Fixed AnimationPlayer path in `tekton.gd` for static turrets (`Visuals/tekton/AnimationPlayer`)
5. Fixed animation names from `tekton_throw_tile` to actual GLB name `ted_bones_001|Tekton Throwing Tiles|Anima_Layer`
6. Fixed static_tekton_controller.gd idle resume (no idle anim exists for static mesh — stops instead)

### Files Modified

- scenes/arena/freemode.tscn — added autoplay script to 3 fishing tekton instances
- scripts/tekton_fishing_autoplay.gd — new script, plays + loops all animations
- scenes/player.gd — sync_throw_tekton now faces tekton + plays throw anim, removed duplicate end_world_pos
- scripts/tekton.gd — fixed AnimationPlayer path for static turrets, fixed throw animation name
- scripts/static_tekton_controller.gd — fixed animation name, idle resume stops instead of playing nonexistent idle
