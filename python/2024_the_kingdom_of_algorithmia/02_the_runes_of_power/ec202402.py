"""Everybody Codes 2, 2024: The Runes of Power"""

# Standard library imports
import sys
from pathlib import Path


def parse_data(puzzle_input):
    """Parse input."""
    words, text = puzzle_input.split("\n\n", maxsplit=1)
    return words.removeprefix("WORDS:").split(","), text


def part1(puzzle_input):
    """Solve part 1."""
    words, text = parse_data(puzzle_input)

    return sum(text.count(word) for word in words)


def part2(puzzle_input):
    """Solve part 2."""
    words, text = parse_data(puzzle_input)

    ids = range(len(text))
    return len(
        find_runic_symbols(words, text, ids)
        | find_runic_symbols(words, text[::-1], ids[::-1])
    )


def part3(puzzle_input):
    """Solve part 3."""
    words, text = parse_data(puzzle_input)

    lines = text.split("\n")
    chars = text.replace("\n", "")
    line_len = len(chars) // len(lines)

    ids = range(len(chars))
    return len(
        find_runic_symbols(words, *wrap(chars, ids, line_len))
        | find_runic_symbols(words, *wrap(chars[::-1], ids[::-1], line_len))
        | find_runic_symbols(words, *flip(chars, ids, line_len))
        | find_runic_symbols(words, *flip(chars[::-1], ids[::-1], line_len))
    )


def find_runic_symbols(words, text, ids):
    """Find the IDs of runic symbols in the text."""
    runic = set()
    for word in words:
        start_idx = 0
        while True:
            try:
                idx = text.index(word, start_idx)
            except ValueError:
                break
            else:
                start_idx = idx + 1
                runic |= set(ids[i] for i in range(idx, idx + len(word)))
    return runic


def wrap(text, ids, line_len):
    """Wrap lines of text and their corresponding IDs."""
    lines = [text[idx : idx + line_len] for idx in range(0, len(text), line_len)]
    line_ids = [
        list(ids[idx : idx + line_len]) for idx in range(0, len(text), line_len)
    ]
    return (
        "\n".join(line * 2 for line in lines),
        [id for line in [list(line) * 2 + [-1] for line in line_ids] for id in line],
    )


def flip(text, ids, line_len):
    """Flip lines of text and their corresponding IDs 90 degrees."""
    return (
        "\n".join(text[idx::line_len] for idx in range(line_len)),
        [
            id
            for line in [list(ids[idx::line_len]) + [-1] for idx in range(line_len)]
            for id in line
        ],
    )


if __name__ == "__main__":
    for paths in zip(sys.argv[1::3], sys.argv[2::3], sys.argv[3::3]):
        puzzle_inputs = [Path(path).read_text().rstrip() for path in paths]
        print(f"\n{", ".join(paths)}:")
        solutions = [
            part(puzzle_input)
            for part, puzzle_input in zip([part1, part2, part3], puzzle_inputs)
        ]
        print("\n".join(str(solution) for solution in solutions))
