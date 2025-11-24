"""Everybody Codes quest 15, 2025: Definitely Not a Maze."""

import collections
import heapq
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = set[Coordinate]

TURNS = {
    "R": {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)},
    "L": {(0, 1): (-1, 0), (1, 0): (0, 1), (0, -1): (1, 0), (-1, 0): (0, -1)},
}


def parse(
    puzzle_input: str,
) -> tuple[Grid, Coordinate, Coordinate, dict[int, int], dict[int, int]]:
    """Parse walls.

    Find possible coordinates and map them to consecutive numbers to help keep
    the search efficient.
    """
    rows, cols, (row, col), direction = {0}, {0}, (0, 0), (-1, 0)
    for command in puzzle_input.split(","):
        turn, *steps = command
        drow, dcol = direction = TURNS[turn][direction]
        num_steps = int("".join(steps))
        row += drow * num_steps
        col += dcol * num_steps
        rows.add(row)
        cols.add(col)

    row2r = {
        r: i
        for idx, row in enumerate(sorted(rows))
        for r, i in [(row - 1, 3 * idx - 1), (row, 3 * idx), (row + 1, 3 * idx + 1)]
    }
    col2c = {
        c: i
        for idx, col in enumerate(sorted(cols))
        for c, i in [(col - 1, 3 * idx - 1), (col, 3 * idx), (col + 1, 3 * idx + 1)]
    }

    start = (row2r[0], col2c[0])
    walls, (row, col), (r, c), direction = {start}, (0, 0), start, (-1, 0)
    for command in puzzle_input.split(","):
        turn, *steps = command
        drow, dcol = direction = TURNS[turn][direction]
        num_steps = int("".join(steps))
        num_s = max(
            abs(row2r[row + drow * num_steps] - r),
            abs(col2c[col + dcol * num_steps] - c),
        )
        for _ in range(num_s):
            r += drow
            c += dcol
            walls.add((r, c))
        row, col = row + drow * num_steps, col + dcol * num_steps
    return walls, start, (r, c), row2r, col2c


def part(puzzle_input: str) -> int:
    """Solve each part."""
    walls, start, end, rcoords, ccoords = parse(puzzle_input)
    return find_shortest_path(
        walls - {start, end},
        start,
        end,
        {r: row for row, r in rcoords.items()},
        {c: col for col, c in ccoords.items()},
    )


part1 = part
part2 = part
part3 = part


def find_shortest_path(
    walls: Grid,
    start: Coordinate,
    end: Coordinate,
    rcoords: dict[int, int],
    ccoords: dict[int, int],
) -> int:
    """Find the shortest path, taking step lengths into account."""
    queue = [(0, start)]
    seen = set()
    while queue:
        num_steps, pos = heapq.heappop(queue)
        if pos == end:
            return num_steps
        if pos in seen:
            continue
        seen.add(pos)

        row, col = pos
        r, c = rcoords[row], ccoords[col]
        for npos in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
            if npos not in walls and npos not in seen:
                nrow, ncol = npos
                nr, nc = rcoords[nrow], ccoords[ncol]
                heapq.heappush(queue, (num_steps + abs(nr - r) + abs(nc - c), npos))
    return 0
