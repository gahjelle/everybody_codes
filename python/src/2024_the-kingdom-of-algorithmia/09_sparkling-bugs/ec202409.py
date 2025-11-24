"""Everybody Codes 9, 2024: Sparkling Bugs"""


def parse_input(puzzle_input: str) -> list[int]:
    """Read the desired brightnesses."""
    return [int(line) for line in puzzle_input.split("\n")]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    balls = parse_input(puzzle_input)
    cache = prepare_cache({1, 3, 5, 10}, max(balls) + 1)
    return sum(cache[ball] for ball in balls)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    balls = parse_input(puzzle_input)
    cache = prepare_cache({1, 3, 5, 10, 15, 16, 20, 24, 25, 30}, max(balls) + 1)
    return sum(cache[ball] for ball in balls)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    balls = parse_input(puzzle_input)
    cache = prepare_cache(
        {1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101},
        (max(balls) + 100) // 2 + 1,
    )
    return sum(num_beetle_pairs(ball, cache, limit=100) for ball in balls)


def prepare_cache(stamps: set[int], max_brightness: int) -> dict[int, int]:
    """Precalculate all needed brightness calculations"""
    infty = 2 * max_brightness
    cache = {brightness: infty for brightness in range(max_brightness)} | {0: 0}

    for stamp in stamps:
        for brightness in range(stamp, max_brightness):
            cache[brightness] = min(cache[brightness], cache[brightness - stamp] + 1)

    return cache


def num_beetle_pairs(target: int, cache: dict[int, int], limit: int = 100) -> int:
    """Find the optimal pair of beetles to achieve the desired brightness."""
    min_brightness = (target - limit) // 2
    max_brightness = target - min_brightness

    # Find best pair
    return min(
        cache[brightness] + cache[target - brightness]
        for brightness in range(min_brightness, max_brightness)
        if abs(2 * brightness - target) <= limit
    )
