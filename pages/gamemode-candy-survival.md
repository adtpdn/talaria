---
title: "GameModes"
slug: "gamemode-candy-survival"
description: "Talaria game-mode catalog — Gauntlet (the implemented family) plus the designed Candy Survival and Mekton Bulls modes."
modified: "2026-06-29"
---

# GameModes

This page catalogs Talaria's game modes. The currently **implemented** mode
family is **Gauntlet** (19/19 core tasks done, 1 polish task in progress).
Sitting alongside it are two **designed** modes that have not shipped yet —
**Candy Survival** and **Mekton Bulls** — which together form the
*Speed / Points / Knock / Survive* design pillar for the next Gauntlet
iteration.

Matches are **2 minutes or less**, routed through the existing
`gauntlet_round_duration` setting, and orchestrated by `GauntletManager` from
`main.gd` (see task #065).

---

## Gauntlet (Implemented)

The shipped game mode. 20×20 arena, growth-tick sticky hazard system, mission
tiles, Smack knockback, Cleanser power-up, slow-mo & screenshake feedback.

| # | Status | Task |
| - | ------ | ---- |
| [065](https://dev.klud.top/talaria/) | done     | Gauntlet: Game Mode Registration |
| [066](https://dev.klud.top/talaria/) | done     | Gauntlet: Arena Setup (20×20 Grid with Layers) |
| [067](https://dev.klud.top/talaria/) | done     | Gauntlet: Growth Tick System (Replaces Cannon Volley) |
| [068](https://dev.klud.top/talaria/) | done     | Gauntlet: Sticky Cell System (v2) |
| [069](https://dev.klud.top/talaria/) | done     | Gauntlet: Telegraph VFX System (v2) |
| [070](https://dev.klud.top/talaria/) | done     | Gauntlet: Growth Phase Escalation (Replaces Impact Sizes) |
| [071](https://dev.klud.top/talaria/) | done     | Gauntlet: Smack Mechanic |
| [072](https://dev.klud.top/talaria/) | done     | Gauntlet: Cleanser Power-Up |
| [073](https://dev.klud.top/talaria/) | done     | Gauntlet: Candidate Scoring System (Replaces Targeting Intelligence) |
| [074](https://dev.klud.top/talaria/) | done     | Gauntlet: Tile Spawning & Mission System |
| [075](https://dev.klud.top/talaria/) | done     | Gauntlet: Bot AI — Sticky Avoidance & Pathfinding |
| [077](https://dev.klud.top/talaria/) | done     | Gauntlet: Cleanser Icon Fix |
| [078](https://dev.klud.top/talaria/) | done     | Gauntlet: Slow-Mo Effect (1/4 Speed) |
| [079](https://dev.klud.top/talaria/) | done     | Gauntlet: Screenshake Follows Player |
| [080](https://dev.klud.top/talaria/) | done     | Gauntlet: Disable Default Powerups Except Smack |
| [081](https://dev.klud.top/talaria/) | done     | Gauntlet: Telegraph Floor Highlight Before Growth |
| [082](https://dev.klud.top/talaria/) | done     | Gauntlet: Candy Bubble System |
| [083](https://dev.klud.top/talaria/) | done     | Gauntlet: Movement Buffer System |
| [076](https://dev.klud.top/talaria/) | progress | Gauntlet: Polish — VFX, SFX, HUD & Arena Scene |

All 19 gameplay/AI tasks are `done`; only the final polish pass (#076) is
still in flight.

---

## Candy Survival (Designed)

> **Candy Survival is a Gauntlet game mode.** 2-minute-or-less matches
> built on Speed, Points, Knock, and Survive.

A free-for-all variant. Everyone runs, everyone steals, the Mekton sits in
the middle as a scoring target.

### Arena

- **18 × 18** grid.
- Blueprints are **single-color focused**.
- **Automatic tile pickup** — no input needed; walking over a matching tile
  counts it.
- If your blueprint's color runs out, finish it with any other color, but
  you only earn **½ points** for that blueprint.

### Candies on Your Head

- Finishing a blueprint drops a candy on your head in the matching color.
- **No carry cap** — stack as many as you can carry.
- Candies grant **points every second**. The more you stack, the **bigger
  the multiplier** on points earned.
- A `×2` (or current multiplier) badge must render next to the Mekton head
  sprite so opponents see the threat.

### Mekton Delivery

- The Mekton's face changes color on a timer.
- You can only deliver candies whose color matches the Mekton's **current**
  face color.
- A successful delivery = **big point payout**.
- Mismatched candies stay on your head (no penalty, no delivery).

### Sugar Rush Mutator

Feeding a candy to the Mekton triggers **Sugar Rush**:

| Parameter        | Value                          |
| ---------------- | ------------------------------ |
| Base rush time   | 2 s                            |
| Multiplier       | ×1.2 per candy in the batch    |
| Example          | 5 candies × 1.2 = 4 s of rush  |
| Effect           | Game speed ×2 — projectiles, dashers, AI, all timers |
| Visual           | Rush bar turns red while active |
| Stacking limit   | **TBD**                        |

Rush stacks additively up to the cap, then any extra duration converts to
points.

### Knock & Ghost Charges

Every player spawns with **5 knock charges OR 5 ghost charges** (your pick).

- **Knock** — shove another player. If they carry candies, **you steal them
  all** and they stack onto your pile.
- **Ghost (4 s)** — walk through candies freely and **cannot be knocked**.
- **Self-knock rule** — knocking a player who carries no candies rebounds:
  **you get knocked instead**.

### Sticky Floor

Sticky material is **pure collision** — it acts like a wall. Standing in it
is the same as standing on a hard tile: trapped, no pickup, no movement.

### Mekton Cheerleaders (TBD)

Cheerleaders stand **outside** the board. Each player picks one during
lobby. They activate only when you are **low on the leaderboard**.
Per-cheerleader buffs are still TBD.

---

## Mekton Bulls (Designed)

> **Mekton Bulls is a Gauntlet game mode.** 2-minute-or-less matches built
> on placement scoring inside a shrinking arena.

A second designed mode. Mektons are no longer a fixed target — they are
roaming bulls, and survival is placement-scored, not point-scored.

### Arena & Phases

The board **shrinks every phase**. A bull standing on the outside of the
arena **floods the outermost ring with water** — instant elimination.

| Phase | Board     |
| ----- | --------- |
| 1     | 20 × 20   |
| 2     | 19 × 19   |
| 3     | 18 × 18   |
| 4     | 17 × 17   |
| 5     | END       |

### Loop

- **Big Mektons** stampede around the arena like bulls.
- A bull that touches a player **knocks them out**.
- Blueprints are small, **3 × 3**, with **automatic tile pickup**.
- Completing a blueprint grants **1 power** — your choice:
    - **Freeze** — slow the nearest bull long enough to escape.
    - **Knock** — shove another player into the bull's path or out of the
      shrinking arena.
- Players can **knock each other** with the same mechanics the bulls use.

### Scoring

**Static point system** — placement-based, no per-second trickle.

| Placement     | Points                       |
| ------------- | ---------------------------- |
| Last standing | Max (fixed)                  |
| First out     | Min (fixed)                  |
| Middle        | Linear between min and max   |

---

## What's Implemented (vs. Candy Survival design)

Both designed modes ride on the existing Gauntlet infrastructure. Below is
what's already shipped (#065–#083) and what would have to be added for Candy
Survival / Mekton Bulls to ship.

### Already in the codebase (referenced by task #)

- **Mode registration, arena, orchestrator** — #065, #066.
- **Growth hazard** (sticky cells, telegraph, growth tick, phase escalation)
  — #067, #068, #069, #070, #081.
- **Mission tiles & tile spawning** — #074.
- **AI (candidate scoring, sticky avoidance, movement buffer)** — #073,
  #075, #083.
- **Smack knockback** (re-used as the "Knock" charge) — #071.
- **Cleanser power-up + icon** — #072, #077.
- **Feedback** (slow-mo, screenshake) — #078, #079.
- **Extras** (candy bubble, disable default powerups) — #080, #082.
- **Polish pass** — #076 (in progress).

### New for Candy Survival

- **18 × 18 arena** (currently 20 × 20 in #066).
- **Candy stack on head** with per-second multiplier + visible `×N` badge.
- **Mekton color rotation** and matching-color delivery rules.
- **Sugar Rush mutator** (×1.2 per candy, ×2 game-speed, red bar, stacking
  cap TBD).
- **Spawn gear**: 5 knock charges OR 5 ghost charges (4 s).
- **Self-knock rebound** for stealing from a candy-less player.
- **Mekton Cheerleaders** outside the board, low-leaderboard activation
  (TBD).
- **`/2` point penalty** for finishing a blueprint with the wrong color.

### New for Mekton Bulls

- **Shrinking arena** (20 → 19 → 18 → 17) with **water-flood outer ring**.
- **Big Mektons** as roaming bulls (separate from the stationary delivery
  Mekton).
- **3 × 3 blueprints** (vs. Candy Survival's 1-color focused).
- **1 power per blueprint**: Freeze or Knock.
- **Placement-scored** static point system (replaces the per-second
  trickle).