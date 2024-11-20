"""Everybody Codes 11, 2024: Biological Warfare"""

# Standard library imports
import collections
import sys
from pathlib import Path


def parse(puzzle_input):
    """Parse the puzzle input.

    Flip the dictionary to map children to their parents to simplify
    calculations later.
    """
    conversions = collections.defaultdict(list)
    for line in puzzle_input.split("\n"):
        parent, _, children = line.partition(":")
        for child in children.split(","):
            conversions[child].append(parent)
    return {
        child: collections.Counter(parents) for child, parents in conversions.items()
    }


def part1(puzzle_input):
    """Solve part 1."""
    conversions = parse(puzzle_input)
    print(conversions)
    return calculate_population(conversions, initial="A", num_days=4)


def part2(puzzle_input):
    """Solve part 2."""
    conversions = parse(puzzle_input)
    return calculate_population(conversions, initial="Z", num_days=10)


def part3(puzzle_input):
    """Solve part 3."""
    conversions = parse(puzzle_input)
    pop_sizes = [
        calculate_population(conversions, initial=termite, num_days=20)
        for termite in conversions.keys()
    ]
    return max(pop_sizes) - min(pop_sizes)


def grow_population(conversions, population):
    """Grow the population one day

    ## Example

    >>> conversions = {"B": {"A": 1}, "C": {"A": 1, "B": 1}, "A": {"B": 1, "C": 1}}
    >>> grow_population(conversions, {"B":1, "C": 1})
    {'B': 0, 'C': 1, 'A': 2}
    """
    return {
        termite: sum(
            population.get(parent, 0) * count for parent, count in parents.items()
        )
        for termite, parents in conversions.items()
    }


def calculate_population(conversions, initial, num_days):
    """Calculate the population after the given number of days.

    ## Example

        C -> A -> BC -> CAA -> ABCBC

    >>> conversions = {"B": {"A": 1}, "C": {"A": 1, "B": 1}, "A": {"B": 1, "C": 1}}
    >>> calculate_population(conversions, initial="C", num_days=4)
    5
    """
    population = {initial: 1}
    for _ in range(num_days):
        population = grow_population(conversions, population)
    return sum(population.values())


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
