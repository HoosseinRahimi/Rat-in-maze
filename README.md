# Rat in a Maze: Pathfinding Algorithms

[![Tests](https://github.com/HoosseinRahimi/Rat-in-maze/actions/workflows/tests.yml/badge.svg)](https://github.com/HoosseinRahimi/Rat-in-maze/actions/workflows/tests.yml)

A Python project for solving grid mazes with four different search strategies:

- **Breadth-First Search (BFS)**
- **A\*** with Manhattan-distance heuristic
- **Depth-First Search (DFS)**
- **Backtracking** to enumerate all simple paths

The maze uses `1` for an open cell and `0` for a blocked cell. Movement is allowed in four directions: down, up, left, and right.

## Why Compare These Algorithms?

The same maze highlights important differences between search strategies:

| Algorithm | Finds a path | Guaranteed shortest | Typical use |
|---|:---:|:---:|---|
| BFS | Yes | Yes | Unweighted shortest paths |
| A* | Yes | Yes* | Goal-directed shortest paths |
| DFS | Yes | No | Reachability and traversal |
| Backtracking | Yes | By enumeration | Exploring every simple solution |

`*` In this project, A* uses Manhattan distance on a four-directional grid with unit edge costs. That heuristic is admissible and consistent, so the first optimal goal state removed from the priority queue gives a shortest path.

## Improvements in This Version

- Correct A* `g` and `f = g + h` cost handling
- Proper best-cost tracking instead of marking nodes visited too early
- Correct messaging: DFS is no longer described as a shortest-path algorithm
- Standard Python filename: `rat_in_maze.py`
- No NumPy dependency; random maze generation uses the Python standard library
- Input validation for maze shape, cell values, and endpoints
- Reusable functions that can be imported without starting the interactive program
- Automated regression tests

## Run

No third-party packages are required.

```bash
python rat_in_maze.py
```

The program asks for:

1. maze dimensions
2. a custom or randomly generated maze
3. start and end coordinates
4. the search algorithm

For a custom maze, separate cells with spaces and rows with semicolons. Example:

```text
1 1 0 1;0 1 1 1;1 1 0 1;1 1 1 1
```

## Path Encoding

Returned paths are strings composed of:

- `D` → down
- `U` → up
- `L` → left
- `R` → right

Example:

```text
DRRDDD
```

## Use as a Module

```python
from rat_in_maze import a_star, bfs

maze = [
    [1, 1, 0, 1],
    [0, 1, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
]

start = (0, 0)
end = (3, 3)

print(bfs(maze, start, end))
print(a_star(maze, start, end))
```

Both BFS and A* return a shortest path if one exists. Their exact path strings can differ when multiple shortest routes have the same length.

## Correctness Notes

### BFS

BFS processes positions in nondecreasing distance from the start. Because every move has cost `1`, the first time the goal is removed from the queue its path has the minimum possible number of moves.

### A*

For a cell `n`, A* prioritizes:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the shortest discovered cost from the start to `n`
- `h(n)` is Manhattan distance from `n` to the goal

A single grid move changes Manhattan distance by at most one, so `h` is consistent. With unit edge costs, A* therefore returns an optimal path when the goal is popped with its best recorded `g` value.

### DFS

DFS explores one branch deeply before backtracking. It finds a path when a reachable goal exists, but it does **not** guarantee the shortest one.

### Backtracking

Backtracking marks the current path as visited, explores every unvisited neighbour, and unmarks the current position when returning. Therefore it enumerates all simple start-to-goal paths. Its worst-case running time is exponential, so it is intended for small mazes.

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- BFS shortest-path length
- A* matching BFS shortest-path length
- multiple fixed mazes
- DFS path validity
- unreachable goals
- `start == end`
- backtracking enumeration
- custom maze validation
- deterministic random-maze generation

## Complexity

Let `V` be the number of open cells and `E` the number of valid neighbour connections.

- **BFS:** `O(V + E)` time, `O(V)` search memory, excluding returned path-string copies
- **DFS:** `O(V + E)` time, `O(V)` search memory
- **A*:** up to `O((V + E) log V)` with a binary heap
- **Backtracking:** exponential in the worst case because it can enumerate exponentially many simple paths

## License

See [`LICENSE`](LICENSE).