"""Everybody Codes, bonus 2024: A Message to the Knights

Bonus from Reddit:
https://www.reddit.com/r/everybodycodes/comments/1h2yc5e/2024_q21_message_to_the_knights/
"""

import sys
from pathlib import Path

# Path hacking to import Day 19
sys.path.append(str(next(Path(__file__).parent.parent.glob("19_*"))))
import ec202419  # pyright: ignore[reportMissingImports]


def parse(puzzle_input):
    num_rounds, _, message = puzzle_input.partition(":")
    return int(num_rounds), message


def solve(puzzle_input):
    """Display bonus message."""
    num_rounds, message = parse(puzzle_input)
    return ec202419.part(message, rounds=num_rounds, display_grid=True)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        puzzle_input = Path(path).read_text().rstrip()
        solve(puzzle_input)
