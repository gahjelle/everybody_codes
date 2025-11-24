"""Everybody Codes quest 8, 2025: The Art of Connection."""

import itertools


def parse(puzzle_input: str) -> tuple[int, list[tuple[int, int]]]:
    """Parse the input into number of nails and a list of threads."""
    nails = [int(number) for number in puzzle_input.split(",")]
    return (
        max(nails),
        [
            (min(a, b), max(a, b))
            for a, b in list(zip(nails[:-1], nails[1:], strict=True))
        ],
    )


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    num_nails, strings = parse(puzzle_input)
    center_diff = num_nails // 2
    return sum(abs(end - start) == center_diff for start, end in strings)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    _, strings = parse(puzzle_input)

    count = 0
    strung = []
    for start, end in strings:
        count += sum(start < s < end < e or s < start < e < end for s, e in strung)
        strung.append((start, end))
    return count


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    num_nails, strings = parse(puzzle_input)

    # Tabulate strings
    string = [[0] * (num_nails + 1) for _ in range(num_nails + 1)]
    for s, e in strings:
        string[s][e] += 1
        string[e][s] += 1

    # Cumulative number of strings
    cs = [[0] * (num_nails + 1) for _ in range(num_nails + 1)]
    for s, e in itertools.product(range(1, num_nails + 1), range(1, num_nails + 1)):
        cs[s][e] = cs[s][e - 1] + string[s][e]

    # Move through possible cuts
    best = 0
    for start in range(1, num_nails - 1):
        num_cuts = 0
        for end in range(start + 2, num_nails + 1):
            # Add strings to the "next half" from previous endpoint
            num_cuts += cs[end - 1][num_nails] - cs[end - 1][end]
            num_cuts += cs[end - 1][start - 1]  # Sector before start
            # Remove strings to endpoint from earlier in sweep
            num_cuts -= cs[end][end - 1] - cs[end][start]
            best = max(best, num_cuts + string[start][end])
    return best
