"""Everybody Codes 17, 2024: Galactic Geometry"""

import math
from typing import TypeAlias

Star: TypeAlias = tuple[int, int]
Stars: TypeAlias = list[Star]
Constellation: TypeAlias = list[tuple[Star, Star]]


def parse_stars(puzzle_input: str) -> Stars:
    """Parse the input."""
    return [
        (row, col)
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char == "*"
    ]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    stars = parse_stars(puzzle_input)
    (constellation,) = create_constellations(stars)  # There should be exactly one
    return size(constellation)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    stars = parse_stars(puzzle_input)
    sizes = [size(group) for group in create_constellations(stars, max_distance=6)]
    return math.prod(sorted(sizes)[-3:])


def size(edges: Constellation) -> int:
    """Calculate the size of a constellation.

    The size is defined to be the number of stars plus the sum of all edge
    lengths.

    ## Example

    >>> size([((1,5), (3,4)), ((5,5), (3,4)), ((3,4), (3,1)), ((1,1), (3,1))])
    16
    """
    return (len(edges) + 1) + sum(manhattan(first, second) for first, second in edges)


def create_constellations(stars: Stars, max_distance: int = 999) -> list[Constellation]:
    """Create one or more constellations based on the given stars."""
    first, *rest = stars
    distances = {star: (manhattan(star, first), first) for star in rest}
    constellation = []
    while distances:
        new_star, (distance, from_star) = min(
            distances.items(), key=lambda item: item[1]
        )
        if distance >= max_distance:
            return create_constellations(list(distances), max_distance) + [
                constellation
            ]

        constellation.append((from_star, new_star))
        distances = {  # Inline Manhattan calculation for performance
            star: min(
                distances[star],
                (abs(new_star[0] - star[0]) + abs(new_star[1] - star[1]), new_star),
            )
            for star in distances
            if star != new_star
        }
    return [constellation]


def manhattan(first: Star, second: Star) -> int:
    """Find the Manhattan distance between two stars."""
    row1, col1 = first
    row2, col2 = second
    return abs(row2 - row1) + abs(col2 - col1)
