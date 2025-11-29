"""Everybody Codes quest 20, 2025: Dream in Triangles."""

import collections
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, str]


def parse_maze(puzzle_input: str) -> Grid:
    """Parse the triangular maze."""
    return {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
        if char != "."
    }


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    maze = parse_maze(puzzle_input)
    triangles = {pos for pos, char in maze.items() if char == "T"}

    pairs = set()
    for triangle in triangles:
        for nbh in neighbours(triangle):
            if nbh in triangles:
                pairs.add(tuple(sorted([triangle, nbh])))
    return len(pairs)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    maze = parse_maze(puzzle_input)
    triangles = {pos for pos, char in maze.items() if char in "TSE"}
    start = next(pos for pos, char in maze.items() if char == "S")
    end = next(pos for pos, char in maze.items() if char == "E")
    return find_path([triangles], start, end)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    maze = parse_maze(puzzle_input)
    triangles = {pos for pos, char in maze.items() if char in "TSE"}
    start = next(pos for pos, char in maze.items() if char == "S")
    end = next(pos for pos, char in maze.items() if char == "E")
    max_col = max(c for _, c in maze)
    grids = [
        triangles,
        rotate(triangles, max_col),
        rotate(rotate(triangles, max_col), max_col),
    ]
    return find_path(grids, start, end)


def neighbours(pos: Coordinate) -> list[Coordinate]:
    """Find neighbours of a given triangle."""
    row, col = pos
    updown = 1 if (row + col) % 2 else -1
    return [(row, col - 1), (row, col + 1), (row + updown, col)]


def rotate(grid: set[Coordinate], max_col: int) -> set[Coordinate]:
    """Rotate the grid 120 degrees.

    12345    97621    54879    12345
    .678.    .843.    .326.    .678.
    ..9..    ..5..    ..1..    ..9..

    0, 0  ->  0,  0  ->  0, 4
    0, 1      0, -1      0, 3
    0, 2      1, -1      1, 3
    0, 3      1, -2      1, 2
    0, 4      2, -2      2, 2
    1, 1      0, -2      0, 2
    1, 2      0, -3      0, 1
    1, 3      1, -3      1, 1
    2, 2      0, -4      0, 0
    """
    return {
        ((col - row) // 2, max_col + (col - row) // 2 - (row + col))
        for row, col in grid
    }


def find_path(grids: list[set[Coordinate]], start: Coordinate, end: Coordinate) -> int:
    """Find the shortest path through the grid."""
    queue = collections.deque([(start, 0, 0)])
    seen = set()
    while queue:
        (row, col), num_steps, grid = queue.popleft()
        if (row, col) == end:
            return num_steps
        if (row, col, grid) in seen:
            continue
        seen.add((row, col, grid))

        ngrid = (grid + 1) % len(grids)
        for npos in [*neighbours((row, col)), (row, col)]:
            if npos not in grids[ngrid] or (*npos, ngrid) in seen:
                continue
            queue.append((npos, num_steps + 1, ngrid))
    return 0
