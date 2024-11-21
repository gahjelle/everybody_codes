"""Everybody Codes 13, 2024: Never Gonna Let You Down"""

# Standard library imports
import heapq
import sys
from pathlib import Path


def parse(puzzle_input):
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


def part1(puzzle_input):
    """Solve part 1."""
    (start,), target, maze = parse(puzzle_input)
    return explore_maze(maze, start, [target])


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3.

    Start at E and walk backwards until you reach the closest S.
    """
    targets, start, maze = parse(puzzle_input)
    return explore_maze(maze, start, targets)


def explore_maze(maze, start, targets):
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


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
