"""Everybody Codes 5, 2024: Pseudo-Random Clap Dance"""

import collections
import itertools

NUM_COLUMNS = 4


def parse_columns(puzzle_input: str) -> list[list[int]]:
    """Parse puzzle input into columns."""
    return [
        list(column)
        for column in zip(
            *[
                [int(person) for person in line.split()]
                for line in puzzle_input.split("\n")
            ]
        )
    ]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    columns = parse_columns(puzzle_input)

    for round in range(10):
        shuffle(columns, round)
    return int("".join(str(column[0]) for column in columns))


def part2(puzzle_input: str, target: int = 2024) -> int:
    """Solve part 2."""
    columns = parse_columns(puzzle_input)

    num_shouts = collections.defaultdict(int)
    for round in itertools.count():
        shuffle(columns, round)
        shout = tuple(column[0] for column in columns)
        num_shouts[shout] += 1
        if num_shouts[shout] == target:
            return (round + 1) * int("".join(str(digit) for digit in shout))
    raise ValueError


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    columns = parse_columns(puzzle_input)

    shouts = set()
    seen_columns = set()
    for round in itertools.count():
        shuffle(columns, round)
        shouts.add("".join(str(column[0]) for column in columns))
        col_fingerprint = (round % NUM_COLUMNS,) + tuple(tuple(col) for col in columns)
        if col_fingerprint in seen_columns:
            return int(max(shouts))
        seen_columns.add(col_fingerprint)
    raise ValueError


def shuffle(columns: list[list[int]], round: int) -> None:
    """Perform one shuffle of the dance"""
    clapper = columns[round % NUM_COLUMNS].pop(0)
    to_column = columns[(round + 1) % NUM_COLUMNS]
    num_moves = (clapper - 1) % (len(to_column) * 2)
    new_idx = min(num_moves, 2 * len(to_column) - num_moves)
    to_column.insert(new_idx, clapper)
