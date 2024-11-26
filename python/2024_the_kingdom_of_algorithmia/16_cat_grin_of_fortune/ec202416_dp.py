"""Everybody Codes 16, 2024: Cat Grin of Fortune"""

# Standard library imports
import collections
import functools
import math
import sys
from pathlib import Path


def parse(puzzle_input, eyes_only=False):
    """Parse input."""
    steps_str, wheels_str = puzzle_input.split("\n\n")
    steps = [int(wheel) for wheel in steps_str.split(",")]
    num_cols = len(steps)
    wheels = tuple(
        tuple(cat[:: 1 + eyes_only] for cat in wheel if cat)
        for wheel in zip(
            *[
                [line[4 * idx : 4 * idx + 3].strip() for idx in range(num_cols)]
                for line in wheels_str.split("\n")
            ]
        )
    )
    return tuple(step % len(wheel) for step, wheel in zip(steps, wheels)), wheels


def part1(puzzle_input, rounds=100):
    """Solve part 1."""
    steps, wheels = parse(puzzle_input)
    return " ".join(
        wheel[rounds * step % len(wheel)] for step, wheel in zip(steps, wheels)
    )


def part2(puzzle_input, rounds=2024_2024_2024):
    """Solve part 2."""
    steps, wheels = parse(puzzle_input, eyes_only=True)
    period = math.lcm(*[len(wheel) for wheel in wheels])
    num_periods, partial_period = divmod(rounds, period)

    period_coins, partial_coins = 0, 0
    for round in range(1, period + 1):
        period_coins += pull_right_lever(wheels, steps, round)
        if round == partial_period:
            partial_coins = period_coins
    return num_periods * period_coins + partial_coins


def pull_right_lever(wheels, steps, right_lever):
    """Pull the right lever the given number of times"""
    line = "".join(
        wheel[(step * right_lever) % len(wheel)] for wheel, step in zip(wheels, steps)
    )
    return sum(count - 2 for count in collections.Counter(line).values() if count >= 3)


def part3(puzzle_input, rounds=256):
    """Solve part 3."""
    steps, wheels = parse(puzzle_input, eyes_only=True)
    max_coins, min_coins = find_max_min(wheels, steps, 0, 0, rounds)
    return f"{max_coins} {min_coins}"


@functools.cache
def find_max_min(wheels, steps, left_lever, right_lever, rounds):
    """Find the max and min coins possible in the given number of rounds."""
    line = "".join(
        wheel[(step * right_lever + left_lever) % len(wheel)]
        for wheel, step in zip(wheels, steps)
    )
    num_coins = (
        sum(count - 2 for count in collections.Counter(line).values() if count >= 3)
        if right_lever > 0
        else 0
    )
    if rounds == 0:
        return num_coins, num_coins

    max_coins, min_coins = zip(
        *(
            find_max_min(
                wheels, steps, left_lever + num_left, right_lever + 1, rounds - 1
            )
            for num_left in [-1, 0, 1]
        )
    )
    return num_coins + max(max_coins), num_coins + min(min_coins)


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
