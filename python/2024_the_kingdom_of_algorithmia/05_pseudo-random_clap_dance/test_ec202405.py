"""Tests for Everybody Codes 5, 2024: Pseudo-Random Clap Dance."""

# Standard library imports
import pathlib

# Third party imports
import ec202405
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
    assert ec202405.part1(example1) == 2323


def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert ec202405.part2(example2) == 50_877_075


def test_part3_example3(example3):
    """Test part 2 on example input."""
    assert ec202405.part3(example3) == 6584
