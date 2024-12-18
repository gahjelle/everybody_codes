# Everybody Codes in Python

Solutions to [Everybody Codes](https://everybody.codes/) in [Python](https://www.python.org/) (57🦆):

|   Day | [2024](2024_the_kingdom_of_algorithmia)                                   |
|------:|:--------------------------------------------------------------------------|
|     1 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/01_the_battle_for_the_farmlands) |
|     2 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/02_the_runes_of_power)           |
|     3 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/03_mining_maestro)               |
|     4 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/04_royal_smiths_puzzle)          |
|     5 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/05_pseudo-random_clap_dance)     |
|     6 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/06_the_tree_of_titans)           |
|     7 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/07_not_fast_but_furious)         |
|     8 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/08_a_shrine_for_nullpointer)     |
|     9 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/09_sparkling_bugs)               |
|    10 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/10_shrine_needs_to_shine)        |
|    11 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/11_biological_warfare)           |
|    12 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/12_desert_shower)                |
|    13 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/13_never_gonna_let_you_down)     |
|    14 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/14_the_house_of_palms)           |
|    15 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/15_from_the_herbalists_diary)    |
|    16 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/16_cat_grin_of_fortune)          |
|    17 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/17_galactic_geometry)            |
|    18 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/18_the_ring)                     |
|    19 | [🦆🦆🦆](2024_the_kingdom_of_algorithmia/19_encrypted_duck)               |
|    20 |                                                                           |

## Running the Solutions

Navigate to the puzzle folder:

```console
$ cd 2024_the_kingdom_of_algorithmia/01_the_battle_for_the_farmlands/
```

Run the full solution by specifying puzzle input:

```console
$ python ec202401.py everybody_codes_e2024_q01_p*
```

You can also run on example input:

```console
$ python ec202401.py example_p*.txt
```

It's possible to work with individual parts in the REPL:

```pycon
>>> import pathlib
>>> import ec202401
```

<!--
## Bootstrap a Puzzle Solution

Use `copier` to invoke the Python template and set up files for a new solution:

```console
$ copier copy --trust gh:gahjelle/template-aoc-python .
```

Answer the questions and allow the hook to download your personal input.
-->

## Test a solution

Test individual puzzles from within the puzzle folder:

```console
$ cd 2024_the_kingdom_of_algorithmia/01_the_battle_for_the_farmlands/
$ pytest -v
```

You can test (and benchmark) all puzzles for their output by running `test_all_puzzles.py`:

```console
$ pytest -v test_all_puzzles.py
```

Finally, you can run all puzzle unit tests by running pytest on the puzzle folders:

```console
$ pytest -v 20*
```

## Adding a Solution to GitHub

Follow these steps after solving a puzzle:

1. Store the solution to an output file:

    ```console
    $ python ec202401.py everybody_codes_e2024_q01_p* > output.py.txt
    ```

2. Run benchmarks and add them to the README:

    ```console
    $ pytest test_all_puzzles.py -k 2024
    $ cat timings.py.md
    ```

3. Update READMEs across all projects:

    ```console
    $ cd ..
    $ make
    ```
