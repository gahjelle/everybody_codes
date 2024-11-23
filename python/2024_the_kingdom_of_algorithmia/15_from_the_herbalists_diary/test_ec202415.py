"""Tests for Everybody Codes 15, 2024: From the Herbalist's Diary."""

# Standard library imports
import pathlib

# Third party imports
import ec202415
import pytest

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    return (PUZZLE_DIR / "example_p1.txt").read_text().rstrip()


@pytest.fixture
def example2():
    return (PUZZLE_DIR / "example_p2.txt").read_text().rstrip()


@pytest.fixture
def example3():
    return (PUZZLE_DIR / "example_p3.txt").read_text().rstrip()


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert ec202415.part1(example1) == 26


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert ec202415.part2(example2) == 38


def test_part3_example3(example3):
    """Test part 2 on example input."""
    assert ec202415.part3(example3) == 126
