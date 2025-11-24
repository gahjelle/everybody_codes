"""Everybody Codes 6, 2024: The Tree of Titans"""

import collections
import itertools
from collections.abc import Generator


def part1(puzzle_input: str) -> str:
    """Solve part 1."""
    path = find_unique_path(parse_tree(puzzle_input), root="RR")
    return "".join(path)


def part2(puzzle_input: str) -> str:
    """Solve part 2."""
    path = find_unique_path(parse_tree(puzzle_input), root="RR")
    return "".join(node[0] for node in path)


part3 = part2


def parse_tree(puzzle_input: str) -> dict[str, list[str]]:
    """Parse the puzzle input into a dictionary"""
    tree = {}
    for line in puzzle_input.split("\n"):
        node, _, children = line.partition(":")
        tree[node] = children.split(",")
    return tree


def find_unique_path(tree: dict[str, list[str]], root: str) -> list[str]:
    """Find the path with a unique length in the tree"""
    return next(
        unique[0]
        for _, paths in itertools.groupby(walk_tree(tree, root), key=len)
        if len(unique := list(paths)) == 1
    )


def walk_tree(tree: dict[str, list[str]], root: str) -> Generator[list[str]]:
    """Walk the tree, starting at node. Yield all paths to fruits"""
    queue = collections.deque([(root, [])])

    while queue:
        node, path = queue.popleft()
        if node == "@":
            yield path + [node]
        else:
            for branch in tree.get(node, []):
                queue.append((branch, path + [node]))
