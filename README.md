*This project has been created as part of the 42 curriculum by juruan.*

# Fly-in — Drone Routing System

## Description

Fly-in is a drone fleet routing simulator written in Python. Given a network of
connected zones with various constraints (capacity limits, restricted areas,
blocked zones), the program finds efficient paths and schedules the movement of
multiple drones from a start hub to an end hub, minimizing the total number of
simulation turns.

The project is fully object-oriented, type-safe (validated with `flake8` and
`mypy`), and includes both terminal output and a graphical visualization using
`matplotlib`.

## Features

- **Custom map parser** with detailed error reporting (line number and cause)
- **Dijkstra's algorithm** for weighted shortest-path computation
- **Yen's K-Shortest Paths** for multi-path discovery with cost-based filtering
- **Conflict-aware scheduler** handling zone capacity, link capacity, and
  restricted zone transit
- **Matplotlib visualization** showing drone movements across the network in
  real time

## Instructions

### Prerequisites

- Python 3.10 or later
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
make install
```

### Running the simulation

```bash
make run
```

The program will ask you to select a map file from the available options.

### Debugging

```bash
make debug
```

Launches the program with Python's built-in debugger (`pdb`).

### Linting

```bash
make lint          # flake8 + mypy standard checks
make lint-strict   # flake8 + mypy --strict
```

### Cleaning

```bash
make clean
```

Removes `__pycache__` and `.mypy_cache` directories.

## Project Structure

```
fly-in/
├── Makefile
├── README.md
├── src/
│   ├── __init__.py
│   ├── __main__.py      # Entry point and map selection
│   ├── model.py          # Data models (Zone, Connection, Map, ZoneType)
│   ├── parser.py         # Map file parser with error handling
│   ├── pathfinding.py    # BFS, Dijkstra, Yen's K-Shortest Paths
│   ├── scheduler.py      # Turn-by-turn drone movement simulation
│   ├── output.py         # Terminal output and matplotlib visualization
│   └── error.py          # Custom ParsingError exception
└── maps/
    ├── easy/
    ├── medium/
    ├── hard/
    └── challenger/
```

## Algorithm Choices and Implementation Strategy

### Pathfinding: Dijkstra with Yen's Extension

The core pathfinding uses **Dijkstra's algorithm** with a priority queue
(`heapq`), accounting for zone-type movement costs:

- **Normal** zones: cost 1
- **Priority** zones: cost 1 (preferred by the algorithm due to equal cost
  with fewer conflicts)
- **Restricted** zones: cost 2 (two-turn transit through the connection)
- **Blocked** zones: excluded from pathfinding entirely

To support multi-path routing, the implementation extends Dijkstra with a
simplified **Yen's K-Shortest Paths** approach. The algorithm works by
iteratively blocking individual edges along the shortest path and re-running
Dijkstra to discover alternative routes. Each candidate path is evaluated
using `compute_path_cost`, and only paths within a cost threshold (1.3× the
shortest path cost) are retained. This prevents drones from being assigned
to inefficient detours that would increase total simulation turns.

#### Why not full multi-path distribution?

During development, I experimented with evenly distributing drones across all
discovered paths (round-robin assignment). Testing revealed that this approach
often **increased** total turns rather than reducing them. The reason: on maps
with a single structural bottleneck (e.g., one restricted exit point), all
paths converge at the same chokepoint. Sending drones on longer alternative
routes only delays their arrival without relieving congestion at the bottleneck.

The final strategy assigns approximately 75% of drones to the shortest path
and 25% to the second-best alternative (when available), achieving a balance
between path diversity and throughput efficiency.

### Scheduling: Greedy Turn-by-Turn Simulation

The scheduler processes each turn by:

1. **Landing in-transit drones** — drones that entered a restricted zone
   connection in the previous turn complete their arrival.
2. **Moving available drones** — for each drone not yet at the end zone,
   the scheduler checks zone capacity (`max_drones`), link capacity
   (`max_link_capacity`), and restricted zone rules before authorizing
   movement.
3. **Handling restricted zones** — when a drone moves toward a restricted
   zone, it spends one turn on the connection (output: `D1-zoneA-zoneB`)
   and arrives the next turn (output: `D1-zoneB`).

The scheduler uses a `Counter` to track real-time zone occupancy and a
`link_usage` dictionary to enforce per-turn connection capacity limits.
Drones moving out of a zone free up capacity within the same turn.

### Considered but not implemented

- **A\* algorithm**: Dijkstra with a heuristic (Manhattan distance to goal).
  Would speed up pathfinding on large maps, but the current maps are small
  enough that Dijkstra runs instantly. The zone coordinates in the map files
  would serve as the heuristic basis.
- **CBS (Conflict-Based Search)**: A multi-agent pathfinding algorithm that
  resolves conflicts through constraint branching. Too complex for the
  current project scope but worth exploring for optimal multi-drone routing.

## Visual Representation

The project provides two forms of output:

### Terminal Output

Each simulation turn is printed as a single line listing all drone movements:

```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```

Drones in transit toward restricted zones show the connection:
`D3-zoneA-zoneB` (in transit), then `D3-zoneB` (arrived next turn).

### Graphical Visualization (matplotlib)

The `visualization()` method in `output.py` renders:

- **Zones** as colored squares, positioned by their (x, y) coordinates
- **Connections** as grey dotted lines between zones
- **Drones** as grey star markers with labels (D1, D2, ...) that update
  each turn with a 2-second pause

Drones in transit toward restricted zones are displayed at the midpoint of
the connection. The visualization runs after the terminal output, allowing
the user to observe the complete simulation flow.

## Resources

### References

- [Dijkstra's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Yen's K-Shortest Paths — Wikipedia](https://en.wikipedia.org/wiki/Yen%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [Python `dataclasses` documentation](https://docs.python.org/3/library/dataclasses.html)
- [matplotlib documentation](https://matplotlib.org/stable/contents.html)

### AI Usage

AI (Claude by Anthropic) was used as a **learning companion** throughout the
project for the following tasks:

- **Conceptual explanations**: Understanding Dijkstra's algorithm, Yen's
  K-Shortest Paths, A\*, and CBS through analogies and step-by-step
  walkthroughs.
- **Debugging guidance**: When errors occurred, AI helped identify the root
  cause by asking guiding questions rather than providing direct solutions.
- **Code review**: AI reviewed code for potential issues such as variable
  shadowing, type mismatches, and logical errors.
- **Algorithm comparison**: AI helped evaluate trade-offs between different
  multi-path strategies (simple edge removal vs. Yen's vs. CBS) and
  distribution approaches (round-robin vs. cost-weighted).

All code was written, tested, and debugged by the author. AI was not used
to generate complete functions or modules.
