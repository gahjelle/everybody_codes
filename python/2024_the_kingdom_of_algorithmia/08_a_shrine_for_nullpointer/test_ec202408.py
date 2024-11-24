"""Tests for Everybody Codes 8, 2024: A Shrine for Nullpointer."""

# Standard library imports
import pathlib

# Third party imports
import ec202408
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
    assert ec202408.part1(example1) == 21


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert ec202408.part2(example2, acolytes=5, available=50) == 27


def test_part3_example3(example3):
    """Test part 2 on example input."""
    assert ec202408.part3(example3, acolytes=5, available=160) == 2
