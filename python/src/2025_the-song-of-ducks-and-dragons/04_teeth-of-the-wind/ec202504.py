"""Everybody Codes quest 4, 2025: Teeth of the Wind."""

import math


def parse_gears(puzzle_input: str) -> list[int]:
    """Parse gears. Double gears are parsed into a flat list."""
    return [int(gear) for gear in puzzle_input.replace("|", "\n").splitlines()]


def part1(puzzle_input: str, num_turns=2025) -> int:
    """Solve part 1."""
    first, *_, last = parse_gears(puzzle_input)
    return math.floor(num_turns * first / last)


def part2(puzzle_input: str, num_turns=10_000_000_000_000) -> int:
    """Solve part 2."""
    first, *_, last = parse_gears(puzzle_input)
    return math.ceil(num_turns * last / first)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    gears = parse_gears(puzzle_input)
    turns = 100
    for left, right in zip(gears[::2], gears[1::2], strict=True):
        turns *= left / right
    return math.floor(turns)
