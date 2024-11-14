#!/usr/bin/env python
"""Test outputs of Everybody Codes puzzle solutions."""

# Standard library imports
import importlib
import pathlib

# Third party imports
import pytest
from codetiming import Timer

PUZZLE_DIR = pathlib.Path(__file__).parent
PUZZLE_PATHS = sorted(p.parent for p in PUZZLE_DIR.rglob("**/output.py.txt"))


class TimingsLog:
    """Logger that can write timings to file."""

    time_units = (
        ("m ⚫️", 60),
        ("s 🔴", 1),
        ("ms 🔵", 1e-3),
        ("μs ⚪️", 1e-6),
        ("ns ⚪️", 1e-9),
    )
    fmt_header = (
        "\n## {year}\n\n"
        "| Day | Puzzle | Python | Part 1 | Part 2 | Part 3 | Total |\n"
        "|:---|:---|:---|---:|---:|---:|---:|\n"
    )
    fmt_entry = (
        "| {day} | {puzzle} | {link} | {part1} | {part2} | {part3} | {total} |\n"
    )

    def __init__(self, path):
        """Initialize logger."""
        self.path = path
        self.path.write_text("# Everybody Codes\n")
        self.current_year = 0

    def write_log(self, year, day, puzzle, link, part1, part2, part3):
        """Write an entry in the log."""
        if year != self.current_year:
            self.current_year = year
            self.write_line(self.fmt_header.format(year=year))

        self.write_line(
            self.fmt_entry.format(
                day=day,
                puzzle=puzzle,
                link=link,
                part1=self.prettytime(part1),
                part2=self.prettytime(part2),
                part3=self.prettytime(part3),
                total=self.prettytime(part1 + part2 + part3),
            )
        )

    def write_line(self, line):
        """Write one line to the log file."""
        with self.path.open(mode="a") as fid:
            fid.write(line)

    @classmethod
    def prettytime(cls, seconds):
        """Pretty-print number of seconds."""
        for unit, threshold in cls.time_units:
            if seconds > threshold:
                return f"{seconds / threshold:.2f} {unit}"


TIMINGS_LOG = TimingsLog(PUZZLE_DIR / "timings.py.md")


@pytest.mark.parametrize(
    "puzzle_path", PUZZLE_PATHS, ids=[p.name for p in PUZZLE_PATHS]
)
def test_puzzle(puzzle_path):
    """Test one puzzle against the expected solution."""

    # Import puzzle
    *_, year_dir, puzzle = puzzle_path.parts
    day = puzzle[:2]
    year, *_ = year_dir.split("_")
    puzzle_mod = importlib.import_module(f"{year_dir}.{puzzle}.ec{year}{day}")

    # Solve each part
    timers, solutions = [], []
    for part in [1, 2, 3]:
        puzzle_input = (
            (puzzle_path / f"everybody_codes_e{year}_q{day}_p{part}.txt")
            .read_text()
            .rstrip()
        )
        puzzle_part = getattr(puzzle_mod, f"part{part}")
        with Timer(logger=None) as timer:
            puzzle_data = puzzle_part(puzzle_input)
        timers.append(timer.last)
        solutions.append(str(puzzle_data))

    # Compare to expected output
    expected = (puzzle_path / "output.py.txt").read_text().rstrip().split("\n")[-3:]
    assert solutions == expected

    # Log elapsed time
    puzzle_name = puzzle[3:].replace("_", " ").title()
    link = f"[ec{year}{day}.py]({puzzle}/ec{year}{day}.py)"
    TIMINGS_LOG.write_log(
        year=year,
        day=int(day),
        puzzle=puzzle_name,
        link=link,
        part1=timers[0],
        part2=timers[1],
        part3=timers[2],
    )
