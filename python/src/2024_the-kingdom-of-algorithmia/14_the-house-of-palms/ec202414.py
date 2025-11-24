"""Everybody Codes 14, 2024: The House of Palms"""

import collections
import itertools
from typing import TypeAlias

DIRECTION = {
    "U": (1, 0, 0),
    "D": (-1, 0, 0),
    "L": (0, -1, 0),
    "R": (0, 1, 0),
    "F": (0, 0, 1),
    "B": (0, 0, -1),
}

Coordinate: TypeAlias = tuple[int, int, int]
Direction: TypeAlias = tuple[int, int, int]
Plan: TypeAlias = list[tuple[Direction, int]]


def parse_plan(puzzle_input: str) -> Plan:
    """Parse one plan."""
    return [(DIRECTION[step[0]], int(step[1:])) for step in puzzle_input.split(",")]


def parse_plans(puzzle_input: str) -> list[Plan]:
    """Parse a list of plans."""
    return [parse_plan(plan) for plan in puzzle_input.split("\n")]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    plan = parse_plan(puzzle_input)
    return max(itertools.accumulate(row * step for (row, _, _), step in plan))


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    plans = parse_plans(puzzle_input)
    return len(set.union(*[grow_tree(plan)[0] for plan in plans]))


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    plans = parse_plans(puzzle_input)
    branches, leaves = zip(*[grow_tree(plan) for plan in plans])
    tree = set.union(*branches)

    all_steps = [  # sorted() inside loop is a bit slow, but okay
        [
            num_steps
            for (_, col, depth), num_steps in sorted(find_steps(tree, leaf).items())
            if col == depth == 0
        ]
        for leaf in leaves
    ]
    return min(sum(steps) for steps in zip(*all_steps))


def find_steps(tree: set[Coordinate], start: Coordinate) -> dict[Coordinate, int]:
    """Find the number of steps it takes to move from start to anywhere in the tree."""
    queue = collections.deque([(0, start)])
    steps = {}
    while queue:
        num_steps, pos = queue.popleft()
        if pos in steps:
            continue
        steps[pos] = num_steps

        row, col, depth = pos
        for drow, dcol, ddepth in DIRECTION.values():
            new_pos = (row + drow, col + dcol, depth + ddepth)
            if new_pos in tree and new_pos not in steps:
                queue.append((num_steps + 1, new_pos))
    return steps


def grow_tree(plan: Plan) -> tuple[set[Coordinate], Coordinate]:
    """Grow one tree based on the plan. Return tree and leaf, the end of the branch"""
    tree = set()

    row, col, depth = 0, 0, 0
    for (drow, dcol, ddepth), steps in plan:
        for _ in range(steps):
            row, col, depth = row + drow, col + dcol, depth + ddepth
            tree.add((row, col, depth))
    return tree, (row, col, depth)
