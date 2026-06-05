---
title: "Gauntlet: Slow-Mo Effect (1/4 Speed)"
id: "078"
status: "in-progress"
priority: 02
sprint: alpha
category: FEATURE
description: "Implement slow-motion effect at 1/4 speed for animations and velocity."
assignee: "default"
cron_job: "pending"
modified: "2026-06-04"
---

# Gauntlet: Slow-Mo Effect (1/4 Speed)

## Problem
No slow-motion effect exists for dramatic moments or gameplay variety.

## Solution
Add slow-motion mode that reduces animation speed and physics velocity to 1/4 of normal.

### Technical Details
1. Add slow-motion toggle or trigger (e.g., item pickup, special event).
2. Scale `Engine.time_scale` to 0.25 for 1/4 speed.
3. Ensure animations, physics, and timers respect time scale.
4. Provide visual indicator (e.g., screen tint, HUD icon) during slow-mo.
5. Define duration (e.g., 3-5 seconds) or manual toggle.

## Acceptance Criteria
- Animations play at 1/4 speed during slow-mo.
- Player/NPC velocity reduced to 1/4.
- Visual feedback indicates slow-mo is active.
- Effect ends cleanly, restoring normal speed.

## Migration Checklist
- [ ] Add slow-mo state flag to game manager.
- [ ] Apply `Engine.time_scale = 0.25` when active.
- [ ] Reset to 1.0 on deactivation.
- [ ] Add HUD indicator for slow-mo status.
