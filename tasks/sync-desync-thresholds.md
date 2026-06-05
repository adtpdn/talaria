---
title: "Sync Desync Thresholds"
id: "035"
status: todo
priority: 01
sprint: alpha
category: NETWORKING
description: "Enforce max position/velocity deviation between client inputs and server ticks."
---
### Goal / Risk

Enforce max position/velocity deviation between client inputs and server ticks.

### Files / Areas

server/modules/match_handler.ts, player.gd

### Execution Checklist

- [ ] Define maximum allowed delta for position and velocity per tick.
- [ ] Implement server-side checks rejecting client states exceeding delta.
- [ ] Force client rubberbanding/correction on rejection.
### AI Execution Prompt

```plain text
Implement anti-cheat thresholds for movement sync. Review scripts/player.gd and server/modules/match_handler.ts. Define a maximum allowable distance/velocity delta per tick. In the server match loop, validate incoming client position updates against their last known state. If the delta exceeds the threshold (e.g., speedhacking/teleporting), reject the update and broadcast a forced correction (rubberband) to the client's last valid position. Acceptance: client cannot teleport across the map; server aggressively corrects impossible movements.
```

### Testing / Auto-Check

AI AUTO-CHECK: Simulate client sending position +1000 units in 1 tick. Assert server rejects, sends correction, and client snaps back.

### MS Teams Daily Report

```plain text
**Completed [PRD-P1-2]: Sync Desync Thresholds**\n- **Goal:** Enforce max position/velocity deviation between client inputs and server ticks.\n- **Status:** Integrated & verified. Code changes applied to: server/modules/match_handler.ts, player.gd
```
