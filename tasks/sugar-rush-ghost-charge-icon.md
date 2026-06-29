---
title: "Sugar Rush: Ghost Charge Icon"
id: "121"
status: "todo"
priority: 03
sprint: alpha
category: POLISH
description: "Replace the Cleanser power-up icon with the new Ghost Charge icon on the action bar and HUD."
modified: "2026-06-29"
supersedes: ["077"]
---

# Sugar Rush: Ghost Charge Icon

## Problem
`_generate_cleanser_icon()` renders the Cleanser pickup icon. Sugar Rush
replaces Cleanser with the Ghost Charge (#117) — the icon must follow.

## Solution
Replace the Cleanser icon with the Ghost Charge icon.

### Changes
1. Rename `_generate_cleanser_icon()` → `_generate_ghost_charge_icon()`.
2. Update the icon texture path or generated mesh.
3. Update `update_cleanser_ui` (rename to `update_ghost_charge_ui`):
    - Show `ghost_charges` count instead of cleanser count.
4. Update touch-controls / action-bar bindings.
5. Color the icon translucent white to match the ghost VFX.

## Acceptance Criteria
- HUD shows a Ghost Charge icon with current charge count.
- Icon visually distinct from Cleanser (translucent vs solid).
- Action bar binding still triggers `_try_activate_ghost`.

## Migration Checklist
- [ ] Rename icon generator.
- [ ] Rename HUD updater.
- [ ] Update action-bar binding.
- [ ] Update touch-controls shortcut label.