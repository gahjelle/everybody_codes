"""Everybody Codes quest 2, 2025: From Complex to Clarity."""

import itertools


def parse(puzzle_input: str) -> complex:
    """Parse the puzzle input."""
    return complex(
        *map(int, puzzle_input[2:].replace("[", "").replace("]", "").split(","))
    )


def part1(puzzle_input: str) -> str:
    """Solve part 1."""
    point = parse(puzzle_input)

    result = 0j
    for _ in range(3):
        result = int_div(result * result, 10) + point
    return f"[{int(result.real)},{int(result.imag)}]"


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    ul_corner = parse(puzzle_input)
    return sum(
        escape(ul_corner + x + y * 1j) is None
        for x, y in itertools.product(range(0, 1001, 10), range(0, 1001, 10))
    )


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    ul_corner = parse(puzzle_input)
    return sum(
        escape(ul_corner + x + y * 1j) is None
        for x, y in itertools.product(range(1001), range(1001))
    )


def int_div(z: complex, factor: int) -> complex:
    """Divide a complex number and only keep the integer parts.

    ## Example:

    >>> int_div(14 - 42j, 10)
    (1-4j)
    """
    res = z / factor
    return int(res.real) + int(res.imag) * 1j


def escape(point: complex) -> int | None:
    """Check whether to engrave the given point by checking if it escapes.

    ## Examples

    >>> escape(35630-64880j) is None
    True

    >>> escape(35460-64910j)
    27
    """
    result = 0j
    for cycle in range(1, 101):
        result = int_div(result * result, 100_000) + point
        if (
            result.real < -1_000_000
            or result.real > 1_000_000
            or result.imag < -1_000_000
            or result.imag > 1_000_000
        ):
            return cycle
    return None
