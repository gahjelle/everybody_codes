"""Everybody Codes 13, 2024: Never Gonna Let You Down"""

import heapq
from collections.abc import Iterable
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Maze: TypeAlias = dict[Coordinate, int]


def parse(puzzle_input: str) -> tuple[set[Coordinate], Coordinate, Maze]:
    """Parse the puzzle input."""
    maze = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char != "#"
    }
    return (
        {pos for pos, char in maze.items() if char == "S"},
        next(pos for pos, char in maze.items() if char == "E"),
        {pos: int(char) for pos, char in maze.items() if char.isdigit()},
    )


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    (start,), target, maze = parse(puzzle_input)
    return explore_maze(maze, start, [target])


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input: str) -> int:
    """Solve part 3.

    Start at E and walk backwards until you reach the closest S.
    """
    targets, start, maze = parse(puzzle_input)
    return explore_maze(maze, start, targets)


def explore_maze(maze: Maze, start: Coordinate, targets: Iterable[Coordinate]) -> int:
    """Walk the maze until you reach the closest target."""
    infty = 999_999
    maze |= {pos: 0 for pos in targets}

    queue = [(0, 0, start)]
    best_seen = {start: 0}
    while queue:
        steps, level, pos = heapq.heappop(queue)
        if pos in targets:
            return steps

        row, col = pos
        for drow, dcol in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if (new_pos := (row + drow, col + dcol)) in maze:
                diff = min(abs(level - maze[new_pos]), 10 - abs(level - maze[new_pos]))
                if (new_steps := steps + 1 + diff) < best_seen.get(new_pos, infty):
                    best_seen[new_pos] = new_steps
                    heapq.heappush(queue, (new_steps, maze[new_pos], new_pos))
    return infty
