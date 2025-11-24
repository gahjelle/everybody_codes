"""Everybody Codes quest 7, 2025: Namegraph."""


def parse(puzzle_input: str) -> tuple[list[str], dict[str, list[str]]]:
    names, rules = puzzle_input.split("\n\n")
    return (
        names.split(","),
        {
            first: followers.split(",")
            for line in rules.splitlines()
            for first, followers in [line.split(" > ")]
        },
    )


def part1(puzzle_input: str) -> str:
    """Solve part 1."""
    names, rules = parse(puzzle_input)
    return next((name for name in names if is_valid(name, rules)), "")


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    names, rules = parse(puzzle_input)
    return sum(idx for idx, name in enumerate(names, start=1) if is_valid(name, rules))


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    prefixes, rules = parse(puzzle_input)

    num_names = 0
    for prefix in prefixes:
        if not is_valid(prefix, rules) or any(
            prefix.startswith(other) and prefix != other for other in prefixes
        ):
            continue
        num_names += count(prefix[-1], rules, len(prefix))

    return num_names


def is_valid(name: str, rules: dict[str, list[str]]) -> bool:
    """Check whether a name satisfies the given rules.

    ## Examples:

    >>> is_valid("EvCo", {"E": {"v"}, "v": {"C"}, "C": {"o"}})
    True
    >>> is_valid("every", {"e": {"r", "v"}, "v": {"a", "e"}, "r": {"e", "r"}})
    False
    """
    return all(
        after in rules.get(before, [])
        for before, after in zip(name[:-1], name[1:], strict=True)
    )


CACHE: dict[tuple[str, int], int] = {}


def count(
    letter: str,
    rules: dict[str, list[str]],
    curr_length: int,
    min_length: int = 7,
    max_length: int = 11,
) -> int:
    """Count the number of possible words."""
    cached = CACHE.get((letter, max_length - curr_length))
    if cached is not None:
        return cached
    if curr_length == max_length:
        return 1
    return (curr_length >= min_length) + sum(
        count(after, rules, curr_length + 1, min_length, max_length)
        for after in rules.get(letter, list())
    )
