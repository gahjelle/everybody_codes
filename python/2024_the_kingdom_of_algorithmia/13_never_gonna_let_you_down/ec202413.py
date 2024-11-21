"""Everybody Codes 13, 2024: Never Gonna Let You Down"""

# Standard library imports
import heapq
import sys
from pathlib import Path


def part1(puzzle_input):
    """Solve part 1."""
    starts, target, maze = parse(puzzle_input)
    return explore_maze(maze, starts[0], [target])


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3.

    Start at E and walk backwards until you reach the closest S.
    """
    starts, target, maze = parse(puzzle_input)
    return explore_maze(maze | {pos: 0 for pos in starts}, target, starts)


def parse(puzzle_input):
    """Parse the puzzle input."""
    maze = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char != "#"
    }
    starts = [pos for pos, char in maze.items() if char == "S"]
    target = next(pos for pos, char in maze.items() if char == "E")
    return (
        starts,
        target,
        {pos: int(char) for pos, char in maze.items() if char.isdigit()} | {target: 0},
    )


def explore_maze(maze, start, targets):
    """Walk the maze until you reach the closest target."""
    queue = [(0, 0, start)]
    seen = {start}
    while queue:
        num_steps, level, pos = heapq.heappop(queue)
        seen.add(pos)
        if pos in targets:
            return num_steps

        row, col = pos
        for drow, dcol in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_pos = (row + drow, col + dcol)
            if new_pos in maze and new_pos not in seen:
                diff = min(abs(level - maze[new_pos]), 10 - abs(level - maze[new_pos]))
                heapq.heappush(queue, (num_steps + 1 + diff, maze[new_pos], new_pos))
    return 999_999


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
