"""Everybody Codes quest 1, story 1: EniCode."""

from typing import NamedTuple


class Parameters(NamedTuple):
    A: int
    B: int
    C: int
    X: int
    Y: int
    Z: int
    M: int


def parse_data(puzzle_input: str) -> list[Parameters]:
    """Parse data into a list of parameters."""
    return [parse_line(line) for line in puzzle_input.split("\n")]


def parse_line(line: str) -> Parameters:
    """Parse one line of data."""
    return Parameters(
        **{
            key: int(value)
            for param in line.split(" ")
            for key, value in [param.split("=")]
        }
    )


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    params_list = parse_data(puzzle_input)
    return max(enicode(params) for params in params_list)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    params_list = parse_data(puzzle_input)
    return max(enicode(params, length=5) for params in params_list)


def part3(puzzle_input):
    """Solve part 3."""
    params_list = parse_data(puzzle_input)
    return max(sum_enicode(params) for params in params_list)


def eni(n: int, exp: int, mod: int, length: int = 0) -> int:
    """Calculate the eni function.

    - Start with 1 as the initial score, and prepare an empty list to store
      remainders.
    - Multiply the score by the number N.
    - Take the remainder after dividing the score by MOD.
    - Add this number to the start of the list of remainders.
    - Repeat the multiplication, remainder, and appending steps EXP times.
    - The final result is effectively a number formed by joining the remainders
      list as a single number.

    ## Examples:

    >>> eni(2, 4, 5)
    1342

    >>> eni(3, 5, 16)
    311193

    >>> eni(2, 7, 5, length=5)
    34213
    """
    length = exp if length == 0 else length
    score = 1

    # Fast track
    for bit in format(max(0, exp - length), "b"):
        score = (score * score) % mod
        if bit == "1":
            score = (score * n) % mod

    remainders: list[int] = []
    for _ in range(length):
        score = (score * n) % mod
        remainders.insert(0, score)

    return int("".join(str(r) for r in remainders))


def enicode(params: Parameters, length: int = 0) -> int:
    """Calculate the enicode by adding three eni calls."""
    return (
        eni(params.A, params.X, params.M, length=length)
        + eni(params.B, params.Y, params.M, length=length)
        + eni(params.C, params.Z, params.M, length=length)
    )


def sum_eni(n: int, exp: int, mod: int) -> int:
    """Calculate the sum of all remainders.

    ## Examples:

    >>> sum_eni(2, 7, 5)
    19

    >>> sum_eni(3, 8, 16)
    48

    >>> sum_eni(4, 3000, 110)
    132000
    """
    seen: dict[int, int] = {}
    remainders: list[int] = [0]
    score = 1

    for idx in range(exp):
        score = (score * n) % mod
        if score in seen:
            cycle_idx = seen[score]
            cycle_len = idx - cycle_idx
            cycle = [r - remainders[cycle_idx] for r in remainders[cycle_idx:]]
            mul = (exp - idx) // cycle_len
            rem = (exp - idx) - mul * cycle_len
            remainders.append(remainders[-1] + mul * cycle[-1] + cycle[rem])
            break
        seen[score] = idx
        remainders.append(score + remainders[-1])
    return remainders[-1]


def sum_enicode(params: Parameters) -> int:
    """Calculate the enicode by adding three eni calls."""
    return (
        sum_eni(params.A, params.X, params.M)
        + sum_eni(params.B, params.Y, params.M)
        + sum_eni(params.C, params.Z, params.M)
    )
