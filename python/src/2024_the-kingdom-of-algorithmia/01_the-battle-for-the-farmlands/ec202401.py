"""Everybody Codes quest 1, 2024: The Battle For the Farmlands."""

POTIONS = {"A": 0, "B": 1, "C": 3, "D": 5, "x": 0}


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    return calculate_potions(_batched(puzzle_input, 1))


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return calculate_potions(_batched(puzzle_input, 2))


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    return calculate_potions(_batched(puzzle_input, 3))


def calculate_potions(insects: list[str]) -> int:
    """Calculate number of potions needed to fight off all insects

    ## Example

    >>> calculate_potions(["AB", "Dx", "xx", "CB", "AA"])  # 3 + 5 + 0 + 6 + 2
    16
    """
    return sum(
        (
            sum(POTIONS[insect] for insect in battle)
            + (num := sum(insect != "x" for insect in battle)) * (num - 1)
        )
        for battle in insects
    )


def _batched(string: str, size: int) -> list[str]:
    """Batch a string into substrings of the given size.

    In Python 3.12 and later, use itertools.batched() instead.

    ## Example
    >>> _batched("ABDxxxCBAA", 2)
    ['AB', 'Dx', 'xx', 'CB', 'AA']
    """
    return [string[idx : idx + size] for idx in range(0, len(string), size)]
