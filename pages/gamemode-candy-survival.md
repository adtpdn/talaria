---
title: "Candy Survival"
slug: "gamemode-candy-survival"
description: "Candy Survival is a Gauntlet game mode — 2-minute-or-less matches built on Speed, Points, Knock, and Survive."
modified: "2026-06-29"
---

# Candy Survival

**Candy Survival is a Gauntlet game mode.**

It belongs to the same family as Candy Pump Survival, registered under the
`GAUNTLET` mode enum (`scripts/game_mode.gd`) and the `Gauntlet Arena` lobby
area. What makes it its own sub-mode is the **speed-and-points** loop: walk
the arena, stack candies, feed the Mekton, and survive the chaos for up to
**2 minutes per match**.

## At a Glance

| Pillar        | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| Speed         | Automatic tile pickup, Mekton-paced color rotation, Sugar Rush mutator |
| Points        | Per-second carry multiplier, big delivery payouts, half-credit for off-color finishes |
| Knock         | Steal candies off other players' heads; ghosts bypass the same |
| Survive       | Sticky floor, shrinking arena, bulls, and water-flood rings  |

Matches are **2 minutes or less** — short enough for a queue rotation,
long enough to swing placement on points, knock, and timing.

---

## Sugar Rush Chaos

A free-for-all variant. Everyone runs, everyone steals.

### Arena

- **18 × 18** grid.
- Blueprints are **single-color focused**.
- **Automatic tile pickup** — no input needed; walking over a matching tile
  counts it.
- If your blueprint's color runs out, you can finish it with any other
  color, but you only earn **½ points** for that blueprint.

### Candies on Your Head

- Finishing a blueprint drops a candy on your head in the matching color.
- **No carry cap** — stack as many as you can carry.
- Candies grant **points every second**. The more you stack, the **bigger the
  multiplier** on points earned.
- A `×2` (or current multiplier) badge must render **next to the Mekton head
  sprite** so opponents see the threat.

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

Cheerleaders stand **outside** the board. Each player picks one during lobby.
They activate only when you are **low on the leaderboard**. Per-cheerleader
buffs are still TBD.

---

## Mekton Bulls — Shrinking Arena

The second sub-mode. Mektons are no longer a fixed target — they are now
roaming bulls.

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

## Why "Gauntlet"

Candy Survival inherits the Gauntlet contract from
`gauntlet-game-mode-registration`:

- registered under `GameMode.GAUNTLET`,
- routed to the `Gauntlet Arena` lobby area,
- driven by `gauntlet_round_duration` (≤ 120 s for Candy Survival),
- orchestrated by `GauntletManager` from `main.gd`.

What it adds on top of the base Gauntlet:

- **Candy stack** economy (head + multiplier + Mekton delivery).
- **Knock / Ghost** charges as spawn gear.
- **Sugar Rush** mutator (speed ×2) and **Bull** sub-mode (shrinking arena +
  placement scoring).

Everything else — `gauntlet_growth_interval`, `gauntlet_cells_per_tick`, the
Cleanser power-up, sticky cells, telegraphed tiles — is shared with the rest
of the Gauntlet family and described in the per-feature task docs under
`tasks/`.