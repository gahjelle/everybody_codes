"""Everybody Codes 8, 2024: A Shrine for Nullpointer"""

# Standard library imports
import sys
from pathlib import Path


def part1(puzzle_input):
    """Solve part 1."""
    available = int(puzzle_input)
    num_blocks, base = 1, 1
    while num_blocks < available:
        base += 2
        num_blocks += base
    return (num_blocks - available) * base


def part2(puzzle_input, acolytes=1_111, available=20_240_000):
    """Solve part 2."""
    num_priests = int(puzzle_input)
    num_blocks, base, thickness = 1, 1, 1
    while num_blocks < available:
        thickness = (thickness * num_priests) % acolytes
        base += 2
        num_blocks += base * thickness
    return (num_blocks - available) * base


def part3(puzzle_input, acolytes=10, available=202_400_000):
    """Solve part 3."""
    num_priests = int(puzzle_input)
    num_blocks, base, thickness = 1, 1, 1
    columns = [1]
    while True:
        thickness = (thickness * num_priests) % acolytes + acolytes
        columns = [current + thickness for current in columns] + [thickness]
        base += 2
        num_blocks += base * thickness

        # Skip unnecessary calculation of blocks to remove
        if num_blocks < available:
            continue

        # Count number of blocks to remove
        remove = [(num_priests * base * current) % acolytes for current in columns[:-1]]
        num_remove = remove[0] + sum(remove[1:]) * 2
        if num_blocks - num_remove >= available:
            return num_blocks - num_remove - available


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
