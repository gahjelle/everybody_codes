"""Everybody Codes 17, 2024: Galactic Geometry"""

# Standard library imports
import math
import sys
from pathlib import Path


def parse_stars(puzzle_input):
    """Parse the input."""
    return [
        (row, col)
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char == "*"
    ]


def part1(puzzle_input):
    """Solve part 1."""
    stars = parse_stars(puzzle_input)
    (constellation,) = create_constellations(stars)  # There should be exactly one
    return size(constellation)


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3."""
    stars = parse_stars(puzzle_input)
    sizes = [size(group) for group in create_constellations(stars, max_distance=6)]
    return math.prod(sorted(sizes)[-3:])


def size(edges):
    """Calculate the size of a constellation.

    The size is defined to be the number of stars plus the sum of all edge
    lengths.

    ## Example

    >>> size([((1,5), (3,4)), ((5,5), (3,4)), ((3,4), (3,1)), ((1,1), (3,1))])
    16
    """
    return (len(edges) + 1) + sum(manhattan(first, second) for first, second in edges)


def create_constellations(stars, max_distance=999):
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


def manhattan(first, second):
    """Find the Manhattan distance between two stars."""
    row1, col1 = first
    row2, col2 = second
    return abs(row2 - row1) + abs(col2 - col1)


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
