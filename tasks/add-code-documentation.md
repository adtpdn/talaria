---
title: "Add Code Documentation"
id: "015"
status: todo
priority: 02
sprint: beta
category: CORE
description: "Comprehensive GDScript documentation following Godot conventions for classes, methods, and parameters."
---

# Add Code Documentation

## Problem
The codebase lacks structured documentation for classes, methods, and parameters. This creates a high barrier to entry for new developers, increases the risk of misuse of complex methods (e.g., `GachaManager.pull`), and makes maintaining the project difficult as the original context of implementation is lost.

## Solution
Implement a comprehensive documentation standard using GDScript comments (`##`) that can be parsed by documentation generators.

### Documentation Standards
- **Class Summaries:** High-level explanation of the class's purpose and responsibility.
- **Method Signatures:** Detailed documentation for every public method using `@param` and `@return` tags.
- **Usage Examples:** Concrete `## @example` blocks for complex systems (e.g., `pull`, `sync_state`, `initialize_astar`).
- **Signal Documentation:** Document the exact event that triggers each signal and the meaning of its parameters.

## Benefits
- **Onboarding:** Significantly reduces the time required for new contributors to become productive.
- **Reliability:** Prevents bugs caused by misunderstood method side-effects or invalid parameter values.
- **Knowledge Base:** Enables automatic generation of a searchable HTML API reference site in `docs/api/`.

## Acceptance Criteria
- **Class Coverage:** 100% of high-priority manager classes must have a header explaining their purpose.
- **Method Coverage:** Every public method in core managers must have descriptions, `@param` tags, and `@return` tags.
- **Example Quality:** Complex methods must include a realistic call example and expected result.
- **Tooling Verification:** Running `gdscript-docs-maker` produces a complete, error-free HTML reference.
- **Accessibility:** The project `README.md` contains a working link to the generated API documentation.

## Migration Checklist
- [ ] Apply `##` comment style to all files in `scripts/managers/` and `scripts/services/`.
- [ ] Document high-priority managers: `auth_manager.gd`, `nakama_manager.gd`, `user_profile_manager.gd`, `gacha_manager.gd`, `backend_service.gd`, and `game_state_manager.gd`.
- [ ] Document medium-priority managers: `friend_manager.gd`, `lobby_manager.gd`, `player_manager.gd`, `settings_manager.gd`, and `skin_manager.gd`.
- [ ] Install and verify `gdscript-docs-maker` tool.
- [ ] Generate the API reference and verify output.
- [ ] Spot-check 5 random complex methods for accuracy.
