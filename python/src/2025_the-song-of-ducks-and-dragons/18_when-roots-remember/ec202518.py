"""Everybody Codes quest 18, 2025: When Roots Remember."""

import collections
import re
from collections.abc import Generator
from typing import TypeAlias

Branches: TypeAlias = dict[int, int]
Tree: TypeAlias = dict[int, tuple[int, Branches]]

PLANT = re.compile(r"Plant (?P<plant>\d+) with thickness (?P<thickness>-?\d+):")
BRANCHES = [
    re.compile(r"- free branch with thickness (?P<thickness>-?\d+)"),
    re.compile(r"- branch to Plant (?P<plant>\d+) with thickness (?P<thickness>-?\d+)"),
]


def parse_tree(puzzle_input: str) -> Tree:
    """Parse the tree of plants."""
    plants = puzzle_input.split("\n\n")

    tree = {}
    for plant_info in plants:
        plant_str, *branch_strs = plant_info.splitlines()
        plant_match = PLANT.match(plant_str)
        if plant_match is None:
            continue
        plant = {key: int(value) for key, value in plant_match.groupdict().items()}

        branches = {}
        for branch_str in branch_strs:
            branch_match = next(
                m for pattern in BRANCHES if (m := pattern.match(branch_str))
            )
            branch = {
                key: int(value) for key, value in branch_match.groupdict().items()
            }
            branches[branch.get("plant", 0)] = branch["thickness"]
        tree[plant["plant"]] = plant["thickness"], branches
    return tree


def parse_tests(puzzle_input: str) -> tuple[Tree, list[list[int]]]:
    """Parse the tree of plants and the relevant test cases."""
    tree, tests = puzzle_input.split("\n\n\n")
    return parse_tree(tree), [
        [int(number) for number in line.split()] for line in tests.splitlines()
    ]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    tree = parse_tree(puzzle_input)
    return calculate_energy(tree, max(tree))


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    tree, test_cases = parse_tests(puzzle_input)
    return sum(
        calculate_energy(tree, max(tree), init=dict(enumerate(test_case, start=1)))
        for test_case in test_cases
    )


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    tree, test_cases = parse_tests(puzzle_input)
    branches = collections.defaultdict(dict)
    for plant, (_, bs) in tree.items():
        for plant_to, thickness in bs.items():
            if plant_to > 0:
                branches[plant_to][plant] = thickness

    # Are all branches "uniform" in the sense that their thicknesses are either
    # all negative or all positive? If so, we find max when we activate all
    # positive branches
    uniform = all(
        all(tn * sum(tns.values()) > 0 for tn in tns.values())
        for tns in branches.values()
    )
    if uniform:
        init = {
            plant: 1 if sum(branches[plant].values()) > 0 else 0
            for plant, (_, bs) in tree.items()
            if 0 in bs
        }
        max_energy = calculate_energy(tree, plant=max(tree), init=init)
    else:
        max_energy = max(
            calculate_energy(tree, max(tree), init=init)
            for init in list_test_cases(len(test_cases[0]))
        )

    # Calculate the total distance to the maximal energy for the test cases
    total = 0
    for test_case in test_cases:
        energy = calculate_energy(
            tree, max(tree), init=dict(enumerate(test_case, start=1))
        )
        if energy > 0:
            total += max_energy - energy
    return total


def calculate_energy(tree: Tree, plant: int, init: dict[int, int] | None = None) -> int:
    """Calculate the energy of one plant."""
    if plant not in tree:
        return 1
    if init is not None and plant in init:
        return init[plant]

    thickness, others = tree[plant]
    energy = sum(
        calculate_energy(tree, other_plant, init=init) * other_thickness
        for other_plant, other_thickness in others.items()
    )
    return energy if energy >= thickness else 0


def list_test_cases(num_inits: int) -> Generator[dict[int, int]]:
    """Generate all possible test cases for the given number of inits."""
    for n in range(2**num_inits):
        yield dict(
            enumerate(int(b) for b in ("0" * num_inits + bin(n)[2:])[-num_inits:])
        )
