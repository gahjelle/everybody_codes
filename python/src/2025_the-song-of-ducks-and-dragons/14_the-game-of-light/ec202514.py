"""Everybody Codes quest 14, 2025: The Game of Light."""

import math
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, bool]


def parse_grid(puzzle_input: str) -> Grid:
    """Parse a grid."""
    return {
        (row, col): char == "#"
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }


def part1(puzzle_input: str, num_rounds=10) -> int:
    """Solve part 1."""
    grid = parse_grid(puzzle_input)
    count = 0
    for _ in range(num_rounds):
        grid = evolve(grid)
        count += sum(grid.values())
    return count


def part2(puzzle_input: str, num_rounds=2025) -> int:
    """Solve part 2."""
    return part1(puzzle_input, num_rounds=num_rounds)


def part3(puzzle_input: str, num_rounds=1_000_000_000, size=34) -> int:
    """Solve part 3."""
    grid = blank_grid(size)
    center = parse_grid(puzzle_input)

    # Move center coordinates to match full grid
    center_size = math.isqrt(len(center))
    offset = (size - center_size) // 2
    center = {
        (row + offset, col + offset): state for (row, col), state in center.items()
    }

    # Evolve the grid until a cycle is detected
    seen: dict[tuple[tuple[bool, ...], bool, int], int] = {}
    round, key = 0, ((), False, 0)
    for round in range(1, num_rounds + 1):
        grid = evolve(grid)
        grid_center = {pos: state for pos, state in grid.items() if pos in center}
        key = tuple(grid.values()), grid_center == center, sum(grid.values())
        if key in seen:
            break
        seen[key] = round

    # Jump to the end of the evolution
    cycle = round - seen[key]
    rounds_left = num_rounds - round
    jump = rounds_left // cycle
    counts = sum(active for _, match, active in seen if match) * (jump + 1)

    # Evolve the final rounds
    for _ in range(round + (cycle * jump), num_rounds + 1):
        grid = evolve(grid)
        grid_center = {pos: state for pos, state in grid.items() if pos in center}
        if grid_center == center:
            counts += sum(grid.values())

    return counts


def blank_grid(size: int) -> Grid:
    """Create a blank grid."""
    return {(row, col): False for row in range(size) for col in range(size)}


def neighbors(pos: Coordinate) -> list[Coordinate]:
    """Find diagonal neighbors of a position, including the position itself."""
    r, c = pos
    return [pos, (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]


def evolve(grid: Grid) -> Grid:
    """Evolve the grid one round."""
    return {
        pos: sum(grid.get(nb, False) for nb in neighbors(pos)) % 2 == 0 for pos in grid
    }
