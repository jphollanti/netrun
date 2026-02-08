# Codebase Structure Review: Netrun

**Project**: Cyberpunk text adventure game (~3,100 lines of Python)

## Current Structure

```
netrun/
├── mloop.py              # Main game loop (entry point)
├── state.py              # Game state singleton + constants
├── player.py             # Player data + deck definitions
├── levelgen.py           # Procedural level generation + visualization
├── cool_print.py         # Terminal UI effects engine
├── n_in_row.py           # Path-crossing puzzle minigame
└── node/
    ├── node.py           # Node factory + registry
    ├── battle.py         # Combat engine
    ├── jack_in.py        # Entry node
    ├── black_ice.py      # Offensive ICE encounters
    ├── white_ice.py      # Defensive ICE encounters
    ├── firewall.py       # Firewall node
    ├── competing_netrunner.py  # PvP encounter
    ├── mainframe.py      # Docker-based terminal simulation
    ├── data_core.py      # Hex grid puzzle
    ├── trace_program.py  # Stub
    └── signal_interference.py  # Stub
```

## Verdict: The structure is reasonable for the project's size

For ~3,100 lines and a single-developer game, this layout is workable.
The `node/` package separation is the right call. A major restructuring
would be over-engineering at this scale.

However, several concrete issues are worth addressing:

## Issues Worth Fixing

### 1. `sys.path` hacking in every node file

Every file under `node/` does this:

```python
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from cool_print import cool_print
```

Repeated in: `battle.py`, `black_ice.py`, `white_ice.py`, `competing_netrunner.py`,
`mainframe.py`, `data_core.py`.

This is unnecessary because the game is always run from the project root via
`python mloop.py`, which puts the root on `sys.path` already. These blocks
can be removed entirely -- the bare `from cool_print import cool_print` will work.

### 2. `state.py` mixes concerns

`state.py` contains three distinct things:
- Global constants (`WIDTH`, `HEIGHT`, `WAYPOINTS`)
- The `MainState` singleton class
- A standalone function `get_sections_of_path()` that sits outside the class

`get_sections_of_path()` is a pure utility function about path geometry that doesn't
touch state at all. It logically belongs in `levelgen.py` since that's where paths
are created and understood.

### 3. `player.py` has orphaned functions

`player.py` defines `slow_down()`, `logged()`, and `watch_dogged()` as module-level
functions, but `state.py` has methods with the same names on `MainState`. The
`player.py` versions use `print()` instead of `cool_print()` and appear to be
leftover earlier implementations. They should be removed if unused.

### 4. `node/node.py` factory could use a dictionary registry

The long if/elif chain is fine for 7 types, but a dictionary registry would be cleaner:

```python
_registry = {
    'Jack-In': jack_in.jack_in,
    'Black ICE': black_ice.black_ice,
    # ...
}

def generate_node(type):
    if type not in _registry:
        raise Exception(f"Unknown node type: {type}")
    return _registry[type]
```

### 5. `levelgen.py` does two unrelated things

It handles both level generation (`generate_new_state`) and map visualization
(`visualize`). These are separate responsibilities that could be clearly
separated or split into two modules.

### 6. Duplicate imports

- `competing_netrunner.py` has `import random` twice
- `mainframe.py` imports `datetime, timedelta` twice
- `data_core.py` imports `os` twice

### 7. `white_ice.py` has an inconsistency that will cause crashes

The `Netwatch Scout` uses the `battle()` system with `actions` and `initiative`
keys, while the other five (Gatekeeper, Watchdog, etc.) use standalone `_action()`
functions and an `action` key (singular). Since `white_ice()` always calls
`battle.battle()`, picking any non-Scout ICE will crash because those lack the
required `initiative`, `actions`, and `greeting` fields.

### 8. No `__init__.py` in `node/`

The `node/` directory functions as a package but lacks an explicit `__init__.py`.
This works in some configurations but having one makes the package contract clear.

### 9. Missing `requirements.txt`

Dependencies (`colorama`, `getch`, `docker`) are not documented anywhere.

## What's Working Well

- **The `node/` package**: Good separation. Encounters are the most likely growth
  area, and per-file modularity makes them independently editable.
- **The `cool_print` module**: Self-contained with clean interfaces (delay providers
  as callables). Complex but focused on one job.
- **The singleton `MainState`**: Pragmatic for single-threaded, single-player flow.
  JSON persistence is simple and appropriate.
- **The factory pattern** in `node.py`: Keeps node creation decoupled from the main loop.

## If the project grows significantly (10k+ lines)

Only then would reorganizing into sub-packages make sense:

```
netrun/
├── main.py
├── config.py               # Constants
├── state.py                # Game state only
├── player.py
├── ui/
│   ├── cool_print.py
│   └── map_renderer.py     # Extracted from levelgen
├── world/
│   ├── levelgen.py
│   └── pathfinding.py
├── encounter/
│   ├── registry.py
│   ├── battle.py
│   ├── black_ice.py
│   ├── white_ice.py
│   ├── firewall.py
│   ├── competing_netrunner.py
│   ├── mainframe.py
│   └── data_core.py
└── puzzle/
    └── n_in_row.py
```

At current scale, this would be premature.

## Priority Fixes

1. Fix the `white_ice.py` crash (most impactful -- this is a bug)
2. Remove `sys.path` hacks from node files
3. Add `requirements.txt`
4. Clean up duplicate imports and orphaned functions in `player.py`
