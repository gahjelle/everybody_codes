"""Everybody Codes 3, Story 1: The Conical Snail Clock"""

import itertools
import math
from typing import NamedTuple


class Snail(NamedTuple):
    x: int
    y: int


def parse(puzzle_input: str) -> list[Snail]:
    """Parse the puzzle input."""
    return [parse_snail(line) for line in puzzle_input.splitlines()]


def parse_snail(line: str) -> Snail:
    """Parse the description of one snail.

    ## Example

    >>> parse_snail("x=3 y=4")
    Snail(x=3, y=4)
    """
    return Snail(
        **{
            key: int(value)
            for coord in line.split()
            for key, _, value in [coord.partition("=")]
        }
    )


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    snails = parse(puzzle_input)
    return sum(
        score_snail(snail) for snail in [move_snail(snail, 100) for snail in snails]
    )


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    snails = parse(puzzle_input)
    first_day, _ = on_first_row(snails)
    return first_day


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    snails = parse(puzzle_input)
    first_day, _ = on_first_row(snails)
    return first_day


def on_first_row(snails: list[Snail]) -> tuple[int, int]:
    """Find when all snails are on the first row.

    Solve recursively. For one snail, the snail will be on the first row on day
    Y-1, and then it will return to the first row every X+Y-1 days.

    For a second snail, only look at days when the first snail is on the first
    row and pick the first day the second snail is also on the first row. Adjust
    the step size to continue to consider days when both snails are on the first
    row.

    Return a tuple of (first_day, step).

    ## Examples

    >>> on_first_row([Snail(3, 1)])
    (0, 3)

    >>> on_first_row([Snail(3, 1), Snail(1, 5)])
    (9, 15)

    >>> on_first_row([Snail(3, 1), Snail(1, 5), Snail(1, 11)])
    (54, 165)
    """
    *other_snails, snail = snails
    if not other_snails:
        return snail.y - 1, snail.x + snail.y - 1

    first_day, step = on_first_row(other_snails)
    for day in itertools.count(first_day, step=step):
        if (day - (snail.y - 1)) % (snail.x + snail.y - 1) == 0:
            return day, math.lcm(step, snail.x + snail.y - 1)

    raise RuntimeError("Unreachable")


def move_snail(snail: Snail, days: int) -> Snail:
    """Move one snail for a number of days.

    ## Examples

    >>> move_snail(Snail(3, 5), 2)
    Snail(x=5, y=3)

    >>> move_snail(Snail(3, 5), 6)
    Snail(x=2, y=6)

    >>> move_snail(Snail(3, 5), 11)
    Snail(x=7, y=1)
    """
    period = snail.x + snail.y - 1
    steps = days % period
    if snail.y - steps < 1:
        steps -= period
    return Snail(x=snail.x + steps, y=snail.y - steps)


def score_snail(snail: Snail) -> int:
    """Calculate a score based on a snail's position.

    ## Example

    >>> score_snail(Snail(28, 77))
    7728
    """
    return snail.x + 100 * snail.y
