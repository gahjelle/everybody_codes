"""Everybody Codes quest 4, 2024: Royal Smith's Puzzle."""


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    nails = [int(nail) for nail in puzzle_input.split()]
    return sum(nails) - min(nails) * len(nails)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    nails = [int(nail) for nail in puzzle_input.split()]

    # Search for best target, start at approximate mean
    target = sum(nails) // len(nails)
    min_strikes = count_strikes(nails, target)
    step = -(2**12) if count_strikes(nails, target - 1) < min_strikes else 2**12
    while True:
        target += step
        num_strikes = count_strikes(nails, target)
        if num_strikes > min_strikes:
            if abs(step) == 1:
                return min_strikes
            else:
                step //= -8
        min_strikes = num_strikes


def count_strikes(nails: list[int], target: int) -> int:
    """Count the number of strikes necessary for all nails to reach target length.

    ## Example

    >>> count_strikes([3, 4, 7, 8], target=3)
    10
    >>> count_strikes([2, 4, 5, 6, 8], target=5)
    8
    >>> count_strikes([12, 4, 6, 9, 7, 5, 5], target=4)
    20
    >>> count_strikes([12, 4, 6, 9, 7, 5, 5], target=6)
    14
    """
    return sum(abs(nail - target) for nail in nails)
