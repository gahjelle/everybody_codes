"""Everybody Codes 15, 2024: From the Herbalist's Diary"""

# Standard library imports
import heapq
import sys
from pathlib import Path
from string import ascii_letters as letters


def parse_grid(puzzle_input):
    """Parse input."""
    return {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char not in "#~"
    }


def part1(puzzle_input):
    """Solve part 1."""
    grid = parse_grid(puzzle_input)
    start = min(grid)
    return explore(grid, start)


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3."""
    return part1(puzzle_input)


def explore(grid, start):
    """Explore the grid while collecting herbs"""
    targets = {target for target in set(grid.values()) if target in letters}
    queue = [(0, start, ())]
    seen = {}
    max_herbs = 0
    while queue:
        num_steps, pos, herbs = heapq.heappop(queue)
        if (pos, herbs) in seen:
            continue
        if pos == start and set(herbs) == targets:
            return num_steps

        # Prune tree
        if len(herbs) > max_herbs:
            max_herbs = len(herbs)
            if max_herbs > 2:
                queue = [
                    (num_steps, pos, herbs)
                    for (num_steps, pos, herbs) in queue
                    if len(herbs) >= max_herbs - 2
                ]
                heapq.heapify(queue)

        seen[pos, herbs] = num_steps
        for drow, dcol in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            new_pos = (pos[0] + drow, pos[1] + dcol)
            if new_pos in grid:
                new_herbs = (
                    tuple(sorted(herbs + (grid[pos],)))
                    if grid[pos] in targets and grid[pos] not in herbs
                    else herbs
                )
                if (
                    num_steps + 1 < seen.get((new_pos, new_herbs), 9_999)
                    and len(herbs) >= max_herbs - 2
                ):
                    heapq.heappush(queue, (num_steps + 1, new_pos, new_herbs))
    return 9_999


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{', '.join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
