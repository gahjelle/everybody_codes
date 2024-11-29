"""Everybody Codes 19, 2024: Encrypted Duck."""

# Standard library imports
import itertools
import sys
from pathlib import Path


def parse(puzzle_input):
    """Parse the input."""
    key, grid = puzzle_input.split("\n\n")
    return key, {
        (row, col): char
        for row, line in enumerate(grid.split("\n"))
        for col, char in enumerate(line)
    }


def part1(puzzle_input, rounds=1):
    """Solve part 1."""
    key, grid = parse(puzzle_input)
    decoded_grid = decode(grid, key, num_rounds=rounds)
    # display(decoded_grid)
    return find_message(decoded_grid)


def part2(puzzle_input, rounds=100):
    """Solve part 2."""
    return part1(puzzle_input, rounds)


def part3(puzzle_input, rounds=1_048_576_000):
    """Solve part 3."""
    return part1(puzzle_input, rounds)


def rotate(grid, key):
    """Rotate the grid once around all rotation points."""
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    max_row, max_col = max(grid)
    for (row, col), direction in zip(
        itertools.product(range(1, max_row), range(1, max_col)), itertools.cycle(key)
    ):
        cells = [(row + dr, col + dc) for dr, dc in deltas + deltas[:1]]
        grid = grid | (
            {start: grid[end] for start, end in zip(cells, cells[1:])}
            if direction == "L"
            else {start: grid[end] for start, end in zip(cells[1:], cells)}
        )
    return grid


def find_permutation_cycles(grid, key):
    """Find the permutation cycles corresponding to one rotation."""
    transitions = {
        value: key for key, value in rotate({pos: pos for pos in grid}, key).items()
    }

    cycles = []
    seen = set()
    for start_pos in grid:
        if start_pos in seen:
            continue
        cycle = []
        pos = start_pos
        while pos not in seen:
            cycle.append(pos)
            seen.add(pos)
            pos = transitions[pos]
        cycles.append(cycle)
    return cycles


def decode(grid, key, num_rounds):
    """Decode a message grid."""
    cycles = find_permutation_cycles(grid, key)
    return {
        cycle[(idx + num_rounds) % len(cycle)]: grid[pos]
        for cycle in cycles
        for idx, pos in enumerate(cycle)
    }


def find_message(grid):
    """Find the message hidden in the grid.

    Assumes the message is in one row.
    """
    row, start_col = next(pos for pos, char in grid.items() if char == ">")
    _, end_col = next(pos for pos, char in grid.items() if char == "<")

    return "".join(grid[row, col] for col in range(start_col + 1, end_col))


def display(grid):
    """Display the grid on the console."""
    max_row, max_col = max(grid)
    for row in range(max_row + 1):
        for col in range(max_col + 1):
            print(grid[row, col], end="")
        print()


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
