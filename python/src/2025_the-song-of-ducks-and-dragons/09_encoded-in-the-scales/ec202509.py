"""Everybody Codes quest 9, 2025: Encoded in the Scales."""

import itertools
from collections import defaultdict, deque
from collections.abc import Generator


def parse(puzzle_input: str) -> tuple[int, dict[int, int]]:
    """Parse the input into a dictionary of scales."""
    lines = puzzle_input.splitlines()
    return len(lines[0]) - 2, {
        int(number): dna_to_int(dna)
        for line in puzzle_input.splitlines()
        for number, dna in [line.split(":")]
    }


def dna_to_int(dna: str) -> int:
    """Convert a DNA to an integer using base 4.

    ## Example:

    >>> dna_to_int("ACAG")  # 0203 ~> 3x1 + 0x4 + 2x16 + 0x64 = 35
    35

    Thanks to ... on Discord for the idea.
    """
    return int(
        dna.replace("A", "0").replace("T", "1").replace("C", "2").replace("G", "3"),
        base=4,
    )


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    num_chars, scales = parse(puzzle_input)
    child, mother, father = next(find_families(scales, num_chars))
    return similarities(child, mother, father, num_chars)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    num_chars, scales = parse(puzzle_input)
    return sum(
        similarities(*family, num_chars=num_chars)
        for family in find_families(scales, num_chars)
    )


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    num_chars, scales = parse(puzzle_input)
    ids = {dna: id for id, dna in scales.items()}

    # Use IDs in the graph because we need them for the final answer
    graph = defaultdict(set)
    for child, mother, father in find_families(scales, num_chars):
        graph[ids[child]] |= {ids[mother], ids[father]}
        graph[ids[mother]].add(ids[child])
        graph[ids[father]].add(ids[child])

    return sum(max(find_components(graph), key=len))


def find_families(
    scales: dict[int, int], num_chars: int
) -> Generator[tuple[int, int, int]]:
    """Find possible families within the given scales.

    With people represented as integers, we can use ^ and & to ensure that the
    differences don't overlap. Order candidates by similarity to investigate
    most likely DNAs first.
    """
    for child in scales.values():
        candidates = sorted(
            [
                (similarity(child, parent, num_chars=num_chars), parent)
                for parent in scales.values()
            ],
            reverse=True,
        )
        for (m, mother), (_, father) in itertools.combinations(candidates, 2):
            if child == mother:
                continue
            if m < num_chars // 2:
                break  # This child has no parents, early break
            if (child ^ mother) & (child ^ father) == 0:
                yield child, mother, father
                break


def similarity(first: int, second: int, num_chars: int) -> int:
    """Calculate the number of equal genes between two persons.

    ## Example:

        First:    CGTTGA ~> 231130 ~> 2908
        Second:   TACTGT ~> 102131 ~> 1181

    >>> similarity(2908, 1181, num_chars=6)
    2
    """
    both = first ^ second
    return sum((both >> shift) & 3 == 0 for shift in range(0, 2 * num_chars, 2))


def similarities(child: int, mother: int, father: int, num_chars: int) -> int:
    """Calculate the similarity score between a child and its parents.

    ## Example:

        Child:   ACAG ~> 0203 ~> 35
        Mother:  ATTG ~> 0113 ~> 23  Similarity 2
        Father:  ACAT ~> 0201 ~> 33  Similarity 3

    >>> similarities(35, 23, 33, num_chars=4)
    6
    """
    return similarity(child, mother, num_chars) * similarity(child, father, num_chars)


def find_components(graph: dict[int, set[int]]) -> Generator[set[int]]:
    """Find the components in the given graph."""
    nodes = set(graph)
    while nodes:
        component = set()
        queue = deque([nodes.pop()])
        while queue:
            node = queue.popleft()
            if node in component:
                continue
            component.add(node)
            queue.extend(graph[node])
        yield component
        nodes -= component
