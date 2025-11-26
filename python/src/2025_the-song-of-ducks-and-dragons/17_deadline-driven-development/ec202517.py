"""Everybody Codes quest 17, 2025: Deadline-Driven Development."""

import heapq
import itertools
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, int]


def parse_vulcano(puzzle_input: str) -> tuple[Grid, Coordinate | None]:
    """Parse a vulcano grid."""
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }
    vrow, vcol = next(pos for pos, char in grid.items() if char == "@")
    srow, scol = next((pos for pos, char in grid.items() if char == "S"), (None, None))
    return {
        (row - vrow, col - vcol): int(char)
        for (row, col), char in grid.items()
        if char not in "@S"
    }, None if (srow is None or scol is None) else (srow - vrow, scol - vcol)


def part1(puzzle_input: str, radius: int = 10) -> int:
    """Solve part 1."""
    grid, _ = parse_vulcano(puzzle_input)
    return sum(
        lava for (row, col), lava in grid.items() if row**2 + col**2 <= radius**2
    )


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    grid, _ = parse_vulcano(puzzle_input)
    max_radius = max(max(grid))

    prev = 0
    damages = []
    for radius in range(1, max_radius + 1):
        damage = sum(
            lava for (row, col), lava in grid.items() if row**2 + col**2 <= radius**2
        )
        damages.append((damage - prev, radius))
        prev = damage

    max_damage, radius = max(damages)
    return max_damage * radius


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    grid, start = parse_vulcano(puzzle_input)
    if start is None:
        return 0

    max_radius = max(max(grid))
    for radius in range(max_radius * 2):
        if steps := find_loop(
            {
                (row, col): char
                for (row, col), char in grid.items()
                if row**2 + col**2 > radius**2
            },
            start,
            max_steps=30 * radius + 29,
        ):
            return steps * radius
    return 0


def find_loop(grid: Grid, start: Coordinate, max_steps: int) -> int:
    """Find the time it takes to create a loop.

    Return 0 if the loop can not be made within the given number of steps.

    Create paths from the start to the middle column (col 0) below the vulcano.
    Use left and right variables to track whether the path runs to the left or
    to the right of the vulcano. Find the best combination of a left and right
    path.
    """
    best_loop = max_steps + 1
    queue = [(0, start, False, False)]
    steps = {}
    while queue:
        num_steps, (row, col), left, right = heapq.heappop(queue)
        if num_steps > max_steps:
            break

        # Do book-keeping for middle column below vulcano
        if col == 0 and row > 0:
            total_steps = (
                steps.get((row, -1), max_steps)  # Left path
                + steps.get((row, 1), max_steps)  # Right path
                + grid[row, 0]  # Connection point
            )
            best_loop = min(best_loop, total_steps)

        # Have we exhausted this path?
        if (row, col) in steps or (left and right):
            continue
        steps[row, col] = num_steps

        # Add the next steps to the queue
        for nr, nc in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
            npos = nr, nc
            if npos in grid:
                heapq.heappush(
                    queue,
                    (
                        num_steps + grid[npos],
                        npos,
                        left or (nr > 0 and nc < 0),
                        right or (nr > 0 and nc > 0),
                    ),
                )

    return best_loop if best_loop <= max_steps else 0
