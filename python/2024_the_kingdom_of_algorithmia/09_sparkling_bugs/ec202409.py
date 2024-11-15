"""Everybody Codes 9, 2024: Sparkling Bugs"""

# Standard library imports
import heapq
import sys
from pathlib import Path


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    return solve(puzzle_input, {1, 3, 5, 10}, num_beetles)


def part2(puzzle_input):
    """Solve part 2."""
    return solve(puzzle_input, {1, 3, 5, 10, 15, 16, 20, 24, 25, 30}, num_beetles)


def part3(puzzle_input):
    """Solve part 3."""
    return solve(
        puzzle_input,
        {1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101},
        num_beetle_pairs,
    )


def solve(puzzle_input, stamps, count_beetles):
    """Solve one part of the challenge with the specified way of counting beetles."""
    balls = parse_input(puzzle_input)
    cache = {stamp: 1 for stamp in stamps}

    return sum(count_beetles(ball, stamps, cache) for ball in balls)


def parse_input(puzzle_input: str) -> list[int]:
    """Read the desired brightnesses."""
    return [int(line) for line in puzzle_input.split("\n")]


def num_beetles(target: int, stamps: list[int], cache: dict[int, int]) -> int:
    """Count the minimum number of beetles needed to achive the desired brightness."""
    if target in cache:
        return cache[target]

    queue = [(num_beetles, brightness) for brightness, num_beetles in cache.items()]
    heapq.heapify(queue)

    seen = set()
    while True:
        num_beetles, brightness = heapq.heappop(queue)
        if brightness in seen:
            continue
        seen.add(brightness)
        if brightness not in cache:
            cache[brightness] = num_beetles
        if brightness == target:
            return num_beetles
        for stamp in stamps:
            if brightness + stamp not in cache:
                heapq.heappush(queue, (num_beetles + 1, brightness + stamp))


def num_beetle_pairs(target: int, stamps: list[int], cache: dict[int, int]) -> int:
    """Find the optimal pair of beetles to achieve the desired brightness."""
    min_brightness = target // 2 - 50
    max_brightness = target - min_brightness

    # Populate cache
    for brightness in range(max_brightness + 1, min_brightness - 1, -1):
        num_beetles(brightness, stamps, cache)

    # Find best pair
    return min(
        cache[brightness] + cache[target - brightness]
        for brightness in range(min_brightness, max_brightness)
        if abs(2 * brightness - target) <= 100
    )


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
