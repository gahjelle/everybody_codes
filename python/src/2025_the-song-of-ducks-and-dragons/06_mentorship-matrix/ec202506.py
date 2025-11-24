"""Everybody Codes quest 6, 2025: Mentorship Matrix."""

MENTOR = "ABC"
NOVICE = "abc"
PAIR = dict(zip(MENTOR + NOVICE, NOVICE + MENTOR))


def parse_by_skill(puzzle_input: str) -> dict[str, list[str]]:
    """Parse the input and sort by skill type."""
    skills = set(puzzle_input.lower())
    return {
        skill: [char for char in puzzle_input if char.lower() == skill]
        for skill in skills
    }


def part1(puzzle_input: str) -> int:
    """Solve part 1."""
    skills = parse_by_skill(puzzle_input)
    return count_mentors(skills["a"])


def part2(puzzle_input: str) -> int:
    """Solve part 1."""
    skills = parse_by_skill(puzzle_input)
    return sum(count_mentors(people) for people in skills.values())


def count_mentors(people: list[str]) -> int:
    """Count the number of mentor/novice pairs in the given list.

    ## Example:

    >>> count_mentors("bBbbB")
    2
    >>> count_mentors("CCcCCCc")
    7
    """
    acc = 0  # Can alternatively use itertools.accumulate
    mentors = [acc := acc + (person in MENTOR) for person in people]
    return sum(
        num_mentors
        for num_mentors, person in zip(mentors, people, strict=True)
        if person in NOVICE
    )


def part3(puzzle_input: str, num_repeat: int = 1000, range_len: int = 1000) -> int:
    """Solve part 3.

    Sweep over the people while keeping a running tally of mentors and novices
    within range to the left. Counting both mentors and novices is offset by
    only looking left.
    """
    num_chars = len(puzzle_input)
    to_the_left = {person: 0 for person in PAIR}

    num_pairs = 0
    for idx, person in enumerate(puzzle_input * num_repeat):
        num_pairs += to_the_left[PAIR[person]]
        if idx >= range_len:
            to_the_left[puzzle_input[(idx - range_len) % num_chars]] -= 1
        to_the_left[person] += 1
    return num_pairs
