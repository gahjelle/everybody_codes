"""Everybody Codes 18, 2024: The Ring."""

import collections
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]


def parse(
    puzzle_input: str,
) -> tuple[dict[Coordinate, str], set[Coordinate], list[Coordinate]]:
    """Parse input data."""
    left_col, right_col = 0, puzzle_input.index("\n") - 1
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char != "#"
    }
    palm_trees = {pos for pos, char in grid.items() if char == "P"}
    starts = [(row, col) for row, col in grid.keys() if col in [left_col, right_col]]
    return grid, palm_trees, starts


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    grid, palm_trees, starts = parse(puzzle_input)
    num_steps = flood_fill(grid, starts)
    return max(steps for pos, steps in num_steps.items() if pos in palm_trees)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input: str) -> int:
    """Solve part 3.

    Flood fill from each palm tree, find location with least number of total
    steps.
    """
    grid, palm_trees, _ = parse(puzzle_input)
    num_steps = collections.defaultdict(int)
    for start in palm_trees:
        for pos, steps in flood_fill(grid, [start]).items():
            num_steps[pos] += steps
    return min(steps for pos, steps in num_steps.items() if pos not in palm_trees)


def flood_fill(
    grid: dict[Coordinate, str], starts: list[Coordinate]
) -> dict[Coordinate, int]:
    """Flood fill the grid."""
    seen: dict[Coordinate, int] = {}
    queue = collections.deque([(start, 0) for start in starts])
    while queue:
        (row, col), steps = queue.popleft()
        if (row, col) in seen:
            continue

        seen[(row, col)] = steps
        for new_pos in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
            if new_pos in grid and new_pos not in seen:
                queue.append((new_pos, steps + 1))
    return seen
