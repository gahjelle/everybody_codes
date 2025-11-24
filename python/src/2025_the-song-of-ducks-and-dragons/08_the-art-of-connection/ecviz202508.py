"""Everybody Codes quest 8, 2025: The Art of Connection."""

import math
from pathlib import Path

from PIL import Image, ImageDraw

CX, CY = 800, 800
RADIUS = 760
EC_YELLOW = (238, 214, 153)


def parse(puzzle_input: str) -> tuple[int, list[tuple[int, int]]]:
    """Parse the input into number of nails and a list of threads."""
    nails = [int(number) for number in puzzle_input.split(",")]
    return (max(nails), list(zip(nails[:-1], nails[1:], strict=True)))


def part2(puzzle_input: str, out_path: Path) -> None:
    """Visualize part 2."""
    draw_stringart(puzzle_input, out_path)


def part3(puzzle_input: str, out_path: Path) -> None:
    """Visualize part 3."""
    draw_stringart(puzzle_input, out_path)


def draw_stringart(puzzle_input: str, out_path: Path) -> None:
    image = Image.new("RGB", size=(CX * 2, CY * 2), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.circle((CX, CY), RADIUS, fill=EC_YELLOW)

    num_nails, strings = parse(puzzle_input)
    for start, end in strings:
        x1, y1 = to_coords(start, num_nails)
        x2, y2 = to_coords(end, num_nails)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=1)
    image.save(out_path)


def to_coords(nail: int, num_nails: int) -> tuple[int, int]:
    """Find coordinates of a single nail."""
    arc = (num_nails - nail) / num_nails * 2 * math.pi
    return CX + int(RADIUS * math.sin(arc)), CY - int(RADIUS * math.cos(arc))
