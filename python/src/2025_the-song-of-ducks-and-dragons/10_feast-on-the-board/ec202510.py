"""Everybody Codes quest 10, 2025: Feast on the Board."""

import itertools
from typing import TypeAlias

Square: TypeAlias = tuple[int, int]
MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
STATES: dict[tuple[bool, Square, frozenset[Square]], int] = {}


def parse_board(
    puzzle_input: str,
) -> tuple[set[Square], Square, set[Square], set[Square]]:
    """Parse the game board. Find the dragon, all sheep, and all hideouts"""
    board = {
        (row, col): char
        for row, line in enumerate(puzzle_input.splitlines())
        for col, char in enumerate(line)
    }
    dragon = next(pos for pos, char in board.items() if char == "D")
    sheep = {pos for pos, char in board.items() if char == "S"}
    hideouts = {pos for pos, char in board.items() if char == "#"}
    return set(board), dragon, sheep, hideouts


def part1(puzzle_input: str, num_rounds=4) -> int:
    """Solve part 1."""
    board, dragon, sheep, _ = parse_board(puzzle_input)

    moves = {dragon}
    for _ in range(num_rounds):
        moves |= move_dragons(moves, board)

    return len(moves & sheep)


def part2(puzzle_input: str, num_rounds=20) -> int:
    """Solve part 2."""
    board, dragon, sheep, hideouts = parse_board(puzzle_input)
    dragons = {dragon}

    num_eaten = 0
    for _ in range(num_rounds):
        # Dragon move
        dragons = move_dragons(dragons, board)
        num_eaten += len(dragons & (sheep - hideouts))
        sheep -= dragons - hideouts

        # Sheep move
        sheep = move_sheep(sheep, board)
        num_eaten += len(dragons & (sheep - hideouts))
        sheep -= dragons - hideouts
    return num_eaten


def part3(puzzle_input: str) -> int:
    """Solve part 3."""
    board, dragon, sheep, hideouts = parse_board(puzzle_input)
    return play_game(dragon, sheep, hideouts, set(board))


def move_dragons(dragons: set[Square], board: set[Square]) -> set[Square]:
    """Move a set of dragons to all their possible new positions on the board."""
    return {
        (dr + mr, dc + mc) for (dr, dc), (mr, mc) in itertools.product(dragons, MOVES)
    } & board


def move_sheep(sheep: set[Square], board: set[Square]) -> set[Square]:
    """Move all sheep to their new positions on the board."""
    return {(r + 1, c) for r, c in sheep} & board


def play_game(
    dragon: Square, sheep: set[Square], hideouts: set[Square], board: set[Square]
) -> int:
    """Initialize a game of dragon chess."""
    _, max_col = max(board)

    # Clear the cache
    STATES.clear()

    # Sheep escape if they reach a line of hideouts at the bottom of their column
    escapes = [
        max(r + 1 for r, c in board - hideouts if c == col)
        for col in range(max_col + 1)
    ]
    return play(False, dragon, frozenset(sheep), (hideouts, escapes, board))


def play(
    dragon_turn: bool,
    dragon: Square,
    sheep: frozenset[Square],
    info: tuple[set[Square], list[int], set[Square]],
) -> int:
    """Play dragon chess and find number of unique games ending with victory."""
    # All sheeps are eaten: victory
    if not sheep:
        return 1

    # Seen state
    state = (dragon_turn, dragon, sheep)
    if state in STATES:
        return STATES[state]

    dr, dc = dragon
    hideouts, escapes, board = info
    count = 0

    # Dragon's turn, make all possible moves inside the board
    if dragon_turn:
        for mr, mc in MOVES:
            ndr, ndc = dr + mr, dc + mc
            if (ndr, ndc) not in board:
                continue
            count += play(False, (ndr, ndc), sheep - ({(ndr, ndc)} - hideouts), info)

    # Sheep's turn, move all sheep if possible
    else:
        did_move = False
        for sr, sc in sheep:
            nsr, nsc = sr + 1, sc

            # Sheep escapes, no victory
            if nsr >= escapes[nsc]:
                did_move = True
                continue

            # Don't move into dragon, unless hideout
            if (nsr, nsc) == dragon and dragon not in hideouts:
                continue

            # Regular move
            count += play(True, dragon, sheep - {(sr, sc)} | {(nsr, nsc)}, info)
            did_move = True
        if not did_move:
            # Skip the sheep's turn if the only sheep is blocked by the dragon
            count += play(True, dragon, sheep, info)

    STATES[state] = count
    return count
