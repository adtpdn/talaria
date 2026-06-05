---
title: "Gauntlet: Disable Default Powerups Except Smack"
id: "080"
status: "in-progress"
priority: 01
sprint: alpha
category: BUG
description: "Default power-ups are active in Gauntlet mode; only Smack should be available."
assignee: "default"
cron_job: "pending"
modified: "2026-06-04"
---

# Gauntlet: Disable Default Powerups Except Smack

## Problem
Default power-ups (non-Smack) are active in Gauntlet mode, conflicting with the intended gameplay where only Smack is the primary PvP tool.

## Solution
Disable all default power-ups in Gauntlet mode, keeping only Smack enabled.

### Technical Details
1. Locate power-up spawn/activation logic for Gauntlet mode.
2. Filter out or disable non-Smack power-ups in Gauntlet.
3. Ensure Cleanser (mission-granted) still works alongside Smack.
4. Update power-up UI to show only Smack when available.

## Acceptance Criteria
- Only Smack and Cleanser are available in Gauntlet mode.
- No other power-ups spawn or activate.
- Power-up UI reflects only available items.

## Migration Checklist
- [ ] Add Gauntlet mode check in power-up spawn system.
- [ ] Disable non-Smack/Cleanser power-ups for Gauntlet.
- [ ] Update HUD to filter power-up display by mode.
- [ ] Test that Smack still charges and activates correctly.
