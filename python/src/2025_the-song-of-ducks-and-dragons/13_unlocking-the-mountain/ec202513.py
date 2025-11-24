"""Everybody Codes quest 13, 2025: Unlocking the Mountain."""


def parse_numbers(puzzle_input: str) -> list[int]:
    """Parse numbers."""
    return [int(number) for number in puzzle_input.splitlines()]
    return [range(int(number), int(number) + 1) for number in puzzle_input.splitlines()]


def parse_ranges(puzzle_input: str) -> list[range]:
    """Parse ranges."""
    return [
        range(int(start), int(end) + 1)
        for line in puzzle_input.splitlines()
        for start, end in [line.split("-")]
    ]


def part1(puzzle_input: str, num_turns: int = 2025) -> int:
    """Solve part 1."""
    numbers = parse_numbers(puzzle_input)
    length = 1 + len(numbers)
    index = num_turns % length
    if index == 0:
        return 1
    elif index <= length // 2:
        return numbers[(index - 1) * 2]
    else:
        return numbers[(length - index) * 2 - 1]


def part2(puzzle_input: str, num_turns=20252025) -> int:
    """Solve part 2."""
    ranges = parse_ranges(puzzle_input)
    return turn_ranges(ranges, num_turns=num_turns)


def part3(puzzle_input: str, num_turns=202520252025) -> int:
    """Solve part 3."""
    return part2(puzzle_input, num_turns=num_turns)


def turn_ranges(ranges: list[range], num_turns: int) -> int:
    """Turn the wheel with ranges of numbers."""
    length = 1 + sum(len(rng) for rng in ranges)
    index = num_turns % length

    # Construct a wheel of ranges
    right: list[range] = []
    left: list[range] = []
    for idx, rng in enumerate(ranges):
        (left if idx % 2 else right).append(rng)
    wheel = [range(1, 2), *right, *[rng[::-1] for rng in left[::-1]]]

    # Find the correct index in the correct range
    for rng in wheel:
        if index < len(rng):
            return rng[index]
        index -= len(rng)
    return 0  # Should never end up here
