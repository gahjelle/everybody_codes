"""Everybody Codes quest 17, 2025: Deadline-Driven Development."""

import heapq
import itertools
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
StrGrid: TypeAlias = dict[Coordinate, str]
Grid: TypeAlias = dict[Coordinate, int]

INFINITY = 999_999


def parse_grid(puzzle_input: str) -> StrGrid:
    """Parse the input grid. Adjust coordinates to be centered around vulcano."""
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }
    vrow, vcol = next(pos for pos, char in grid.items() if char == "@")
    return {(row - vrow, col - vcol): char for (row, col), char in grid.items()}


def parse_vulcano(puzzle_input: str) -> Grid:
    """Parse a vulcano grid."""
    return {
        pos: int(char)
        for pos, char in parse_grid(puzzle_input).items()
        if char not in "@"
    }


def parse_foothills(puzzle_input: str) -> tuple[Coordinate, Grid]:
    """Parse a vulcano grid, include start coordinates."""
    grid = parse_grid(puzzle_input)
    start = next(pos for pos, char in grid.items() if char == "S")
    return start, {pos: 0 if char in "S@" else int(char) for pos, char in grid.items()}


def part1(puzzle_input: str, radius: int = 10) -> int:
    """Solve part 1."""
    grid = parse_vulcano(puzzle_input)
    return sum(lava(grid, max_radius=radius).values())


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    grid = parse_vulcano(puzzle_input)
    max_radius = max(max(grid))
    damages = [
        (sum(lava(grid, min_radius=r, max_radius=r + 1).values()), r + 1)
        for r in range(max_radius)
    ]
    max_damage, radius = max(damages)
    return max_damage * radius


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    (srow, scol), grid = parse_foothills(puzzle_input)
    for radius in itertools.count(start=abs(srow) // 3):
        if steps := find_loop(
            foothills(grid, radius=radius), (srow, scol), max_steps=30 * radius + 29
        ):
            return steps * radius
    return 0


def lava(vulcano: Grid, min_radius: int = 0, max_radius: int = INFINITY) -> Grid:
    """Find the erupted area of a vulcano with the given radius."""
    return {
        (row, col): value
        for (row, col), value in vulcano.items()
        if min_radius**2 < row**2 + col**2 <= max_radius**2
    }


def foothills(vulcano: Grid, radius: int) -> Grid:
    """Find the non-damaged area around the vulcano."""
    return {
        (row, col): value
        for (row, col), value in vulcano.items()
        if row**2 + col**2 > radius**2
    }


def find_loop(grid: Grid, start: Coordinate, max_steps: int) -> int:
    """Find the length of the shortest loop around the vulcano.

    Use loop to count the number of loops the path makes. In practice, loop
    counts how many times the path crosses the ray going directly south from the
    vulcano.
    """
    ray = {(-1, 0): 1, (0, -1): -1}
    queue = [(0, start, 0)]
    seen = set()
    while queue:
        num_steps, (row, col), loop = heapq.heappop(queue)
        if num_steps > max_steps:
            break
        if (row, col) == start and loop != 0:
            return num_steps
        if (row, col, loop) in seen or abs(loop) >= 2:
            continue
        seen.add((row, col, loop))

        for nr, nc in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
            if (npos := (nr, nc)) not in grid:
                continue
            nloop = loop + (nr > 0) * ray.get((col, nc), 0)
            if (nr, nc, nloop) not in seen:
                heapq.heappush(queue, (num_steps + grid[npos], npos, nloop))
    return 0
