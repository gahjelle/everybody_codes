"""Everybody Codes quest 15, 2025: Definitely Not a Maze."""

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

    Assumes that each "corridor" is at least two spaces wide. Use row and col to
    designate original coordinates and r and c as notation for coordinates in
    the compressed space.
    """
    # Find corners in order to find the compressed coordinates
    rows, cols, (row, col), direction = {0}, {0}, (0, 0), (-1, 0)
    for command in puzzle_input.split(","):
        turn, *steps = command
        drow, dcol = direction = TURNS[turn][direction]
        num_steps = int("".join(steps))
        row += drow * num_steps
        col += dcol * num_steps
        rows.add(row)
        cols.add(col)

    # Map original coordinates to a compressed space
    row2r = {
        row + offset: 3 * idx + offset
        for offset in [0, -1, 1]
        for idx, row in enumerate(sorted(rows))
    }
    col2c = {
        col + offset: 3 * idx + offset
        for offset in [0, -1, 1]
        for idx, col in enumerate(sorted(cols))
    }

    # Create walls in the compressed space
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

    return (
        walls,
        start,
        (r, c),
        {r: row for row, r in row2r.items()},
        {c: col for col, c in col2c.items()},
    )


def part(puzzle_input: str) -> int:
    """Solve each part."""
    walls, start, end, r2row, c2col = parse(puzzle_input)
    return find_shortest_path(walls - {start, end}, start, end, r2row, c2col)


part1 = part
part2 = part
part3 = part


def find_shortest_path(
    walls: Grid,
    start: Coordinate,
    end: Coordinate,
    r2row: dict[int, int],
    c2col: dict[int, int],
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

        r, c = pos
        row, col = r2row[r], c2col[c]
        for npos in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]:
            if npos not in walls and npos not in seen:
                nr, nc = npos
                if nr not in r2row or nc not in c2col:  # Don't search outside the grid
                    continue
                nrow, ncol = r2row[nr], c2col[nc]
                heapq.heappush(
                    queue, (num_steps + abs(nrow - row) + abs(ncol - col), npos)
                )
    return 0
