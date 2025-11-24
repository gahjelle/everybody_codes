"""Everybody Codes quest 5, 2025: Fishbone Order."""

from dataclasses import dataclass
from typing import Self


@dataclass
class SwordSegment:
    """Construct a sword as a linked list of segments."""

    middle: int
    left: int | None = None
    right: int | None = None
    next_segment: Self | None = None

    @classmethod
    def from_numbers(cls, numbers: list[int]) -> Self:
        """Create sword segments from the given numbers."""
        head, *tail = numbers
        segments = cls(head)
        for number in tail:
            segments.add(number)
        return segments

    def add(self, number: int) -> None:
        """Add a number to the sword.

        - Check all segments of the spine, starting from the top.
        - If your number is less than the one on the spine segment and the left
          side of the segment is free - place it on the left.
        - If your number is greater than the one on the spine segment and the
          right side of the segment is free - place it on the right.
        - If no suitable place is found at any segment, create a new spine
          segment from your number and place it as the last one.
        """
        cls = type(self)

        if self.left is None and number < self.middle:
            self.left = number
        elif self.right is None and number > self.middle:
            self.right = number
        elif self.next_segment is None:
            self.next_segment = cls(number)
        else:
            self.next_segment.add(number)

    def spine(self) -> int:
        """Collect the spine of the sword as a string of numbers."""
        return int(
            str(self.middle)
            + ("" if self.next_segment is None else str(self.next_segment.spine()))
        )

    def as_number(self) -> list[int]:
        """Represent the segments as numbers."""
        return [
            int(
                ("" if self.left is None else str(self.left))
                + str(self.middle)
                + ("" if self.right is None else str(self.right))
            ),
            *([] if self.next_segment is None else self.next_segment.as_number()),
        ]

    def score(self, sword_id: int) -> list[int]:
        """Calculate a score for the sword."""
        return [int(self.spine()), *self.as_number(), sword_id]


def parse_swords(puzzle_input: str) -> dict[int, list[int]]:
    """Parse information about several swords."""
    return dict([parse_sword(line) for line in puzzle_input.splitlines()])


def parse_sword(puzzle_input: str) -> tuple[int, list[int]]:
    """Parse information about a sword."""
    sword_id, _, numbers = puzzle_input.partition(":")
    return int(sword_id), [int(number) for number in numbers.split(",")]


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    _, numbers = parse_sword(puzzle_input)
    return SwordSegment.from_numbers(numbers).spine()


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    swords = parse_swords(puzzle_input)
    qualities = [
        SwordSegment.from_numbers(numbers).spine() for numbers in swords.values()
    ]
    return max(qualities) - min(qualities)


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    swords = parse_swords(puzzle_input)
    qualities = {
        sword_id: SwordSegment.from_numbers(numbers)
        for sword_id, numbers in swords.items()
    }
    scores = sorted(
        [sword.score(sword_id) for sword_id, sword in qualities.items()], reverse=True
    )
    return sum(idx * score[-1] for idx, score in enumerate(scores, start=1))
