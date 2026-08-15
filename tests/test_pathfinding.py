import random
import unittest

from rat_in_maze import (
    a_star,
    all_simple_paths,
    apply_path,
    bfs,
    dfs,
    generate_random_maze,
    parse_custom_maze,
)


class PathfindingTests(unittest.TestCase):
    def setUp(self):
        self.maze = [
            [1, 1, 0, 1],
            [0, 1, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 1],
        ]
        self.start = (0, 0)
        self.end = (3, 3)

    def assert_valid_path(self, maze, start, end, path):
        self.assertIsNotNone(path)
        positions = apply_path(start, path)
        self.assertEqual(positions[-1], end)
        rows, cols = len(maze), len(maze[0])
        for row, col in positions:
            self.assertTrue(0 <= row < rows and 0 <= col < cols)
            self.assertEqual(maze[row][col], 1)

    def test_bfs_returns_shortest_path(self):
        path = bfs(self.maze, self.start, self.end)
        self.assert_valid_path(self.maze, self.start, self.end, path)
        self.assertEqual(len(path), 6)

    def test_a_star_matches_bfs_shortest_length(self):
        bfs_path = bfs(self.maze, self.start, self.end)
        astar_path = a_star(self.maze, self.start, self.end)
        self.assert_valid_path(self.maze, self.start, self.end, astar_path)
        self.assertEqual(len(astar_path), len(bfs_path))

    def test_a_star_matches_bfs_on_multiple_fixed_mazes(self):
        mazes = [
            [[1, 1, 1], [0, 0, 1], [1, 1, 1]],
            [[1, 0, 1], [1, 1, 1], [1, 0, 1]],
            [[1, 1, 1, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
        ]
        for maze in mazes:
            start = (0, 0)
            end = (len(maze) - 1, len(maze[0]) - 1)
            self.assertEqual(len(a_star(maze, start, end)), len(bfs(maze, start, end)))

    def test_dfs_returns_a_valid_path_when_one_exists(self):
        path = dfs(self.maze, self.start, self.end)
        self.assert_valid_path(self.maze, self.start, self.end, path)

    def test_unreachable_returns_none(self):
        maze = [[1, 0], [0, 1]]
        self.assertIsNone(bfs(maze, (0, 0), (1, 1)))
        self.assertIsNone(a_star(maze, (0, 0), (1, 1)))
        self.assertIsNone(dfs(maze, (0, 0), (1, 1)))

    def test_start_equal_end_returns_empty_path(self):
        maze = [[1]]
        self.assertEqual(bfs(maze, (0, 0), (0, 0)), "")
        self.assertEqual(a_star(maze, (0, 0), (0, 0)), "")
        self.assertEqual(dfs(maze, (0, 0), (0, 0)), "")
        self.assertEqual(all_simple_paths(maze, (0, 0), (0, 0)), [""])

    def test_backtracking_enumerates_simple_paths(self):
        maze = [[1, 1], [1, 1]]
        paths = set(all_simple_paths(maze, (0, 0), (1, 1)))
        self.assertEqual(paths, {"DR", "RD"})

    def test_custom_maze_dimension_validation(self):
        self.assertEqual(parse_custom_maze("1 1;0 1", 2, 2), [[1, 1], [0, 1]])
        with self.assertRaises(ValueError):
            parse_custom_maze("1 1;0 1", 3, 2)

    def test_random_maze_is_reproducible_with_rng(self):
        first = generate_random_maze(3, 4, rng=random.Random(123))
        second = generate_random_maze(3, 4, rng=random.Random(123))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
