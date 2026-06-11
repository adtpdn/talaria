---
title: "Fix Tekton Pickup Prompt Keybind"
id: "086"
status: done
priority: 02
sprint: beta
category: UI
description: "Fixed the [G] prompt above roaming Tektons to follow keybind settings from options menu."
modified: "2026-06-11"
---
### Goal / Risk

The [G] prompt above roaming Tektons always showed G regardless of what the player bound the grab action to in settings.

### Solution

Fixed mapping in SettingsManager:
- get_action_display() now maps tekton_grab to the correct internal action_grab_tekton key.
- get_control_keycode() also updated with the same mapping.
