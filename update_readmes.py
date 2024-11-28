"""Update Everybody Codes READMEs"""

# Standard library imports
import pathlib
import sys
from dataclasses import dataclass

# Third party imports
import pandas as pd
import parse


@dataclass
class Puzzle:
    year: int
    day: int

    @property
    def title(self):
        titles = {
            2024: {
                1: "The Battle for the Farmlands",
                2: "The Runes of Power",
                3: "Mining Maestro",
                4: "Royal Smith's Puzzle",
                5: "Pseudo-Random Clap Dance",
                6: "The Tree of Titans",
                7: "Not Fast but Furious",
                8: "A Shrine for Nullpointer",
                9: "Sparkling Bugs",
                10: "Shrine Needs to Shine",
                11: "Biological Warfare",
                12: "Desert Shower",
                13: "Never Gonna Let You Down",
                14: "The House of Palms",
                15: "From the Herbalist's Diary",
                16: "Cat Grin of Fortune",
                17: "Galactic Geometry",
                18: "The Ring",
            }
        }
        return titles[self.year][self.day]

    @property
    def url(self):
        return f"https://everybody.codes/event/{self.year}/quests/{self.day}"


def _solutions(glob, pattern, path):
    """Identify solution files for different languages"""
    solutions = []
    for output_path in sorted(BASEDIR.glob(glob)):
        if match := pattern.parse(str(output_path.relative_to(BASEDIR))):
            solutions.append(
                (
                    match["year"],
                    match["day"],
                    match["language"],
                    BASEDIR / path.format(**match.named),
                )
            )
    return solutions


BASEDIR = pathlib.Path(__file__).resolve().parent
EMOJI = {
    "python": "🐍",
    "julia": "🍡",
    "elixir": "💧",
    "gleam": "🌠",
    "crystal": "💎",
    "lua": "🌜",
    "ruby": "🔶",
    "rust": "🪤",
}
HOMEPAGE = {
    "python": "https://www.python.org/",
    "julia": "https://julialang.org/",
    "elixir": "https://elixir-lang.org/",
    "gleam": "https://gleam.run/",
    "crystal": "https://crystal-lang.org/",
    "lua": "https://www.lua.org/",
    "ruby": "https://www.ruby-lang.org/en/",
    "rust": "https://www.rust-lang.org/",
}
SOLUTIONS = {
    "python": _solutions(
        "python/*/*/output.py.txt*",
        parse.compile(
            "{language}/{year:d}_{event}/{day:02d}_{name}/output.py.{_suffix}"
        ),
        "python/{year}_{event}/{day:02d}_{name}/README.md",
    ),
    "elixir": _solutions(
        "elixir/lib/*/*/output.ex.txt*",
        parse.compile("{language}/lib/{year:d}/{day:02d}_{name}/output.ex.{_suffix}"),
        "elixir/lib/{year}/{day:02d}_{name}/README.md",
    ),
}


def _as_markdown_table(puzzles):
    """Format puzzle list as Markdown table"""
    return (
        pd.DataFrame(puzzles)
        .pivot_table(index="Day", columns="Year", values="link", aggfunc="sum")
        .reindex(range(1, 21))
        .fillna("")
        .to_markdown()
    )


def _as_markdown_language_list(puzzles):
    """Format language list as Markdown"""
    languages = (
        pd.DataFrame(puzzles)
        .assign(
            emoji=lambda df: df.link.str.extract(r"\[(.)\]"),
            language=lambda df: df.link.str.extract(r"\[.\]\((\w+)/"),
        )
        .groupby("language")
        .agg(emoji=("emoji", "first"), num_puzzles=("language", "size"))
        .reset_index()
        .assign(
            name=lambda df: df.language.str.capitalize(),
            stars=lambda df: df.num_puzzles * 3,
        )
        .sort_values(by="stars", ascending=False)
    )
    return "\n".join(
        f"- {lang.emoji} [{lang.name}]({lang.language}/) ({lang.stars} 🦆)"
        for lang in languages.itertuples()
    )


def _as_total_stars_overview(puzzles):
    """Show total number of stars"""
    num_unique_puzzles = pd.DataFrame(puzzles).groupby(["Year", "Day"]).size().size
    return f"{3 * num_unique_puzzles} 🦆"


def _year_link(year, link):
    return link if link.name.startswith(str(year)) else _year_link(year, link.parent)


def _strip_readme(path):
    """Link to parent directory instead of README.md"""
    return path.parent if path.name == "README.md" else path


def _assemble_puzzle_list(puzzles, emoji=None, link_dir=BASEDIR, link_years=False):
    """Create a formatted list of puzzles"""
    return [
        {
            "Year": (
                f"[{year}]({_year_link(year, puzzle_path).relative_to(link_dir)})"
                if link_years
                else year
            ),
            "Day": day,
            "link": (
                f"[{EMOJI[language] if emoji is None else emoji}]"
                f"({_strip_readme(puzzle_path).relative_to(link_dir)})"
            ),
        }
        for year, day, language, puzzle_path in puzzles
    ]


def _other_solutions(current_language, current_year, current_day, puzzle_dir):
    """List solutions in languages different from current"""
    relative_basedir = "../" * len(puzzle_dir.parent.relative_to(BASEDIR).parts)

    other_solutions = [
        f"- [{EMOJI[language]} {language.title()}]"
        f"({relative_basedir}{_strip_readme(path).relative_to(BASEDIR)})"
        for language, solutions in SOLUTIONS.items()
        for year, day, _, path in solutions
        if year == current_year and day == current_day and language != current_language
    ]
    if other_solutions:
        return "\nSolutions in other languages:\n\n{}\n".format(
            "\n".join(other_solutions)
        )
    else:
        return ""


def _language_template(language):
    """Add information from the language template"""
    template_path = BASEDIR / language / "README.template"
    return template_path.read_text() if template_path.exists() else ""


def update_main_readme():
    """Create a table with an overview over all solutions"""
    template_path = BASEDIR / "README.template"
    readme_path = BASEDIR / "README.md"

    puzzles = _assemble_puzzle_list(
        [puzzle for language in SOLUTIONS.values() for puzzle in language]
    )
    readme_path.write_text(
        template_path.read_text().format(
            list_of_languages=_as_markdown_language_list(puzzles),
            total_stars=_as_total_stars_overview(puzzles),
            table_of_puzzles=_as_markdown_table(puzzles),
        )
    )


def update_language_readme(language):
    """Create a table listing solutions for a given language"""
    puzzles = _assemble_puzzle_list(
        SOLUTIONS[language],
        emoji="🦆🦆🦆",
        link_dir=BASEDIR / language,
        link_years=True,
    )
    print(f"Updating READMEs for {language} solutions: {3 * len(puzzles)}🦆")

    text = (
        f"# Everybody Codes in {language.title()}\n\n"
        "Solutions to [Everybody Codes](https://everybody.codes/) in "
        f"[{language.title()}]({HOMEPAGE[language]}) "
        f"({3 * len(puzzles)}🦆):\n\n"
        f"{_as_markdown_table(puzzles)}\n\n"
        f"{_language_template(language)}"
    )
    (BASEDIR / language / "README.md").write_text(text)


def update_puzzle_readmes(language):
    """Add a README for each puzzle with a link to the Everybody Codes website"""
    for year, day, _, readme_path in SOLUTIONS[language]:
        puzzle = Puzzle(year=year, day=day)
        readme_path.write_text(
            f"# {puzzle.title}\n\n"
            f"**Everybody Codes: Day {day}, {year}**\n\n"
            f"Puzzle text: <{puzzle.url}>\n"
            f"{_other_solutions(language, year, day, readme_path)}"
        )


if __name__ == "__main__":
    update_main_readme()
    for language in sys.argv[1:]:
        update_language_readme(language)
        update_puzzle_readmes(language)
