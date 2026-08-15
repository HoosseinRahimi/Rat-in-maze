from __future__ import annotations

import heapq
import random
from collections import deque
from collections.abc import Iterable, Sequence

Maze = Sequence[Sequence[int]]
Point = tuple[int, int]

DIRECTIONS: tuple[tuple[str, int, int], ...] = (
    ("D", 1, 0),
    ("U", -1, 0),
    ("L", 0, -1),
    ("R", 0, 1),
)


def maze_shape(maze: Maze) -> tuple[int, int]:
    if not maze or not maze[0]:
        raise ValueError("maze must contain at least one row and one column")

    rows = len(maze)
    cols = len(maze[0])
    if any(len(row) != cols for row in maze):
        raise ValueError("maze must be rectangular")
    if any(cell not in (0, 1) for row in maze for cell in row):
        raise ValueError("maze cells must be 0 (blocked) or 1 (open)")
    return rows, cols


def is_valid(row: int, col: int, maze: Maze) -> bool:
    rows, cols = maze_shape(maze)
    return 0 <= row < rows and 0 <= col < cols and maze[row][col] == 1


def heuristic(point: Point, goal: Point) -> int:
    """Manhattan distance for four-directional unit-cost movement."""
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


def _validate_endpoints(maze: Maze, start: Point, end: Point) -> None:
    maze_shape(maze)
    if not is_valid(*start, maze):
        raise ValueError(f"start point {start} is outside the maze or blocked")
    if not is_valid(*end, maze):
        raise ValueError(f"end point {end} is outside the maze or blocked")


def _neighbors(point: Point, maze: Maze) -> Iterable[tuple[str, Point]]:
    row, col = point
    for move, delta_row, delta_col in DIRECTIONS:
        next_point = (row + delta_row, col + delta_col)
        if is_valid(*next_point, maze):
            yield move, next_point


def dfs(maze: Maze, start: Point, end: Point) -> str | None:
    """Return one path found by depth-first search, or ``None`` if unreachable."""
    _validate_endpoints(maze, start, end)

    stack: list[tuple[Point, str]] = [(start, "")]
    visited = {start}

    while stack:
        point, path = stack.pop()
        if point == end:
            return path

        for move, next_point in _neighbors(point, maze):
            if next_point not in visited:
                visited.add(next_point)
                stack.append((next_point, path + move))

    return None


def bfs(maze: Maze, start: Point, end: Point) -> str | None:
    """Return a shortest path in an unweighted maze, or ``None`` if unreachable."""
    _validate_endpoints(maze, start, end)

    queue: deque[tuple[Point, str]] = deque([(start, "")])
    visited = {start}

    while queue:
        point, path = queue.popleft()
        if point == end:
            return path

        for move, next_point in _neighbors(point, maze):
            if next_point not in visited:
                visited.add(next_point)
                queue.append((next_point, path + move))

    return None


def a_star(maze: Maze, start: Point, end: Point) -> str | None:
    """Return a shortest path using A* with a Manhattan-distance heuristic."""
    _validate_endpoints(maze, start, end)

    frontier: list[tuple[int, int, Point, str]] = [
        (heuristic(start, end), 0, start, "")
    ]
    best_cost: dict[Point, int] = {start: 0}

    while frontier:
        _, cost, point, path = heapq.heappop(frontier)

        # Ignore stale heap entries superseded by a cheaper route.
        if cost != best_cost.get(point):
            continue

        if point == end:
            return path

        for move, next_point in _neighbors(point, maze):
            next_cost = cost + 1
            if next_cost < best_cost.get(next_point, float("inf")):
                best_cost[next_point] = next_cost
                priority = next_cost + heuristic(next_point, end)
                heapq.heappush(
                    frontier,
                    (priority, next_cost, next_point, path + move),
                )

    return None


def all_simple_paths(maze: Maze, start: Point, end: Point) -> list[str]:
    """Enumerate every simple path. This can be exponential for large mazes."""
    _validate_endpoints(maze, start, end)

    answers: list[str] = []
    visited: set[Point] = set()

    def backtrack(point: Point, path: str) -> None:
        if point == end:
            answers.append(path)
            return

        visited.add(point)
        for move, next_point in _neighbors(point, maze):
            if next_point not in visited:
                backtrack(next_point, path + move)
        visited.remove(point)

    backtrack(start, "")
    return answers


def apply_path(start: Point, path: str) -> list[Point]:
    """Decode a path string into the visited coordinates, including the start."""
    row, col = start
    positions = [(row, col)]
    deltas = {move: (dr, dc) for move, dr, dc in DIRECTIONS}

    for move in path:
        if move not in deltas:
            raise ValueError(f"unknown path move: {move!r}")
        dr, dc = deltas[move]
        row += dr
        col += dc
        positions.append((row, col))

    return positions


def render_maze_with_path(maze: Maze, path: str, start: Point, end: Point) -> str:
    path_positions = set(apply_path(start, path))
    lines: list[str] = []

    for row_index, row in enumerate(maze):
        rendered_row: list[str] = []
        for col_index, cell in enumerate(row):
            point = (row_index, col_index)
            if point == start:
                rendered_row.append("S")
            elif point == end:
                rendered_row.append("E")
            elif point in path_positions:
                rendered_row.append("*")
            else:
                rendered_row.append(str(cell))
        lines.append(" ".join(rendered_row))

    return "\n".join(lines)


def generate_random_maze(
    rows: int,
    cols: int,
    *,
    open_probability: float = 0.7,
    rng: random.Random | None = None,
) -> list[list[int]]:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and columns must be positive")
    if not 0 <= open_probability <= 1:
        raise ValueError("open_probability must be between 0 and 1")

    generator = rng or random.Random()
    return [
        [1 if generator.random() < open_probability else 0 for _ in range(cols)]
        for _ in range(rows)
    ]


def parse_custom_maze(text: str, rows: int, cols: int) -> list[list[int]]:
    maze = [list(map(int, row.split())) for row in text.split(";") if row.strip()]
    actual_rows, actual_cols = maze_shape(maze)
    if (actual_rows, actual_cols) != (rows, cols):
        raise ValueError(
            f"expected a {rows}x{cols} maze, got {actual_rows}x{actual_cols}"
        )
    return maze


def _read_point(label: str) -> Point:
    row = int(input(f"Enter the {label} row: "))
    col = int(input(f"Enter the {label} column: "))
    return row, col


def main() -> None:
    print("Rat in a Maze — DFS, BFS, A*, and backtracking")

    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    option = input("Choose maze (1 = custom, 2 = random): ").strip()

    if option == "1":
        raw = input("Enter rows separated by ';' and cells by spaces: ")
        maze = parse_custom_maze(raw, rows, cols)
    elif option == "2":
        maze = generate_random_maze(rows, cols)
        print("\nRandomly generated maze:")
        print("\n".join(" ".join(map(str, row)) for row in maze))
    else:
        raise ValueError("maze option must be 1 or 2")

    start = _read_point("start")
    end = _read_point("end")
    _validate_endpoints(maze, start, end)

    method = input(
        "Choose method (1 = backtracking, 2 = A*, 3 = DFS, 4 = BFS): "
    ).strip()

    if method == "1":
        paths = all_simple_paths(maze, start, end)
        if not paths:
            path = None
        else:
            path = min(paths, key=len)
            print(f"Simple paths found: {len(paths)}")
            print("Shortest among enumerated simple paths:", path)
    elif method == "2":
        path = a_star(maze, start, end)
        if path is not None:
            print("Shortest path found by A*:", path)
    elif method == "3":
        path = dfs(maze, start, end)
        if path is not None:
            print("Path found by DFS (not guaranteed shortest):", path)
    elif method == "4":
        path = bfs(maze, start, end)
        if path is not None:
            print("Shortest path found by BFS:", path)
    else:
        raise ValueError("method must be 1, 2, 3, or 4")

    if path is None:
        print("No path found.")
        return

    print("Path length:", len(path))
    print("\nMaze with path [S=start, E=end, *=path]:")
    print(render_maze_with_path(maze, path, start, end))


if __name__ == "__main__":
    main()
