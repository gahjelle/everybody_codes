"""Everybody Codes quest 3, 2025: The Deepest Fit."""

from collections import Counter


def parse_crates(puzzle_input: str) -> list[int]:
    """Parse the puzzle input into a list of crate sizes."""
    return [int(crate) for crate in puzzle_input.split(",")]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    crates = parse_crates(puzzle_input)
    return sum(set(crates))


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    crates = parse_crates(puzzle_input)
    return sum(sorted(set(crates))[:20])


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    crates = parse_crates(puzzle_input)
    return max(Counter(crates).values())
