"""Everybody Codes 6, 2024: The Tree of Titans"""

# Standard library imports
import collections
import itertools
import sys
from pathlib import Path


def part1(puzzle_input):
    """Solve part 1."""
    path = find_unique_path(parse_tree(puzzle_input), root="RR")
    return "".join(path)


def part2(puzzle_input):
    """Solve part 2."""
    path = find_unique_path(parse_tree(puzzle_input), root="RR")
    return "".join(node[0] for node in path)


part3 = part2


def parse_tree(puzzle_input):
    """Parse the puzzle input into a dictionary"""
    tree = {}
    for line in puzzle_input.split("\n"):
        node, _, children = line.partition(":")
        tree[node] = children.split(",")
    return tree


def find_unique_path(tree, root):
    """Find the path with a unique length in the tree"""
    return next(
        unique[0]
        for _, paths in itertools.groupby(walk_tree(tree, root), key=len)
        if len(unique := list(paths)) == 1
    )


def walk_tree(tree, root):
    """Walk the tree, starting at node. Yield all paths to fruits"""
    queue = collections.deque([(root, [])])

    while queue:
        node, path = queue.popleft()
        if node == "@":
            yield path + [node]
        else:
            for branch in tree.get(node, []):
                queue.append((branch, path + [node]))


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
