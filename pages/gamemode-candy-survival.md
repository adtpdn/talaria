---
title: "Candy Survival — Sugar Rush Chaos"
slug: "gamemode-candy-survival"
description: "Speed-and-points Gauntlet variant: 18×18 arena, automatic tile pickup, candy stack delivery, knock mechanics, and Sugar Rush mutators."
modified: "2026-06-29"
---

# Candy Survival — Sugar Rush Chaos

A high-tempo Gauntlet variant built around **Speed**, **Points**, and **Knock
players — Survive**. 2-minute-or-less matches on an **18×18** arena.

## Core Loop

1. Walk over tiles → automatic pickup into your blueprint progress.
2. Finish a blueprint → a candy of the matching color spawns on top of your
   head.
3. Stack as many candies as you can carry.
4. Deliver them to the **Mekton** when its face is the same color as the
   candy.
5. Knock rivals to steal their candies — or get knocked yourself.

---

## Arena

- **18 × 18** grid.
- **Blueprints are 1-color focused** — every blueprint is a single color.
- If the blueprint's color runs out before you finish it, you may complete it
  with **any other color**, but you only earn **½ points** for that blueprint.
- **Automatic tile pickup** — no keypress needed; walking over a matching tile
  counts it.

## Candies on Your Head

- Finishing a blueprint drops a candy on your head in the matching color.
- You can **stack as many as you want** — there is no hard cap on carries.
- Candies give you **points every second**, and the more you stack, the
  **bigger the multiplier** on points earned.
- The stack counter must be visible — show a `×2` (or current multiplier)
  badge next to the Mekton head sprite.

## Mekton Delivery

- The Mekton face changes color periodically.
- You can **only deliver** candies whose color matches the Mekton's current
  face color.
- Hitting the Mekton with a matching stack = **big point payout** for that
  delivery.
- Non-matching candies stay on your head (no penalty, but no delivery).

---

## Sugar Rush Mutator

Feeding a candy to the Mekton triggers a **Sugar Rush**:

| Parameter        | Value (current)                          |
| ---------------- | ---------------------------------------- |
| Base rush time   | **2 seconds**                            |
| Multiplier       | **×1.2** per candy fed in this batch     |
| Example          | 5 candies × 1.2 = **4 s** of rush        |
| Effect           | Game speed **×2** — projectiles, dashers, AI, all timers |
| Visual           | Rush bar turns **red** while active      |
| Stacking limit   | **TBD** (cap on rush duration / refresh)  |

> Rush stacks additively up to the cap, then convert into points.

---

## Knock / Ghost Charges

- Every player spawns with **5 knock charges OR 5 ghost charges** (your pick).
- **Knock:** shove another player; if they carry candies, **you steal them all**
  and they stack onto your own pile.
- **Ghost (4 s):** walk through candies freely and **cannot be knocked**.
- **Self-knock rule:** if you knock a player who carries **no candies**, the
  knock rebounds and **you get knocked** instead.

## Sticky Floor

Sticky material on the floor is **pure collision** — it acts like a wall.
Standing in it = trapped, same as a hard tile. No tile-pickup, no movement.

---

## Mekton Cheerleaders (TBD)

Cheerleaders stand **outside** the board. Each player picks one during lobby:

- Activates only when you are **low on the leaderboard**.
- Effect list and per-cheerleader buffs are still **TBD**.

---

# Mekton Bulls — Shrinking Arena

A second mode in the Candy Survival family: the Mektons are now roaming bulls.

## Loop

- **Big Mektons** stampede around the arena like bulls.
- A bull that touches a player **knocks them out**.
- The board **shrinks every phase**:

| Phase | Board     |
| ----- | --------- |
| 1     | 20 × 20   |
| 2     | 19 × 19   |
| 3     | 18 × 18   |
| 4     | 17 × 17   |
| 5     | END       |

- A bull standing on the outside of the arena **floods the outermost ring
  with water** — instant elimination if you're caught in it.

## Blueprints & Power

- Blueprints are small, **3 × 3**.
- **Automatic tile pickup** (same as Sugar Rush).
- Completing a blueprint grants **1 power**, your choice:
    - **Freeze** — slow the nearest bull long enough to escape.
    - **Knock** — shove another player into the bull's path or straight out
      of the shrinking arena.
- Players can **knock each other** with the same mechanics the bulls use.

## Scoring

**Static point system** — placement-based, no per-second trickle.

| Placement | Points |
| --------- | ------ |
| Last standing | Max (fixed) |
| First out | Min (fixed) |
| Middle    | Linear interpolation between min and max |

---

## Mode Picker

> 2 minutes or less per game. **Candy Survival is ( Gauntlet ).**

The current default mode picker routes Sugar Rush Chaos and Mekton Bulls
under the **Gauntlet** umbrella — fast matches, respawn off, single life
unless the mode explicitly grants one.