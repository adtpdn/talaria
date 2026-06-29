---
title: "GameModes"
slug: "gamemode-candy-survival"
description: "Talaria game-mode catalog. Gauntlet (shipped, as Candy Pump Survival) → migrating to Sugar Rush, plus the new Mekton Bulls game mode (#134-#145)."
modified: "2026-06-29"
---

# GameModes

Talaria's current shipped mode family is **Gauntlet** (displayed in the
lobby as **"Candy Pump Survival"**). The next iteration renames it to
**Sugar Rush** — same enum (`GameMode.GAUNTLET = 3`), same manager
(`scripts/managers/gauntlet_manager.gd`), but with the *Speed / Points /
Knock / Survive* design pillar baked in.

A second, brand-new game mode — **Mekton Bulls** (`#134`–`#145`) — sits
alongside Sugar Rush as its **own top-level mode** (not a Sugar-Rush
sub-flag). It has its own manager, its own enum entry
(`GameMode.MEKTON_BULLS = 4`), its own lobby string, and a
shrinking-arena + placement-scoring loop that shares zero rules with
Sugar Rush.

Every implementation reference is grounded in the live Godot project at
`/home/beng/Godot/Projects/tekton-enet`, against the task list at
`/home/beng/Documents/github/talaria`.

---

## Sugar Rush (Next iteration — replaces Gauntlet)

> Sugar Rush is a Gauntlet game mode. 2-minute-or-less matches built on
> Speed, Points, Knock, and Survive.

### Live Constants (from `tekton-enet/scripts/`)

| Constant              | Current (Gauntlet)             | Target (Sugar Rush) | Source |
| --------------------- | ------------------------------ | ------------------- | ------ |
| Arena size            | **20 × 20**                    | **18 × 18**         | `gauntlet_manager.gd` `ARENA_COLUMNS=20`, `ARENA_ROWS=20` |
| Round duration        | **180 s** (host-configurable)  | **≤ 120 s**         | `lobby_manager.gd` `gauntlet_round_duration=180` |
| NPC center            | `(9, 9)` (center of 3×3)       | recompute for 18²   | `gauntlet_manager.gd` `NPC_CENTER` |
| Telegraph window      | **1.0 s** passable → sticky    | **n/a** — replaced by Mekton color rotation | `gauntlet_manager.gd` `telegraph_duration` |
| Slow-mo duration      | **4.0 s** at ¼ speed           | **Sugar Rush = ×2 speed, 2 s base** | `gauntlet_manager.gd` `slowmo_duration=4.0` |
| Phase enum            | `OPEN_ARENA → ROUTE_PRESSURE → SURVIVAL_ENDGAME` | `OPEN_ARENA → SUGAR_RUSH × STACK → SURVIVAL_ENDGAME` | `gauntlet_manager.gd` `enum Phase` |

### Migration Map — shipped Gauntlet → Sugar Rush

Each shipped Gauntlet task #065–#083 maps to one or more new Sugar Rush
tasks (`#111`–`#131` for Sugar Rush, `#134`–`#145` for the new Mekton Bulls game mode). Old tasks stay `done`; new tasks carry the work.

| Old # | Shipped (Gauntlet)                          | New # | Sugar Rush replacement |
| ----- | ------------------------------------------- | ----- | ---------------------- |
| [065](https://dev.klud.top/talaria/) | Game Mode Registration (display string = "Candy Pump Survival") | [111](#task-111) | Sugar Rush Mode Registration + rename to "Sugar Rush" |
| [066](https://dev.klud.top/talaria/) | Arena Setup 20 × 20                         | [112](#task-112) | Arena Setup 18 × 18 |
| [067](https://dev.klud.top/talaria/) | Growth Tick (`_process_growth_tick`)        | [113](#task-113) | Candy Stack Growth Tick (`_process_candy_tick`) |
| [068](https://dev.klud.top/talaria/) | Sticky Cell System                          | keep  | Sugar Rush keeps sticky on the floor (no change) |
| [069](https://dev.klud.top/talaria/) | Telegraph VFX (`sync_growth_telegraph`)     | [114](#task-114) | Mekton Color Rotation Telegraph (`sync_mekton_color`) |
| [070](https://dev.klud.top/talaria/) | Growth Phase Escalation                     | [115](#task-115) | Sugar Rush Stacking (`_check_sugar_rush_stack`) |
| [071](https://dev.klud.top/talaria/) | Smack Mechanic (`has_smack_charged`)        | [116](#task-116) | Knock Charge System (5 charges per spawn) |
| [072](https://dev.klud.top/talaria/) | Cleanser Power-Up                           | [117](#task-117) | Ghost Charge (4 s, 5 charges, walk-through + immune) |
| [073](https://dev.klud.top/talaria/) | Candidate Scoring                           | [118](#task-118) | Bot AI for Candy Survival (candy-stack aware) |
| [074](https://dev.klud.top/talaria/) | Tile Spawning & Mission                     | [119](#task-119) | Single-Color Blueprint Auto-Pickup |
| [075](https://dev.klud.top/talaria/) | Bot AI Sticky Avoidance                     | (folded into #118) | — |
| [076](https://dev.klud.top/talaria/) | Polish — VFX, SFX, HUD, Arena Scene         | [120](#task-120) | Sugar Rush Polish — Rush Bar + ×N Badge |
| [077](https://dev.klud.top/talaria/) | Cleanser Icon                               | [121](#task-121) | Ghost Charge Icon |
| [078](https://dev.klud.top/talaria/) | Slow-Mo (¼ speed, 4 s)                      | [122](#task-122) | Sugar Rush Speed ×2 (2 s base + 1.2× per candy) |
| [079](https://dev.klud.top/talaria/) | Screenshake Follows Player                  | keep  | — |
| [080](https://dev.klud.top/talaria/) | Disable Default Powerups Except Smack       | [130](#task-130) | Spawn gear: 5 Knock OR 5 Ghost |
| [081](https://dev.klud.top/talaria/) | Telegraph Floor Highlight                   | [123](#task-123) | Mekton Color Beacon (face-color highlight) |
| [082](https://dev.klud.top/talaria/) | Candy Bubble System                         | [124](#task-124) | Head-stack delivery bubble (carry/transfer) |
| [083](https://dev.klud.top/talaria/) | Movement Buffer System                      | [125](#task-125) | Auto Tile Pickup Pathing |
| —     | —                                           | [126](#task-126) | Mekton Cheerleaders (TBD) |
| —     | —                                           | [127](#task-127) | Head Stack Multiplier + ×N Badge UI |
| —     | —                                           | [128](#task-128) | Mekton Delivery Rules (matching-color only) |
| —     | —                                           | [129](#task-129) | Half-Point Penalty for Off-Color Finish |
| —     | —                                           | [131](#task-131) | Self-Knock Rebound (no-candy target) |
| —     | —                                           | —               | *(Mekton Bulls has its own game-mode task chain `#134`–`#145`; see [the Mekton Bulls section](#mekton-bulls-new-top-level-game-mode-134145))* |

Grep confirms `sugar_rush`, `mekton_bull`, `shrinking_arena` return
**0 hits** anywhere in `tekton-enet/scripts/` — every new task is unimplemented.

### Sugar Rush design spec

#### Arena

- **18 × 18** grid (vs. the 20 × 20 shipped in `gauntlet_manager.gd`).
- Blueprints are **single-color focused**.
- **Automatic tile pickup** — no input needed; walking over a matching tile
  counts it.
- If your blueprint's color runs out, finish it with any other color, but
  you only earn **½ points** for that blueprint.

#### Candies on Your Head

- Finishing a blueprint drops a candy on your head in the matching color.
- **No carry cap** — stack as many as you can carry.
- Candies grant **points every second**. The more you stack, the **bigger
  the multiplier** on points earned.
- A `×2` (or current multiplier) badge must render next to the Mekton head
  sprite so opponents see the threat.

#### Mekton Delivery

- The Mekton's face changes color on a timer.
- You can only deliver candies whose color matches the Mekton's **current**
  face color.
- A successful delivery = **big point payout**.
- Mismatched candies stay on your head (no penalty, no delivery).

#### Sugar Rush Mutator

Feeding a candy to the Mekton triggers **Sugar Rush**:

| Parameter        | Value                          |
| ---------------- | ------------------------------ |
| Base rush time   | 2 s                            |
| Multiplier       | ×1.2 per candy in the batch    |
| Example          | 5 candies × 1.2 = 4 s of rush  |
| Effect           | Game speed ×2 — projectiles, dashers, AI, all timers |
| Visual           | Rush bar turns red while active |
| Stacking limit   | **TBD**                        |

#### Knock & Ghost Charges

Every player spawns with **5 knock charges OR 5 ghost charges** (your pick).

- **Knock** — shove another player. If they carry candies, **you steal them
  all** and they stack onto your pile.
- **Ghost (4 s)** — walk through candies freely and **cannot be knocked**.
- **Self-knock rule** — knocking a player who carries no candies rebounds:
  **you get knocked instead**.

#### Sticky Floor

Sticky material is **pure collision** — it acts like a wall. Standing in it
is the same as standing on a hard tile: trapped, no pickup, no movement.

#### Mekton Cheerleaders (TBD)

Cheerleaders stand **outside** the board. Each player picks one during
lobby. They activate only when you are **low on the leaderboard**.
Per-cheerleader buffs are still TBD.

---

## Mekton Bulls (New top-level game mode — `#134`–`#145`)

> Mekton Bulls is a Talaria game mode. 2-minute-or-less matches built on
> placement scoring inside a shrinking arena with a roaming bull.

A second mode in the same family as Sugar Rush, but a **peer** — it has
its own enum entry (`GameMode.MEKTON_BULLS = 4`), its own
`MektonBullsManager`, its own lobby string, and shares zero gameplay
rules with Sugar Rush. Tracking lives under `#134`–`#145`; structural
skeleton (`#134`) is `progress`, the rest are `todo` and gated on it.

### Game-Mode Separation Pattern (how Talaria splits modes)

Mirroring how `Freemode / Stop n Go / Tekton Doors / Gauntlet` are
separated today, each Talaria mode owns its own manager node and is
selected via the `GameMode` enum + `LobbyManager.game_mode` string.
`scenes/main.gd` dispatches on the string and conditionally creates the
matching manager. `Freemode` is the baseline with no manager.

| Mode            | Enum                    | Manager                | Arena rules               | Scoring          |
| --------------- | ----------------------- | ---------------------- | ------------------------- | ---------------- |
| Freemode        | `FREEMODE = 0`          | (none — baseline)      | Open arena                | Free             |
| Stop n Go       | `STOP_N_GO = 1`         | `StopNGoManager`       | Phase-based stops         | Phase timer      |
| Tekton Doors    | `TEKTON_DOORS = 2`      | `PortalModeManager`    | Portal-driven             | Portal capture   |
| Gauntlet / Sugar Rush | `GAUNTLET = 3`   | `GauntletManager`      | 18 × 18 sticky growth     | Per-second + delivery |
| **Mekton Bulls** | **`MEKTON_BULLS = 4`** | **`MektonBullsManager`** | **Shrinking arena, bulls** | **Placement** |

Mekton Bulls is its own mode, not a Sugar-Rush sub-flag, because:

- The arena lifetime is different (shrinks mid-match).
- The scoring system is different (placement, not points-per-time).
- The hazard is different (roaming bull, not sticky growth).
- The manager has **zero** code overlap with `GauntletManager`.

Folding it into Gauntlet would couple two different games behind a
boolean flag — the shipped pattern (one manager per game mode) is the
correct mirror.

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

## Migration Task List

Each row is a tracked task under `tasks/`. Open one for full acceptance
criteria.

### Mode & Arena

- <a id="task-111"></a>**#111 Sugar Rush Mode Registration** — replace
  the `"Candy Pump Survival"` display string with `"Sugar Rush"` and
  document the new mode identity. `supersedes_part_of(#065)`.
- <a id="task-112"></a>**#112 Sugar Rush Arena Setup 18 × 18** — change
  `ARENA_COLUMNS`, `ARENA_ROWS`, `NPC_CENTER`, and the boundary loop.
  `supersedes_part_of(#066)`.

### Tick & Phases

- <a id="task-113"></a>**#113 Candy Stack Growth Tick** — replace
  `_process_growth_tick()` with a per-second candy-stack tick that grows
  the head stack when standing on a matching tile. `supersedes(#067)`.
- <a id="task-115"></a>**#115 Sugar Rush Stacking** — replace growth-phase
  escalation with rush-stacking logic. `supersedes(#070)`.

### Telegraph → Mekton Color

- <a id="task-114"></a>**#114 Mekton Color Rotation Telegraph** — replace
  telegraph VFX with face-color rotation. `supersedes(#069)`.
- <a id="task-123"></a>**#123 Mekton Color Beacon** — replace floor
  telegraph highlight with a Mekton-face color beacon. `supersedes(#081)`.

### Knock / Ghost / Spawn Gear

- <a id="task-116"></a>**#116 Knock Charge System** — convert Smack into a
  5-charge spawn gear that steals head-stack candies. `supersedes(#071)`.
- <a id="task-117"></a>**#117 Ghost Charge (4 s)** — replace Cleanser with a
  5-charge, 4-second pass-through immunity. `supersedes(#072)`.
- <a id="task-121"></a>**#121 Ghost Charge Icon** — replace Cleanser icon
  with the Ghost Charge icon. `supersedes(#077)`.
- <a id="task-130"></a>**#130 Spawn Gear: 5 Knock OR 5 Ghost** — give
  each player exactly one of the two gears on spawn. `supersedes(#080)`.
- <a id="task-131"></a>**#131 Self-Knock Rebound** — knocking a player with
  no head-stack bounces the knock back at the attacker. new feature.

### Bot AI & Pathing

- <a id="task-118"></a>**#118 Bot AI for Candy Survival** — bot
  pathfinding that prefers candy-rich tiles, avoids dangerous players,
  and times deliveries to Mekton color. `supersedes(#073, #075)`.
- <a id="task-119"></a>**#119 Single-Color Blueprint Auto-Pickup** —
  rework mission tiles into single-color blueprints with automatic pickup.
  `supersedes(#074)`.
- <a id="task-125"></a>**#125 Auto Tile Pickup Pathing** — replace
  movement-buffer penalties with an auto-pickup-aware path cost.
  `supersedes(#083)`.

### Head Stack & Delivery

- <a id="task-127"></a>**#127 Head Stack Multiplier + ×N Badge UI** —
  render the running `×N` multiplier next to the Mekton head sprite.
  new feature.
- <a id="task-128"></a>**#128 Mekton Delivery Rules** — only matching-color
  candies deliver; mismatches stay on the head. new feature.
- <a id="task-129"></a>**#129 Half-Point Penalty for Off-Color Finish** —
  award ½ points when a blueprint is finished with a non-matching color.
  new feature.
- <a id="task-124"></a>**#124 Head-Stack Delivery Bubble** — convert the
  candy-bubble spawner into a delivery-triggered VFX/SFX burst.
  `supersedes_part_of(#082)`.

### Mutator & Feedback

- <a id="task-122"></a>**#122 Sugar Rush Speed ×2** — replace slow-mo
  (¼ speed, 4 s) with Sugar Rush (×2 speed, 2 s base × 1.2 per candy).
  `supersedes(#078)`.
- <a id="task-120"></a>**#120 Sugar Rush Polish — Rush Bar + ×N Badge** —
  fold the remaining polish work onto Sugar Rush visuals.
  `supersedes(#076)`.

### Cheerleaders

- <a id="task-126"></a>**#126 Mekton Cheerleaders (TBD)** — design
  per-cheerleader buffs and the low-leaderboard activation hook.
  new feature (TBD).

### Mekton Bulls (`#134`–`#145`)

- <a id="task-134"></a>**#134 Mekton Bulls: Game Mode Registration** —
  `progress`. The structural skeleton: enum entry, `LobbyManager`
  string, area mapping, `MektonBullsManager` node, `main.gd` dispatch
  hooks. All other Mekton Bulls tasks are `blocked_by: ["134"]`.
- <a id="task-135"></a>**#135 Mekton Bulls: Arena Setup & Phase Shrinker**
  — 20 × 20 → 19 → 18 → 17 phase shrinks.
- <a id="task-136"></a>**#136 Mekton Bulls: Big Mekton Bull Spawner + Roam AI**
  — bull entity that roams and charges players.
- <a id="task-137"></a>**#137 Mekton Bulls: Water Flood Outer Ring** —
  bull-on-boundary floods the outermost ring; players there die.
- <a id="task-138"></a>**#138 Mekton Bulls: 3 × 3 Blueprint Auto-Pickup**
  — small 3 × 3 blueprints with automatic pickup.
- <a id="task-139"></a>**#139 Mekton Bulls: Power Reward — Freeze OR Knock**
  — 1 power per blueprint completion (Freeze slow or Knock shove).
- <a id="task-140"></a>**#140 Mekton Bulls: Placement-Scored Point System**
  — static min/max points; first out = min, last standing = max,
  middle = linear interpolation.
- <a id="task-141"></a>**#141 Mekton Bulls: Bot AI (Bull Avoidance + Knock Steal Pathing)**
  — bot pathing that avoids the bull and times Freeze/Knock pickups.
- <a id="task-142"></a>**#142 Mekton Bulls: Player Knock (Mutual Knockback)**
  — players knock each other (1 cell shove; chains into water or bull).
- <a id="task-143"></a>**#143 Mekton Bulls: HUD — Bull Tracker, Power Picker, Placement**
  — bull-tracker arrow, freeze/knock power picker, end-of-match
  placement overlay.
- <a id="task-144"></a>**#144 Mekton Bulls: Polish — Bull SFX + Knock Burst**
  — bull charge/impact SFX, freeze VFX, water-flood splash, knock
  burst.
- <a id="task-145"></a>**#145 Mekton Bulls: Round Timer & Phase Auto-Advance**
  — ≤ 2 min round, auto phase advance every 30 s, early-end on
  last survivor.

---

## Untouched Gauntlet Tasks

These shipped tasks remain unchanged and continue to apply to Sugar Rush:

- [068](https://dev.klud.top/talaria/) — Sticky Cell System (kept on the floor).
- [079](https://dev.klud.top/talaria/) — Screenshake Follows Player (kept as-is).