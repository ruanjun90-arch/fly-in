*This project has been created as part of the 42 curriculum by juruan.*

## Description

Fly-in is a drone routing system. Given a map file describing a network of
zones connected by bidirectional links, it routes a fleet of drones from a
start zone to an end zone in as few simulation turns as possible, while
respecting zone capacities, connection capacities, and special zone types
(blocked, restricted, priority).

## Instructions
​```
- make install        # install dependencies with uv
- make run            # run the simulation
- make debug          # run under pdb
- make lint           # flake8 + mypy
- make clean          # remove caches
​```

### Parser

The parser is fully object-oriented: a `Parser` class builds a `Map` made of `Zone`, `Connection`, and a `ZoneType` enum.

Key design decisions:
- Lines are read through a context manager; comments and blank lines are skipped, and the original line number is kept for error messages.
- `nb_drones` is validated once, up front, before the main loop.
- Validation is placed where the data is: per-line checks (coordinates, dashes in names, capacities, zone types, metadata brackets) live in the parsing methods; global checks (exactly one start/end) are split — duplicates caught while parsing, absence caught after the loop.
- `frozenset` connection keys make `a-b` and `b-a` count as the same link.
- The `ZoneType` enum validates zone types for free.
- Every parsing error stops with a clear message and the line number.

### Simulation & Pathfinding
<!-- TODO: fill in once implemented -->

## Visual Representation
- maps/easy/01_linear_path.txt
- maps/easy/02_simple_fork.txt
- maps/easy/03_basic_capacity.txt
- maps/medium/01_dead_end_trap.txt
- maps/medium/02_circular_loop.txt
- maps/medium/03_priority_puzzle.txt
- maps/hard/01_maze_nightmare.txt
- maps/hard/02_capacity_hell.txt
- maps/hard/03_ultimate_challenge.txt
- maps/challenger/01_the_impossible_dream.txt

## Resources

- BFS / graph traversal
- Python docs (dataclasses, enum, typing)
- https://docs.python.org/zh-cn/3.14/library/heapq.html

### Use of AI

AI was used as a learning and reviewing aid for the parser, not as a code generator：
- to clarify concepts I was unsure about (string indexing vs unpacking, narrow `try` blocks, referential integrity specification vs implementation);
- to review my code and help me locate the *cause* of bugs — without being handed the fixes, so I worked them out myself;
- to discuss validation strategy and edge cases.

Every line of code was written and debugged by me, and I can explain the reasoning behind each validation rule.
