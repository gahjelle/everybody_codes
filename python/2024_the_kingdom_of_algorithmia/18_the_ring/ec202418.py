"""Everybody Codes 18, 2024: The Ring."""

# Standard library imports
import collections
import sys
from pathlib import Path


def parse(puzzle_input):
    """Parse input data."""
    left_col, right_col = 0, puzzle_input.index("\n") - 1
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char != "#"
    }
    palm_trees = {pos for pos, char in grid.items() if char == "P"}
    starts = [(row, col) for row, col in grid.keys() if col in [left_col, right_col]]
    return grid, palm_trees, starts


def part1(puzzle_input):
    """Solve part 1."""
    grid, palm_trees, starts = parse(puzzle_input)
    num_steps = flood_fill(grid, starts)
    return max(steps for pos, steps in num_steps.items() if pos in palm_trees)


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3.

    Flood fill from each palm tree, find location with least number of total
    steps.
    """
    grid, palm_trees, _ = parse(puzzle_input)
    num_steps = sum(
        (flood_fill(grid, [start]) for start in palm_trees), collections.Counter()
    )
    return min(steps for pos, steps in num_steps.items() if pos not in palm_trees)


def flood_fill(grid, starts):
    """Flood fill the grid."""
    seen = collections.Counter()
    queue = collections.deque([(start, 0) for start in starts])
    while queue:
        (row, col), steps = queue.popleft()
        if (row, col) in seen:
            continue

        seen[(row, col)] = steps
        for new_pos in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
            if new_pos in grid and new_pos not in seen:
                queue.append((new_pos, steps + 1))
    return seen


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
