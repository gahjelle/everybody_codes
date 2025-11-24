"""Everybody Codes quest 16, 2025: Harmonics of Stone."""

import math


def parse(puzzle_input: str) -> list[int]:
    """Parse the input."""
    return [int(number) for number in puzzle_input.split(",")]


def part1(puzzle_input: str, num_columns=90) -> int:
    """Solve part 1."""
    spell = parse(puzzle_input)
    return count_blocks(spell, num_columns=num_columns)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    wall = parse(puzzle_input)
    return math.prod(find_spell(wall))


def part3(puzzle_input: str, num_blocks=202_520_252_025_000) -> int:
    """Solve part 3."""
    wall = parse(puzzle_input)
    spell = find_spell(wall)

    # Binary search on the number of columns
    lo, hi = 0, num_blocks
    while hi - lo > 1:
        mid = (lo + hi) // 2
        mid_blocks = count_blocks(spell, mid)
        if mid_blocks <= num_blocks:
            lo = mid
        else:
            hi = mid
    return lo


def count_blocks(spell: list[int], num_columns: int) -> int:
    """Count the number of blocks used in the given number of columns."""
    return sum(num_columns // number for number in spell)


def find_spell(wall: list[int]) -> list[int]:
    """Find the spell that created the given wall."""
    spell = []
    for idx, number in enumerate(wall, start=1):
        current = sum(idx % n == 0 for n in spell)
        if current < number:
            spell.append(idx)
    return spell
