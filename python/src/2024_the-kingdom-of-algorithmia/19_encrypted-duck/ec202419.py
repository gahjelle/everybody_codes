"""Everybody Codes 19, 2024: Encrypted Duck."""

import itertools
from typing import TypeAlias

Coordinate: TypeAlias = tuple[int, int]
Grid: TypeAlias = dict[Coordinate, str]


def parse(puzzle_input: str) -> tuple[str, Grid]:
    """Parse the input."""
    key, grid = puzzle_input.split("\n\n")
    return key, {
        (row, col): char
        for row, line in enumerate(grid.split("\n"))
        for col, char in enumerate(line)
    }


def part1(puzzle_input: str, rounds: int = 1) -> str:
    """Solve part 1."""
    return part(puzzle_input, rounds)


def part2(puzzle_input: str, rounds: int = 100) -> str:
    """Solve part 2."""
    return part(puzzle_input, rounds)


def part3(puzzle_input: str, rounds: int = 1_048_576_000) -> str:
    """Solve part 3."""
    return part(puzzle_input, rounds)


def part(puzzle_input: str, rounds: int, *, display_grid: bool = False) -> str:
    """Solve a single part."""
    key, grid = parse(puzzle_input)
    decoded_grid = decode(grid, key, num_rounds=rounds)

    if display_grid:
        display(decoded_grid)
    return find_message(decoded_grid)


def rotate(grid: Grid, key: str) -> Grid:
    """Rotate the grid once around all rotation points."""
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    max_row, max_col = max(grid)
    for (row, col), direction in zip(
        itertools.product(range(1, max_row), range(1, max_col)), itertools.cycle(key)
    ):
        cells = [(row + dr, col + dc) for dr, dc in deltas + deltas[:1]]
        grid = grid | (
            {start: grid[end] for start, end in zip(cells, cells[1:])}
            if direction == "L"
            else {start: grid[end] for start, end in zip(cells[1:], cells)}
        )
    return grid


def find_permutation_cycles(grid: Grid, key: str) -> list[list[Coordinate]]:
    """Find the permutation cycles corresponding to one rotation."""
    transitions = {
        value: key for key, value in rotate({pos: pos for pos in grid}, key).items()
    }

    cycles = []
    seen = set()
    for start_pos in grid:
        if start_pos in seen:
            continue
        cycle = []
        pos = start_pos
        while pos not in seen:
            cycle.append(pos)
            seen.add(pos)
            pos = transitions[pos]
        cycles.append(cycle)
    return cycles


def decode(grid: Grid, key: str, num_rounds: int) -> Grid:
    """Decode a message grid."""
    cycles = find_permutation_cycles(grid, key)
    return {
        cycle[(idx + num_rounds) % len(cycle)]: grid[pos]
        for cycle in cycles
        for idx, pos in enumerate(cycle)
    }


def find_message(grid: Grid) -> str:
    """Find the message hidden in the grid.

    Assumes the message is in one row.
    """
    row, start_col = next((pos for pos, char in grid.items() if char == ">"), (0, 0))
    _, end_col = next((pos for pos, char in grid.items() if char == "<"), (0, 0))

    return "".join(grid[row, col] for col in range(start_col + 1, end_col))


def display(grid: Grid) -> None:
    """Display the grid on the console."""
    max_row, max_col = max(grid)
    for row in range(max_row + 1):
        for col in range(max_col + 1):
            print(grid[row, col], end="")
        print()
