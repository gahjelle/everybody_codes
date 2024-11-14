"""Everybody Codes 4, 2024: Royal Smith's Puzzle"""

# Standard library imports
import sys
from pathlib import Path


def part1(puzzle_input):
    """Solve part 1."""
    nails = [int(nail) for nail in puzzle_input.split()]
    return sum(nails) - min(nails) * len(nails)


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3."""
    nails = [int(nail) for nail in puzzle_input.split()]

    # Search for best target, start at approximate mean
    target = sum(nails) // len(nails)
    min_strikes = count_strikes(nails, target)
    step = -(2**12) if count_strikes(nails, target - 1) < min_strikes else 2**12
    while True:
        target += step
        num_strikes = count_strikes(nails, target)
        if num_strikes > min_strikes:
            if abs(step) == 1:
                return min_strikes
            else:
                step //= -8
        min_strikes = num_strikes


def count_strikes(nails, target):
    """Count the number of strikes necessary for all nails to reach target length.

    ## Example

    >>> count_strikes([3, 4, 7, 8], target=3)
    10
    >>> count_strikes([2, 4, 5, 6, 8], target=5)
    8
    >>> count_strikes([12, 4, 6, 9, 7, 5, 5], target=4)
    20
    >>> count_strikes([12, 4, 6, 9, 7, 5, 5], target=6)
    14
    """
    return sum(abs(nail - target) for nail in nails)


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
