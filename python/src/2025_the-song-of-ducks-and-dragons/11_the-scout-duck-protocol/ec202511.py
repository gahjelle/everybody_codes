"""Everybody Codes quest 11, 2025: The Scout Duck Protocol."""

import itertools


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    birds = [int(num) for num in puzzle_input.splitlines()]

    phase_1 = True
    for _ in range(10):
        if phase_1:
            birds = move_right(birds)
            if all(left <= right for left, right in itertools.pairwise(birds)):
                phase_1 = False
        else:
            birds = move_left(birds)
    return checksum(birds)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    birds = [int(num) for num in puzzle_input.splitlines()]
    target = sum(birds) // len(birds)

    round = 0
    while True:
        round += 1
        birds = move_right(birds)
        if all(left <= right for left, right in itertools.pairwise(birds)):
            break

    return round + sum(abs(b - target) for b in birds) // 2


def part3(puzzle_input: str) -> int:
    """Solve part 3.

    Part 3 has special input where the birds are already in the second phase.
    During the second phase, exactly two columns changes the number of birds
    each round.
    """
    birds = [int(num) for num in puzzle_input.splitlines()]
    target = sum(birds) // len(birds)
    return sum(abs(b - target) for b in birds) // 2


def move_right(birds: list[int]) -> list[int]:
    """Move birds to the right."""
    new_birds = birds[:]
    for f_col, t_col in itertools.pairwise(range(len(birds))):
        if new_birds[f_col] > new_birds[t_col]:
            new_birds[f_col] -= 1
            new_birds[t_col] += 1
    return new_birds


def move_left(birds: list[int]) -> list[int]:
    """Move birds to the left."""
    new_birds = birds[:]
    for t_col, f_col in itertools.pairwise(range(len(birds))):
        if new_birds[f_col] > new_birds[t_col]:
            new_birds[f_col] -= 1
            new_birds[t_col] += 1
    return new_birds


def checksum(birds: list[int]) -> int:
    """Calculate a checksum by multiplying each column by its index."""
    return sum(idx * num for idx, num in enumerate(birds, start=1))
