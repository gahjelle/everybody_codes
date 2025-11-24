"""Everybody Codes quest 12, 2025: One Spark to Burn Them All."""

import collections
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, int]


def parse(puzzle_input: str) -> Grid:
    """Parse grid."""
    return {
        (row, col): int(value)
        for row, line in enumerate(puzzle_input.splitlines())
        for col, value in enumerate(line)
    }


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    grid = parse(puzzle_input)
    return len(destroy(grid, start=[(0, 0)]))


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    grid = parse(puzzle_input)
    return len(destroy(grid, start=[min(grid), max(grid)]))


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    grid = parse(puzzle_input)
    first, barrels = optimal(grid)
    grid2 = {barrel: size for barrel, size in grid.items() if barrel not in barrels}
    second, barrels = optimal(grid2)
    grid3 = {barrel: size for barrel, size in grid2.items() if barrel not in barrels}
    third, _ = optimal(grid3)

    return len(destroy(grid, start=[first, second, third]))


def destroy(grid: Grid, start: list[Coordinate]) -> set[Coordinate]:
    """Destroy barrels, starting at start."""
    seen = set()
    queue = collections.deque(start)
    while queue:
        barrel = queue.popleft()
        if barrel in seen:
            continue
        seen.add(barrel)

        size = grid[barrel]
        r, c = barrel
        for nrow, ncol in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
            nsize = grid.get((nrow, ncol), 10)  # Regular barrels are at most 9
            if nsize <= size:
                queue.append((nrow, ncol))
    return seen


def optimal(grid: Grid) -> tuple[Coordinate, set[Coordinate]]:
    """Find the optimal start point."""
    local_maxima = [
        (r, c)
        for (r, c), size in grid.items()
        if all(
            npos not in grid or grid[npos] <= size
            for npos in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
        )
    ]
    destruction = {start: destroy(grid, [start]) for start in local_maxima}
    return max(destruction.items(), key=lambda pair: len(pair[1]))
