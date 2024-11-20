"""Everybody Codes 12, 2024: Desert Shower"""

# Standard library imports
import string
import sys
from pathlib import Path

VALUES = {"A": 1, "B": 2, "C": 3, "T": 1, "H": 2}


def parse_catapults(puzzle_input):
    """Parse the catapult map."""
    coords = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n")[::-1])
        for col, char in enumerate(line)
        if char in string.ascii_letters
    }
    targets = {char for char in coords.values() if char not in "ABC"}
    return (
        {VALUES[char]: coord for coord, char in coords.items() if char in "ABC"},
        {
            VALUES[target]: [coord for coord, char in coords.items() if char == target]
            for target in targets
        },
    )


def parse_meteors(puzzle_input):
    """Parse meteor list."""
    return [
        tuple(int(coord) for coord in line.split())[::-1]
        for line in puzzle_input.split("\n")
    ]


def part1(puzzle_input):
    """Solve part 1."""
    catapults, targets = parse_catapults(puzzle_input)
    return sum(
        shoot(catapults, target) * score
        for score, coords in targets.items()
        for target in coords
    )


def part2(puzzle_input):
    """Solve part 2."""
    return part1(puzzle_input)


def part3(puzzle_input):
    """Solve part 3."""
    meteors = parse_meteors(puzzle_input)
    return sum(
        shoot_meteor({catapult + 1: (catapult, 0) for catapult in range(3)}, meteor)
        for meteor in meteors
    )


def shoot(catapults, target):
    """Shoot a catapult at the target.

    Take into account that the hit can happen in any of the three phases of the
    flight.
    """
    t_row, t_col = target
    return min(
        power * catapult
        for catapult, (row, col) in catapults.items()
        for fire in [shoot_up, shoot_flat, shoot_down]
        if (power := fire(row, col, t_row, t_col)) > 0
    )


def shoot_meteor(catapults, target):
    """Shoot catapults at moving meteors.

    Calculate where the meteor will be at time of impact and treat it as a fixed
    target. Time is when the shot is fired. The earlier a shot is fired, the
    higher it will hit, so we want to fire as early as possible.
    """
    t_row, t_col = target
    for time in range(t_col % 2, t_row, 2):
        flight_time = (t_col - time) // 2
        if score := shoot(
            catapults, (t_row - time - flight_time, t_col - time - flight_time)
        ):
            return score
    return 0


def shoot_up(row, col, t_row, t_col):
    """Hit the target in the beginning of the projectile's flight"""
    power = t_row - row
    return power if t_row - t_col == row - col else 0


def shoot_flat(row, col, t_row, t_col):
    """Hit the target in the middle of the projectile's flight"""
    power = t_row - row
    horizontal_displacement = (t_col - t_row) - (col - row)
    return power if 0 < horizontal_displacement <= power else 0


def shoot_down(row, col, t_row, t_col):
    """Hit the target as the projectile is falling down at end of flight"""
    total_flight = (t_col - col) + (t_row - row)
    power = total_flight // 3
    return power if total_flight % 3 == 0 and t_col - col >= 2 * power else 0


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
