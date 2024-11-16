"""Everybody Codes 10, 2024: Shrine Needs to Shine"""

# Standard library imports
import collections
import itertools
import sys
from pathlib import Path

MAX_DEDUCE_COUNT = 2


def part1(puzzle_input):
    """Solve part 1."""
    grid = parse_grid(puzzle_input)

    text = []
    for row, col in itertools.product(range(2, 6), range(2, 6)):
        horizontal = get_letters(grid, [row], range(8))
        vertical = get_letters(grid, range(8), [col])
        text.append((horizontal & vertical).pop())

    return "".join(text)


def part2(puzzle_input):
    """Solve part 2."""
    inputs = split_input(puzzle_input, num_rows=7, num_cols=15, drow=9, dcol=9)
    return sum(calculate_power(part1(input)) for input in inputs)


def part3(puzzle_input):
    """Solve part 3."""
    grid = parse_grid(puzzle_input)
    runes = fill_grid(grid)

    total_power = 0
    max_row, max_col = max(grid.keys())
    num_rows, num_cols = (max_row + 1) // 6, (max_col + 1) // 6
    for brow, bcol in itertools.product(range(num_rows), range(num_cols)):
        word = "".join(
            runes[brow * 6 + row, bcol * 6 + col]
            for row, col in itertools.product(range(2, 6), range(2, 6))
        )
        if "." not in word and "?" not in word:
            total_power += calculate_power(word)

    return total_power


def parse_grid(puzzle_input):
    """Parse the puzzle input."""
    return {
        (row, col): letter
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, letter in enumerate(line.strip())
        if letter != "*"
    }


def split_input(puzzle_input, num_rows, num_cols, drow, dcol):
    lines = puzzle_input.split("\n")

    for row in range(num_rows):
        for col in range(num_cols):
            block = "\n".join(
                line[col * dcol : col * dcol + 8]
                for line in lines[row * drow : row * drow + 8]
            )
            if block.strip():
                yield block


def get_letters(grid, rows, cols):
    """Get a set of letters from the grid."""
    return {
        letter
        for row, col in itertools.product(rows, cols)
        if (letter := grid[row, col]) != "."
    }


def get_coords(grid, rows, cols, symbol):
    """Get the coordinates of the given symbol."""
    return [
        (row, col)
        for row, col in itertools.product(rows, cols)
        if grid[row, col] == symbol
    ]


def fill_grid(grid):
    """Fill in grid with letters. This should be cleaned up :)"""
    runes = {coords: letter for coords, letter in grid.items() if letter == "."}
    queue = collections.deque((row, col, 0) for row, col in runes.keys())
    while queue:
        row, col, count = queue.popleft()
        brow, bcol = row // 6, col // 6
        horizontal = get_letters(grid, [row], range(bcol * 6, bcol * 6 + 8))
        vertical = get_letters(grid, range(brow * 6, brow * 6 + 8), [col])
        overlap = horizontal & vertical
        if len(overlap) == 1:
            letter = overlap.pop()
            runes[row, col] = letter
            grid[row, col] = letter
        elif "?" in horizontal:
            solved = get_letters(runes, range(brow * 6 + 2, brow * 6 + 6), [col])
            options = vertical - solved
            if len(options) == 1:
                runes[row, col] = options.pop()
                qcols = get_coords(grid, [row], range(bcol * 6, bcol * 6 + 8), "?")
                if len(qcols) == 1:
                    _, qcol = qcols[0]
                    grid[row, qcol] = runes[row, col]
            elif count < MAX_DEDUCE_COUNT:
                queue.append((row, col, count + 1))
        elif "?" in vertical:
            solved = get_letters(runes, [row], range(bcol * 6 + 2, bcol * 6 + 6))
            options = horizontal - solved
            if len(options) == 1:
                runes[row, col] = options.pop()
                qrows = get_coords(grid, range(brow * 6, brow * 6 + 8), [col], "?")
                if len(qrows) == 1:
                    qrow, _ = qrows[0]
                    grid[qrow, col] = runes[row, col]
            elif count < MAX_DEDUCE_COUNT:
                queue.append((row, col, count + 1))
    return runes


def calculate_power(word):
    return sum(idx * (ord(char) - 64) for idx, char in enumerate(word, start=1))


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
