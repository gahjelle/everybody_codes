"""Everybody Codes quest 7, 2025: Namegraph."""

from collections.abc import Generator


def parse(puzzle_input: str) -> tuple[list[str], dict[str, set[str]]]:
    names, rules = puzzle_input.split("\n\n")
    return (
        names.split(","),
        {
            first: set(followers.split(","))
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

    names = set()
    for prefix in prefixes:
        if not is_valid(prefix, rules):
            continue
        names |= set(generate(prefix, rules))

    return len(names)


def is_valid(name: str, rules: dict[str, set[str]]) -> bool:
    """Check whether a name satisfies the given rules.

    ## Examples:

    >>> is_valid("EvCo", {"E": {"v"}, "v": {"C"}, "C": {"o"}})
    True
    >>> is_valid("every", {"e": {"r", "v"}, "v": {"a", "e"}, "r": {"e", "r"}})
    False
    """
    for first, follows in zip(name[:-1], name[1:], strict=True):
        if follows not in rules.get(first, set()):
            return False
    return True


def generate(
    prefix: str, rules: dict[str, set[str]], min_length: int = 7, max_length: int = 11
) -> Generator[str]:
    """Generate all valid names starting with the given prefix.

    ## Example:

    >>> sorted(generate("eve", {"e": {"r", "v"}, "v": {"a", "e"}, "r": {"e", "r"}}, 3, 5))
    ['eve', 'ever', 'evere', 'everr', 'evev', 'eveva', 'eveve']
    """
    if min_length <= len(prefix) <= max_length:
        # print(prefix)
        yield prefix
    if len(prefix) >= max_length:
        return
    for follows in rules.get(prefix[-1], set()):
        yield from generate(f"{prefix}{follows}", rules, min_length, max_length)
