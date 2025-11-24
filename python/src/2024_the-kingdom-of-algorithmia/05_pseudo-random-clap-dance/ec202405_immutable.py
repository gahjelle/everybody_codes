"""Everybody Codes 5, 2024: Pseudo-Random Clap Dance"""

# Standard library imports
import collections
import itertools

NUM_COLUMNS = 4


def parse_columns(puzzle_input):
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


def part1(puzzle_input):
    """Solve part 1."""
    columns = parse_columns(puzzle_input)
    for clapper in range(10):
        columns = shuffle(columns, clapper % NUM_COLUMNS)

    return int("".join(str(column[0]) for column in columns))


def part2(puzzle_input):
    """Solve part 2."""
    columns = parse_columns(puzzle_input)

    shouts = collections.defaultdict(int)
    for round in itertools.count(start=1):
        columns = shuffle(columns, (round - 1) % NUM_COLUMNS)
        round_shout = tuple(column[0] for column in columns)
        shouts[round_shout] += 1
        if shouts[round_shout] == 2024:
            return round * int("".join(str(digit) for digit in round_shout))


def part3(puzzle_input):
    """Solve part 3."""
    columns = parse_columns(puzzle_input)
    shouts = set()
    seen_columns = set()

    for round in itertools.count(start=1):
        columns = shuffle(columns, (round - 1) % NUM_COLUMNS)
        shouts.add("".join(str(column[0]) for column in columns))
        col_fingerprint = (round % NUM_COLUMNS,) + tuple(tuple(col) for col in columns)
        if col_fingerprint in seen_columns:
            return int(max(shouts))
        seen_columns.add(col_fingerprint)


def shuffle(columns, clapper_col):
    """Perform one shuffle of the dance"""
    clapper, *prev_col = columns[clapper_col]
    next_col = columns[(clapper_col + 1) % NUM_COLUMNS]
    num_moves = abs((clapper % (len(next_col) * 2)) - 1)
    new_idx = num_moves if num_moves <= len(next_col) else 2 * len(next_col) - num_moves

    if clapper_col == NUM_COLUMNS - 1:
        return (
            [next_col[:new_idx] + [clapper] + next_col[new_idx:]]
            + columns[1:clapper_col]
            + [prev_col]
        )
    else:
        return (
            columns[:clapper_col]
            + [prev_col]
            + [next_col[:new_idx] + [clapper] + next_col[new_idx:]]
            + columns[clapper_col + 2 :]
        )
