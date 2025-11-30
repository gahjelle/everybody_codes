"""Everybody Codes, bonus 2025: Thank You, Dragonducks

Bonus from Reddit:
https://www.reddit.com/r/everybodycodes/comments/1p98ubm/2025_thank_you_dragonducks/
"""

import sys
from pathlib import Path


def parse(puzzle_input):
    return {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
        if char != "."
    }


def rotate(grid, size):
    """Rotate the grid 120 degrees."""
    return {
        (nrow := (col - row) // 2, size + nrow - (row + col)): char
        for (row, col), char in grid.items()
    }


def display(grid):
    """Display the message in the grid."""
    prev_row, prev_col = 0, -1
    for (row, col), char in sorted(grid.items()):
        if row > prev_row:
            print("\n" * (row - prev_row), end="")
            prev_col = -1
        if col > prev_col + 1:
            print(" " * (col - prev_col - 1), end="")
        prev_row, prev_col = row, col
        print(char, end="")
    print()


def solve(puzzle_input):
    """Display bonus message."""
    grid = parse(puzzle_input)
    size = max(c for _, c in grid)
    display(rotate(rotate(grid, size), size))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        puzzle_input = Path(path).read_text().rstrip()
        solve(puzzle_input)
