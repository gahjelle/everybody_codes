"""Everybody Codes 16, 2024: Cat Grin of Fortune.

Thanks to https://github.com/AllanTaylor314/EverybodyCodes/ for help on part 3.
"""

import collections
import functools
import math
from typing import TypeAlias

Steps: TypeAlias = tuple[int, ...]  # Use tuple to be able to cache later
Wheels: TypeAlias = tuple[tuple[str, ...], ...]


def parse(puzzle_input: str, *, eyes_only: bool = False) -> tuple[Steps, Wheels]:
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


def part1(puzzle_input: str, rounds: int = 100) -> str:
    """Solve part 1."""
    steps, wheels = parse(puzzle_input)
    return " ".join(
        wheel[rounds * step % len(wheel)] for step, wheel in zip(steps, wheels)
    )


def part2(puzzle_input: str, rounds: int = 2024_2024_2024) -> int:
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


def part3(puzzle_input: str, rounds: int = 256) -> str:
    """Solve part 3."""
    steps, wheels = parse(puzzle_input, eyes_only=True)
    max_coins, min_coins = find_max_min(wheels, steps, 0, 0, rounds)
    return f"{max_coins} {min_coins}"


def pull_right_lever(wheels: Wheels, steps: Steps, num_right: int) -> int:
    """Pull the right lever the given number of times"""
    line = "".join(
        wheel[(step * num_right) % len(wheel)] for wheel, step in zip(wheels, steps)
    )
    return sum(count - 2 for count in collections.Counter(line).values() if count >= 3)


@functools.cache
def find_max_min(
    wheels: Wheels, steps: Steps, num_right: int, num_left: int, rounds: int
) -> tuple[int, int]:
    """Find the max and min coins possible in the given number of rounds."""
    line = "".join(
        wheel[(step * num_right + num_left) % len(wheel)]
        for wheel, step in zip(wheels, steps)
    )
    num_coins = (
        sum(count - 2 for count in collections.Counter(line).values() if count >= 3)
        if num_right > 0
        else 0
    )
    if rounds == 0:
        return num_coins, num_coins

    max_coins, min_coins = zip(
        *(
            find_max_min(
                wheels, steps, num_right + 1, num_left + round_left, rounds - 1
            )
            for round_left in [-1, 0, 1]
        )
    )
    return num_coins + max(max_coins), num_coins + min(min_coins)
