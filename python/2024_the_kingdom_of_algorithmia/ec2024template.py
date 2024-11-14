"""Everybody Codes #, 2024: <NAME>"""

# Standard library imports
import sys
from pathlib import Path


def parse_data_part1(puzzle_input):
    """Parse input for part 1."""
    return puzzle_input


def part1(insects):
    """Solve part 1."""


def parse_data_part2(puzzle_input):
    """Parse input for part 2."""
    return puzzle_input


def part2(insects):
    """Solve part 2."""


def parse_data_part3(puzzle_input):
    """Parse input for part 3."""
    return puzzle_input


def part3(insects):
    """Solve part 3."""


def solve(puzzle_input1, puzzle_input2, puzzle_input3):
    """Solve the puzzle for the given input."""
    yield part1(parse_data_part1(puzzle_input1))
    yield part2(parse_data_part2(puzzle_input2))
    yield part3(parse_data_part3(puzzle_input3))


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = solve(*puzzle_inputs)
        print("\n".join(str(solution) for solution in solutions))
