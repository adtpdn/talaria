---
title: "Refactor player.gd (Large Class)"
id: "021"
status: todo
priority: 01
sprint: beta
category: CORE
description: "Refactor player.gd to reduce complexity. Extract input, movement, animation, and networking into separate classes."
---
## Overview

Refactor player.gd to reduce complexity and improve maintainability.

## Current Issues

- Large class with too many responsibilities
- High cyclomatic complexity
- Mixed concerns (input, movement, animation, networking)
- Difficult to test
## Scope

- Extract input handling into separate class
- Extract movement logic into separate class
- Extract animation control into separate class
- Extract network sync into separate class
- Reduce method complexity
## Acceptance Criteria

- [ ] Class size reduced by 50%+
- [ ] Single Responsibility Principle followed
- [ ] Cyclomatic complexity reduced
- [ ] Unit tests added
- [ ] No regression in functionality
