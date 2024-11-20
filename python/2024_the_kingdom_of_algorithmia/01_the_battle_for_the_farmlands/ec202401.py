"""Everybody Codes 1, 2024: The Battle For the Farmlands"""

# Standard library imports
import itertools
import sys
from pathlib import Path

POTIONS = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}


def part1(puzzle_input):
    """Solve part 1."""
    return calculate_potions(puzzle_input)


def part2(puzzle_input):
    """Solve part 2."""
    return calculate_potions(itertools.batched(puzzle_input, 2))


def part3(puzzle_input):
    """Solve part 3."""
    return calculate_potions(itertools.batched(puzzle_input, 3))


def calculate_potions(insects):
    """Calculate number of potions needed to fight off all insects

    ## Example

    >>> calculate_potions(["AB", "Dx", "xx", "CB", "AA"])  # 3 + 5 + 0 + 6 + 2
    16
    """
    return sum(
        (
            sum(POTIONS[insect] for insect in battle)
            + (num := sum(insect != "x" for insect in battle)) * (num - 1)
        )
        for battle in insects
    )


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
