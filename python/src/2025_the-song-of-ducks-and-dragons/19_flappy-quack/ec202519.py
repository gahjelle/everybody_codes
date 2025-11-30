"""Everybody Codes quest 19, 2025: Flappy Quack."""

import collections
import heapq
import itertools
from typing import TypeAlias

Walls: TypeAlias = dict[int, set[int]]
Cache: TypeAlias = dict[int, set[int]]


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
    last_wall = max(walls)
    min_height = min(find_heights(walls))
    return find_flaps(last_wall, min_height)


part1 = part
part2 = part
part3 = part


def find_flaps(x: int, height: int) -> int:
    """Find the number of flaps necessary to come to the given position."""
    return (x + height) // 2


def find_heights(walls: Walls) -> set[int]:
    """Find the possible heights at the final wall."""
    heights = {0}
    for x, next_x in itertools.pairwise([0, *walls]):
        dx = next_x - x
        heights = {
            height
            for height in walls[next_x]
            if any(height - dx <= h <= height + dx for h in heights)
        }
        # print(next_x, heights)
    return heights
