"""Everybody Codes quest 3, 2024: Mining Maestro."""

from collections.abc import Callable

Point = tuple[int, int]


def parse_data(puzzle_input: str) -> set[Point]:
    """Parse map into set of coordinates"""
    return {
        (row, col)
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char == "#"
    }


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    return solve(puzzle_input, neighbors_4)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return solve(puzzle_input, neighbors_4)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    return solve(puzzle_input, neighbors_8)


def solve(puzzle_input: str, neighbors: Callable[[Point], set[Point]]) -> int:
    """Solve the puzzle for the given number of neighbors"""
    coords = parse_data(puzzle_input)
    return count_blocks(coords, neighbors)


def count_blocks(coords: set[Point], neighbors: Callable[[Point], set[Point]]) -> int:
    """Count the number of blocks that can be dug on the given map.

    ## Example:

        .#.        .1.        .1.
        ###   ->   111   ->   121
        .#.        .1.        .1.

    >>> count_blocks({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}, neighbors_4)
    6
    """
    if not coords:
        return 0
    return len(coords) + count_blocks(
        {coord for coord in coords if not neighbors(coord) - coords}, neighbors
    )


def neighbors_4(point: Point) -> set[Point]:
    """List neighbors of the given point, adjacent only.

    ## Example

    >>> sorted(neighbors_4((2, 5)))
    [(1, 5), (2, 4), (2, 6), (3, 5)]
    """
    row, col = point
    return {(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)}


def neighbors_8(point: Point) -> set[Point]:
    """List neighbors of the given point, including diagonally.

    ## Example

    >>> sorted(neighbors_8((2, 5)))
    [(1, 4), (1, 5), (1, 6), (2, 4), (2, 6), (3, 4), (3, 5), (3, 6)]
    """
    row, col = point
    return {
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    }
