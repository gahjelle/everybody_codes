"""Everybody Codes quest 1, 2025: Whispers in the Shell."""


def parse(puzzle_input: str) -> tuple[list[str], list[int]]:
    """Parse the input into a list of names and a list of moves."""
    names, _, moves = puzzle_input.partition("\n\n")
    return names.split(","), [parse_move(move) for move in moves.split(",")]


def parse_move(move: str) -> int:
    """Parse a move into a number.

    L moves left and is represented by negative numbers. R moves right and is
    represented by positive numbers.

    ## Examples:

    >>> parse_move("R1")
    1
    >>> parse_move("R25")
    25
    >>> parse_move("L3")
    -3
    >>> parse_move("L281")
    -281
    """
    return int(move.replace("L", "-").replace("R", ""))


def part1(puzzle_input: str) -> str:
    """Solve part 1."""
    names, moves = parse(puzzle_input)
    size = len(names)

    pos = 0
    for steps in moves:
        pos = min(max(pos + steps, 0), size - 1)

    return names[pos]


def part2(puzzle_input: str) -> str:
    """Solve part 2."""
    names, moves = parse(puzzle_input)
    size = len(names)

    final_pos = sum(moves) % size
    return names[final_pos]


def part3(puzzle_input: str) -> str:
    """Solve part 3."""
    names, moves = parse(puzzle_input)
    size = len(names)

    for idx in moves:
        names[0], names[idx % size] = names[idx % size], names[0]

    return names[0]
