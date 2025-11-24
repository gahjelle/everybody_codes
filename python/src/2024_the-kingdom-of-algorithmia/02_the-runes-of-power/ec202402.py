"""Everybody Codes quest 2, 2024: The Runes of Power."""

from typing import Sequence


def parse_data(puzzle_input: str) -> tuple[list[str], str]:
    """Parse input."""
    words, text = puzzle_input.split("\n\n", maxsplit=1)
    return words.removeprefix("WORDS:").split(","), text


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    words, text = parse_data(puzzle_input)

    return sum(text.count(word) for word in words)


def part2(puzzle_input: str) -> int:
    """Solve part 2."""
    words, text = parse_data(puzzle_input)

    ids = range(len(text))
    return len(
        find_runic_symbols(words, text, ids)
        | find_runic_symbols(words, text[::-1], ids[::-1])
    )


def part3(puzzle_input: str) -> int:
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


def find_runic_symbols(words: list[str], text: str, ids: Sequence[int]) -> set[int]:
    """Find the IDs of runic symbols in the text.

    ## Example

    >>> words = ["THE", "OWE", "ROD"]
    >>> text = "THE POWER OF THE SEHTI"
    >>> ids = find_runic_symbols(words, text, range(len(text)))
    >>> sorted(ids)
    [0, 1, 2, 5, 6, 7, 13, 14, 15]
    """
    runic: set[int] = set()
    for word in words:
        start_idx = 0
        while True:
            try:
                idx = text.index(word, start_idx)
            except ValueError:
                break
            else:
                start_idx = idx + 1
                runic |= {ids[i] for i in range(idx, idx + len(word))}
    return runic


def wrap(text, ids, line_len):
    """Wrap lines of text and their corresponding IDs.

    HELWORLT      HELWORLTHELWORLT
    ENIGWDXL  ->  ENIGWDXLENIGWDXL
    TRODEOAL      TRODEOALTRODEOAL

    ## Example

    >>> chars = "HELTENIL"
    >>> wrap(chars, range(len(chars)), 4)
    ('HELTHELT\\nENILENIL', [0, 1, 2, 3, 0, 1, 2, 3, -1, 4, 5, 6, 7, 4, 5, 6, 7, -1])
    """
    lines = [text[idx : idx + line_len] for idx in range(0, len(text), line_len)]
    line_ids = [
        list(ids[idx : idx + line_len]) for idx in range(0, len(text), line_len)
    ]
    return (
        "\n".join(line * 2 for line in lines),
        [id for line in [list(line) * 2 + [-1] for line in line_ids] for id in line],
    )


def flip(text, ids, line_len):
    """Flip lines of text and their corresponding IDs 90 degrees.

    HELW      HET
    ENIG  ->  ENR
    TROD      LIO
              WGD

    ## Example

    >>> chars = "HELTENIL"
    >>> flip(chars, range(len(chars)), 4)
    ('HE\\nEN\\nLI\\nTL', [0, 4, -1, 1, 5, -1, 2, 6, -1, 3, 7, -1])
    """
    return (
        "\n".join(text[idx::line_len] for idx in range(line_len)),
        [
            id
            for line in [list(ids[idx::line_len]) + [-1] for idx in range(line_len)]
            for id in line
        ],
    )
