"""Everybody Codes quest 20, 2025: Dream in Triangles."""

import collections
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, str]
Triangles: TypeAlias = set[Coordinate]


def parse_maze(puzzle_input: str) -> tuple[Triangles, Coordinate, Coordinate, int]:
    """Parse the triangular maze."""
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
        if char != "."
    }
    triangles = {pos for pos, char in grid.items() if char in "TSE"}
    start = next((pos for pos, char in grid.items() if char == "S"), (0, 0))
    end = next((pos for pos, char in grid.items() if char == "E"), (0, 0))
    size = max(c for _, c in grid)
    return triangles, start, end, size


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    triangles, _, _, _ = parse_maze(puzzle_input)
    pairs = {
        (triangle, nbh)
        for triangle in triangles
        for nbh in neighbours(triangle)
        if nbh in triangles
    }
    return len(pairs) // 2  # Pairs are double counted


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    triangles, start, end, _ = parse_maze(puzzle_input)
    return find_path([triangles], start, end)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    triangles, start, end, size = parse_maze(puzzle_input)
    grids = [triangles, rotate(triangles, size), rotate(rotate(triangles, size), size)]
    return find_path(grids, start, end)


def neighbours(pos: Coordinate) -> list[Coordinate]:
    """Find neighbours of a given triangle."""
    row, col = pos
    updown = 1 if (row + col) % 2 else -1
    return [(row, col - 1), (row, col + 1), (row + updown, col)]


def rotate(grid: set[Coordinate], size: int) -> set[Coordinate]:
    """Rotate the grid 120 degrees.

    12345    97621    54879    12345
    .678.    .843.    .326.    .678.
    ..9..    ..5..    ..1..    ..9..

    0, 0                       0,  0                          0, 4
    0, 1                       0, -1                          0, 3
    0, 2  Rotate around (0,0)  1, -1    Translate by size     1, 3
    0, 3                       1, -2                          1, 2
    0, 4                       2, -2                          2, 2
    1, 1         ->            0, -2            ->            0, 2
    1, 2                       0, -3                          0, 1
    1, 3                       1, -3                          1, 1
    2, 2                       0, -4                          0, 0
    """
    return {(nrow := (col - row) // 2, size + nrow - (row + col)) for row, col in grid}


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
