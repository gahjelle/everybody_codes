"""Everybody Codes 15, 2024: From the Herbalist's Diary"""

import heapq
from string import ascii_letters as letters
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, str]
Herbs: TypeAlias = tuple[str, ...]  # Use tuple instead of list for hashability


def parse(puzzle_input: str) -> Grid:
    """Parse input."""
    return {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char not in "#~"
    }


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    grid = parse(puzzle_input)
    start = min(grid)
    return explore(grid, start)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    grid = parse(puzzle_input)
    num_steps = 0

    # Left column
    start_left = min(pos for pos, herb in grid.items() if herb == "K")
    grid_left = {
        (row, col): herb for (row, col), herb in grid.items() if col < start_left[1]
    } | {start_left: "."}
    num_steps += explore(grid_left, start_left)

    # Right column
    start_right = max(pos for pos, herb in grid.items() if herb == "K")
    grid_right = {
        (row, col): herb for (row, col), herb in grid.items() if col > start_right[1]
    } | {start_right: "."}
    num_steps += explore(grid_right, start_right)

    # Center column
    start_center = min(grid)
    grid_center = {
        (row, col): herb
        for (row, col), herb in grid.items()
        if start_left[1] <= col <= start_right[1]
    } | {start_left: "X", start_right: "Y"}  # Replace K by X and Y
    num_steps += explore(grid_center, start_center)

    return num_steps


def explore(grid: Grid, start: Coordinate) -> int:
    """Explore the grid while collecting herbs"""
    infty = 9_999
    targets = {target for target in set(grid.values()) if target in letters}
    queue: list[tuple[int, Coordinate, Herbs]] = [(0, start, ())]
    seen: dict[tuple[Coordinate, Herbs], int] = {}
    while queue:
        num_steps, pos, herbs = heapq.heappop(queue)
        if (pos, herbs) in seen:
            continue
        if pos == start and set(herbs) == targets:
            return num_steps

        seen[pos, herbs] = num_steps
        for drow, dcol in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_pos = (pos[0] + drow, pos[1] + dcol)
            if new_pos in grid:
                new_herbs = (
                    tuple(sorted(herbs + (grid[pos],)))
                    if grid[pos] in targets and grid[pos] not in herbs
                    else herbs
                )
                if num_steps + 1 < seen.get((new_pos, new_herbs), infty):
                    heapq.heappush(queue, (num_steps + 1, new_pos, new_herbs))
    return infty
