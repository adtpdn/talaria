---
title: "GameModes"
slug: "gamemode-candy-survival"
description: "Talaria game-mode catalog. Gauntlet (shipped, as Candy Pump Survival) plus the designed Candy Survival and Mekton Bulls modes."
modified: "2026-06-29"
---

# GameModes

Talaria's current shipped mode family is **Gauntlet** (displayed in the
lobby as **"Candy Pump Survival"**). Sitting alongside it are two **designed
but not implemented** modes — **Candy Survival** and **Mekton Bulls** — which
together form the *Speed / Points / Knock / Survive* design pillar for the
next iteration.

Every implementation reference below is grounded in the live Godot project at
`/home/beng/Godot/Projects/tekton-enet`, against the task list at
`/home/beng/Documents/github/talaria`.

---

## Gauntlet (Shipped — `GameMode.GAUNTLET`)

The currently playable mode. Wired through `scripts/game_mode.gd` (the
`GameMode.GAUNTLET` enum, value `3`, string `"Candy Pump Survival"`),
orchestrated by `scripts/managers/gauntlet_manager.gd`, configured in
`scripts/managers/lobby_manager.gd` (`gauntlet_round_duration`).

### Live Constants (from source)

| Constant              | Value                         | Source |
| --------------------- | ----------------------------- | ------ |
| Arena size            | **20 × 20**                   | `gauntlet_manager.gd` `ARENA_COLUMNS=20`, `ARENA_ROWS=20` |
| Round duration        | **180 s** (host-configurable) | `lobby_manager.gd` `gauntlet_round_duration=180` |
| NPC center            | `(9, 9)` (center of 3×3)      | `gauntlet_manager.gd` `NPC_CENTER` |
| Telegraph window      | **1.0 s** passable before sticky | `gauntlet_manager.gd` `telegraph_duration=1.0` |
| Slow-mo duration      | **4.0 s** at ¼ speed          | `gauntlet_manager.gd` `slowmo_duration=4.0`, `trigger_slowmo()` |
| Phase 3 start         | when **120 s** remain (Survival Endgame) | `gauntlet_manager.gd` `PHASE_3_START=120.0` |
| Phase enum            | `OPEN_ARENA → ROUTE_PRESSURE → SURVIVAL_ENDGAME` | `gauntlet_manager.gd` `enum Phase` |

### Task Coverage

| # | Status | Task |
| - | ------ | ---- |
| [065](https://dev.klud.top/talaria/) | done     | Gauntlet: Game Mode Registration (`GameMode.GAUNTLET`, `LobbyManager`, `GauntletManager`) |
| [066](https://dev.klud.top/talaria/) | done     | Gauntlet: Arena Setup (20×20 Grid with Layers) — matches `ARENA_COLUMNS`/`ARENA_ROWS` |
| [067](https://dev.klud.top/talaria/) | done     | Gauntlet: Growth Tick System — `gauntlet_manager._process_growth_tick()`, `_cells_this_tick()` |
| [068](https://dev.klud.top/talaria/) | done     | Gauntlet: Sticky Cell System — `is_sticky_cell()`, `clear_sticky_cell()`, `apply_sticky_slow()` |
| [069](https://dev.klud.top/talaria/) | done     | Gauntlet: Telegraph VFX — `sync_growth_telegraph()`, `_spawn_telegraph_highlight()` |
| [070](https://dev.klud.top/talaria/) | done     | Gauntlet: Growth Phase Escalation — `cells_per_tick` dict + `_check_phase_transition()` |
| [071](https://dev.klud.top/talaria/) | done     | Gauntlet: Smack Mechanic — `has_smack_charged()`, `consume_smack()` |
| [072](https://dev.klud.top/talaria/) | done     | Gauntlet: Cleanser Power-Up — `_try_use_cleanser()`, `use_cleanser_cell()` |
| [073](https://dev.klud.top/talaria/) | done     | Gauntlet: Candidate Scoring — `_calculate_candidate_score()` + 7 layer scorers |
| [074](https://dev.klud.top/talaria/) | done     | Gauntlet: Tile Spawning & Mission System — `setup_mission_tiles()` |
| [075](https://dev.klud.top/talaria/) | done     | Gauntlet: Bot AI — Sticky Avoidance & Pathfinding (`BotStrategicPlanner`) |
| [077](https://dev.klud.top/talaria/) | done     | Gauntlet: Cleanser Icon Fix — `_generate_cleanser_icon()` |
| [078](https://dev.klud.top/talaria/) | done     | Gauntlet: Slow-Mo Effect (1/4 Speed) — `trigger_slowmo(duration=4.0)` |
| [079](https://dev.klud.top/talaria/) | done     | Gauntlet: Screenshake Follows Player — `screen_shake.gd` |
| [080](https://dev.klud.top/talaria/) | done     | Gauntlet: Disable Default Powerups Except Smack |
| [081](https://dev.klud.top/talaria/) | done     | Gauntlet: Telegraph Floor Highlight — `_spawn_telegraph_highlight()` |
| [082](https://dev.klud.top/talaria/) | done     | Gauntlet: Candy Bubble System — `_try_spawn_bubble()`, `_explode_bubble()` |
| [083](https://dev.klud.top/talaria/) | done     | Gauntlet: Movement Buffer System — `_detect_movement_buffers()`, `_buffer_penalty_at()` |
| [076](https://dev.klud.top/talaria/) | progress | Gauntlet: Polish — VFX, SFX, HUD & Arena Scene (`_setup_hud()`, `_animate_phase_label()`) |

**18 done / 1 in progress.** Grep confirms `sugar_rush`, `mekton_bull`,
`shrinking_arena`, `candy_survival` return **0 hits** anywhere in
`tekton-enet/scripts/` — every designed mode on this page is unimplemented.

---

## Candy Survival (Designed)

> **Candy Survival is a Gauntlet game mode.** 2-minute-or-less matches
> built on Speed, Points, Knock, and Survive.

Free-for-all variant. Everyone runs, everyone steals, the Mekton sits in
the middle as a scoring target. **Not implemented** — no function in
`gauntlet_manager.gd` references candies, head-stacks, or Sugar Rush.

### Arena

- **18 × 18** grid (vs. the 20 × 20 shipped in `gauntlet_manager.gd`).
- Blueprints are **single-color focused**.
- **Automatic tile pickup** — no input needed; walking over a matching
  tile counts it.
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
roaming bulls, and survival is placement-scored. **Not implemented** — no
shrinking-arena code exists in `tekton-enet/scripts/`.

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

## What's Implemented vs. Designed

A direct comparison of what is in `tekton-enet/scripts/` today vs. what the
two designed modes would require.

### Already in `gauntlet_manager.gd` (referenced by task #)

- **Mode registration, arena, orchestrator** — #065, #066 (`GameMode`,
  `GauntletManager`, `LobbyManager`).
- **Growth hazard** (sticky cells, telegraph, growth tick, phase escalation)
  — #067, #068, #069, #070, #081 (`_process_growth_tick`, `is_sticky_cell`,
  `sync_growth_telegraph`, `_check_phase_transition`).
- **Mission tiles & tile spawning** — #074 (`setup_mission_tiles`).
- **AI (candidate scoring, sticky avoidance, movement buffer)** — #073,
  #075, #083 (`_calculate_candidate_score`, `BotStrategicPlanner`,
  `_detect_movement_buffers`).
- **Smack knockback** (re-usable as the "Knock" charge) — #071
  (`has_smack_charged`, `consume_smack`).
- **Cleanser power-up + icon** — #072, #077 (`_try_use_cleanser`,
  `_generate_cleanser_icon`).
- **Feedback** (slow-mo, screenshake) — #078, #079 (`trigger_slowmo`,
  `screen_shake.gd`).
- **Extras** (candy bubble, disable default powerups) — #080, #082
  (`_try_spawn_bubble`, `_explode_bubble`).
- **Polish pass** — #076 (`_setup_hud`, `_animate_phase_label`).

### New for Candy Survival (not in source)

- **18 × 18 arena** (would need to override `ARENA_COLUMNS=20` /
  `ARENA_ROWS=20`).
- **Candy stack on head** with per-second multiplier + visible `×N` badge.
- **Mekton color rotation** and matching-color delivery rules.
- **Sugar Rush mutator** (×1.2 per candy, ×2 game-speed, red bar, stacking
  cap TBD).
- **Spawn gear**: 5 knock charges OR 5 ghost charges (4 s).
- **Self-knock rebound** for stealing from a candy-less player.
- **Mekton Cheerleaders** outside the board, low-leaderboard activation
  (TBD).
- **`/2` point penalty** for finishing a blueprint with the wrong color.

### New for Mekton Bulls (not in source)

- **Shrinking arena** (20 → 19 → 18 → 17) with **water-flood outer ring**.
- **Big Mektons** as roaming bulls (separate from the stationary delivery
  Mekton).
- **3 × 3 blueprints** (vs. Candy Survival's 1-color focused).
- **1 power per blueprint**: Freeze or Knock.
- **Placement-scored** static point system (replaces the per-second
  trickle).

### Duration callout

The shipped default is **180 s** (`gauntlet_round_duration`), but the
designed modes target **≤ 120 s**. The host can lower the timer today via
`LobbyManager.set_gauntlet_round_duration()`; no code change needed for
the shorter cap, just a lobby preset.