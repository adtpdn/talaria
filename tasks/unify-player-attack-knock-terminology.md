---
title: "Unify Player Attack/Knock Terminology"
id: "084"
status: done
priority: 02
sprint: beta
category: CODE
description: "Refactored is_attack_mode and is_knock_mode into unified is_charged_strike across the entire codebase."
modified: "2026-06-11"
---
### Goal / Risk

Player had two separate boolean states (is_attack_mode and is_knock_mode) for the same charged mechanic, causing confusion.

### Solution

Unified both into a single is_charged_strike boolean and renamed attack_mode_timer to charged_strike_timer.

### Files Modified

- scenes/player.gd — Variables, timers, enter_charged_strike(), grab_tekton()
- scripts/bot_controller.gd — Bot now calls enter_charged_strike()
- scripts/managers/player_input_manager.gd — Input checks use is_charged_strike
- scripts/managers/player_movement_manager.gd — Push/knock logic uses is_charged_strike
- scripts/managers/powerup_manager.gd — Triggers enter_charged_strike()
- scripts/managers/tutorial_manager.gd — Updated fallback checks
