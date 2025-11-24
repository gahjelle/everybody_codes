"""Everybody Codes quest 8, 2025: The Art of Connection."""


def parse(puzzle_input: str) -> tuple[int, list[tuple[int, int]]]:
    """Parse the input into number of nails and a list of threads."""
    nails = [int(number) for number in puzzle_input.split(",")]
    return (max(nails), list(zip(nails[:-1], nails[1:], strict=True)))


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    num_nails, strings = parse(puzzle_input)
    center_diff = num_nails // 2
    return sum(abs(end - start) == center_diff for start, end in strings)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    _, strings = parse(puzzle_input)

    # return sum(
    #     sum(does_cut(start, end, s, e) for s, e in strings[:idx])
    #     for idx, (start, end) in enumerate(strings[1:], start=1)
    # )

    count = 0
    strung = []
    for start, end in strings:
        count += sum(does_cut(start, end, s, e) for s, e in strung)
        strung.append((start, end))
    return count


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    num_nails, strings = parse(puzzle_input)
    num_cuts = [
        (
            ((start, end) in strings or (end, start) in strings)
            + sum(does_cut(start, end, s, e) for s, e in strings)
        )
        for start in range(1, num_nails - 1)
        for end in range(start + 2, num_nails + 1)
    ]
    return max(num_cuts)


def does_cut(start: int, end: int, s: int, e: int) -> bool:
    """Check if (start, end) cuts over (s, e)."""
    return ordered(start, s, end, e) or ordered(start, e, end, s)


def ordered(a: int, b: int, c: int, d: int) -> bool:
    """Check whether the given numbers are strictly ordered on a circle."""
    circled = False
    for first, second in [(a, b), (b, c), (c, d), (d, a)]:
        if first == second:
            return False
        if first > second:
            if circled:
                return False
            circled = True
    return True
