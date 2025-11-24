"""Everybody Codes 7, 2024: Not Fast but Furious"""

import collections
import itertools
import math
from collections.abc import Generator

SYMBOLS = {"-": -1, "=": 0, "+": 1, "S": 0}

TRACK_PT1 = "S=========SS"

TRACK_PT2 = """
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-
"""

TRACK_PT3 = """
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-
"""


def parse_plan(puzzle_input: str) -> dict[str, list[int]]:
    """Parse input data."""
    return {
        line[0]: [SYMBOLS[symbol] for symbol in line[2:].split(",")]
        for line in puzzle_input.split("\n")
    }


def parse_track(track: str) -> list[int]:
    """Parse a racetrack into segments."""
    grid = {
        (row, col): char
        for row, line in enumerate(track.strip().split("\n"))
        for col, char in enumerate(line)
        if char != " "
    }
    (prev_row, prev_col), (row, col) = (0, 0), (0, 1)

    segments = []
    while not segments or grid[prev_row, prev_col] != "S":
        segments.append(SYMBOLS[grid[row, col]])
        for drow, dcol in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if (row + drow, col + dcol) != (prev_row, prev_col) and grid.get(
                (row + drow, col + dcol)
            ) in SYMBOLS:
                prev_row, prev_col = row, col
                row, col = row + drow, col + dcol
                break
    return segments


def part1(puzzle_input: str, track_string: str = TRACK_PT1, num_rounds: int = 1) -> str:
    """Solve part 1."""
    track = parse_track(track_string)
    plans = parse_plan(puzzle_input)
    essence = {
        player: calculate_essence(plan, track, num_rounds=num_rounds)
        for player, plan in plans.items()
    }
    return "".join(sorted(essence, key=lambda player: essence[player], reverse=True))


def part2(
    puzzle_input: str, track_string: str = TRACK_PT2, num_rounds: int = 10
) -> str:
    """Solve part 2."""
    return part1(puzzle_input, track_string, num_rounds)


def part3(
    puzzle_input: str, track_string: str = TRACK_PT3, num_rounds: int = 2024
) -> int:
    """Solve part 3.

    Take advantage of not needing to calculate all rounds, since the races will
    repeat at some point.
    """
    track = parse_track(track_string)
    opponent_plan = parse_plan(puzzle_input)["A"]
    necessary_rounds = math.gcd(num_rounds, len(opponent_plan))
    opponent_essence = calculate_essence(opponent_plan, track, necessary_rounds)

    num_actions = collections.Counter(opponent_plan)
    return sum(
        calculate_essence(plan, track, necessary_rounds) > opponent_essence
        for plan in create_plans(num_actions[1], num_actions[0], num_actions[-1])
    )


def create_plans(num_plus: int, num_equal: int, num_minus: int) -> Generator[list[int]]:
    """Create all possible plans with the given number of actions."""
    num_actions = num_plus + num_equal + num_minus
    for idx_plus in itertools.combinations(range(num_actions), num_plus):
        actions = set(range(num_actions)) - set(idx_plus)
        for idx_equal in itertools.combinations(actions, num_equal):
            yield [
                1 if idx in idx_plus else 0 if idx in idx_equal else -1
                for idx in range(num_actions)
            ]


def calculate_essence(plan: list[int], track: list[int], num_rounds: int) -> int:
    """Calculate the total essence gatherered in one race."""
    full_plan, track_segments = zip(*zip(itertools.cycle(plan), track * num_rounds))
    rounds = [
        segment if segment != 0 else plan
        for plan, segment in zip(full_plan, track_segments)
    ]
    return sum(itertools.accumulate(rounds, initial=10))
