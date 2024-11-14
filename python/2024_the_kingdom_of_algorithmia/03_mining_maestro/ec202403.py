"""Everybody Codes 3, 2024: Mining Maestro"""

# Standard library imports
import sys
from pathlib import Path


def parse_data(puzzle_input):
    """Parse map into set of coordinates"""
    return {
        (row, col)
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char == "#"
    }


def part1(puzzle_input):
    """Solve part 1."""
    return solve(puzzle_input, neighbors_4)


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3."""
    return solve(puzzle_input, neighbors_8)


def solve(puzzle_input, neighbors):
    """Solve the puzzle for the given number of neighbors"""
    coords = parse_data(puzzle_input)
    return count_blocks(coords, neighbors)


def count_blocks(coords, neighbors):
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


def neighbors_4(point):
    """List neighbors of the given point, adjacent only.

    ## Example

    >>> sorted(neighbors_4((2, 5)))
    [(1, 5), (2, 4), (2, 6), (3, 5)]
    """
    row, col = point
    return {(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)}


def neighbors_8(point):
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


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
