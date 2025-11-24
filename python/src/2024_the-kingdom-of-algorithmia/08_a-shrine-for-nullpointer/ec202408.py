"""Everybody Codes 8, 2024: A Shrine for Nullpointer"""


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    available = int(puzzle_input)
    num_blocks, base = 1, 1
    while num_blocks < available:
        base += 2
        num_blocks += base
    return (num_blocks - available) * base


def part2(puzzle_input: str, acolytes: int = 1_111, available: int = 20_240_000) -> int:
    """Solve part 2."""
    num_priests = int(puzzle_input)
    num_blocks, base, thickness = 1, 1, 1
    while num_blocks < available:
        thickness = (thickness * num_priests) % acolytes
        base += 2
        num_blocks += base * thickness
    return (num_blocks - available) * base


def part3(puzzle_input: str, acolytes: int = 10, available: int = 202_400_000) -> int:
    """Solve part 3."""
    num_priests = int(puzzle_input)
    num_blocks, base, thickness = 1, 1, 1
    columns = [1]
    while True:
        thickness = (thickness * num_priests) % acolytes + acolytes
        columns = [current + thickness for current in columns] + [thickness]
        base += 2
        num_blocks += base * thickness

        # Skip unnecessary calculation of blocks to remove
        if num_blocks < available:
            continue

        # Count number of blocks to remove
        remove = [(num_priests * base * current) % acolytes for current in columns[:-1]]
        num_remove = remove[0] + sum(remove[1:]) * 2
        if num_blocks - num_remove >= available:
            return num_blocks - num_remove - available
