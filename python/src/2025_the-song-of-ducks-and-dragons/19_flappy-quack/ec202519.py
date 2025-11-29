"""Everybody Codes quest 19, 2025: Flappy Quack."""

import collections
import heapq
from typing import TypeAlias

Walls: TypeAlias = dict[int, set[int]]


def parse_walls(puzzle_input: str) -> Walls:
    walls = collections.defaultdict(set)
    for wall in puzzle_input.splitlines():
        x, ys = parse_wall(wall)
        walls[x] |= ys
    return walls


def parse_wall(line: str) -> tuple[int, set[int]]:
    """Parse one wall."""
    x, y, height = [int(num) for num in line.split(",")]
    return x, {h for h in range(y, y + height) if (x + h) % 2 == 0}


def part(puzzle_input: str) -> int:
    """Solve each part

    Note the number of flaps to get to a position is not dependent on the path
    to get there. As long as the "maze" is solvable, we can "teleport" to the
    second to last wall and calculate flaps from there.
    """
    walls = parse_walls(puzzle_input)
    last_two_walls = dict(sorted(walls.items())[-2:])
    return find_flaps(last_two_walls, target=max(walls))


part1 = part
part2 = part
part3 = part


def find_flaps(walls: Walls, target: int) -> int:
    """Find the minimum number of flaps necessary to pass all walls."""
    queue = [(0, 0, 0)]
    seen = set()
    while queue:
        x, flaps, y = heapq.heappop(queue)
        if x in walls and y not in walls[x]:
            continue
        if x == target:
            return flaps
        if (x, y) in seen:
            continue
        seen.add((x, y))

        next_x = min(wx for wx in walls if wx > x)
        next_ys = walls[next_x]
        dx = next_x - x
        for ny in next_ys:
            if abs(ny - y) > dx:
                continue
            nflaps = flaps + dx - (dx - (ny - y)) // 2
            heapq.heappush(queue, (next_x, nflaps, ny))

    return 0
