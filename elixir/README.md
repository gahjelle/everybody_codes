# Everybody Codes in Elixir

Solutions to [Everybody Codes](https://everybody.codes/) in [Elixir](https://elixir-lang.org/) (9🦆):

|   Day | [2024](lib/2024)                                   |
|------:|:---------------------------------------------------|
|     1 | [🦆🦆🦆](lib/2024/01_the_battle_for_the_farmlands) |
|     2 |                                                    |
|     3 | [🦆🦆🦆](lib/2024/03_mining_maestro)               |
|     4 |                                                    |
|     5 |                                                    |
|     6 |                                                    |
|     7 |                                                    |
|     8 |                                                    |
|     9 |                                                    |
|    10 |                                                    |
|    11 | [🦆🦆🦆](lib/2024/11_biological_warfare)           |
|    12 |                                                    |
|    13 |                                                    |
|    14 |                                                    |
|    15 |                                                    |
|    16 |                                                    |
|    17 |                                                    |
|    18 |                                                    |
|    19 |                                                    |
|    20 |                                                    |

## Run the Solutions

There are two special Everybody Codes mix tasks:

- `mix solve 2024 1` solves the given puzzle, in this case Puzzle 1, 2024.
- `mix benchmark 2024 1` benchmarks the given puzzle, in this case Puzzle 1, 2024.

You can also run the solutions manually inside a `iex -S mix` session:

```elixir
iex> import EverybodyCodes2024.Day01
iex> EverybodyCodes.solve("lib/2024/01_the_battle_for_the_farmlands/input.txt", &parse/1, &part1/1, &part2/1)
```

Alternatively, you can only read and parse the data, and work with them manually from there:

```elixir
iex> import EverybodyCodes2024.Day01
iex> data = EverybodyCodes.read_text("lib/2024/01_the_battle_for_the_farmlands/input.txt") |> part1()
```

## Bootstrap a Puzzle Solution

Use `copier` to invoke the Elixir template and set up files for a new solution:

```console
$ copier path/to/template-aoc-elixir/ .
```

Answer the questions and allow the hook to download your personal input.


## Test a Solution

Each puzzle comes with a test file that can be run with `mix test`:

```console
$ mix test test/ec202401_test.exs
```

You can run all tests by not specifying a particular test file:

```console
$ mix test
```

This will run all tests except those marked as `slow` or `solution`. The
`solution` tests run the full solution and compare the result to the correct
solution. You can run them by including them:

```console
$ mix test --include solution
```

There are also a few other tags you can use:

```console
$ mix test --only solution
$ mix test --only year2024
$ mix test --include solution --exclude year2024
```


## Adding a Solution to GitHub

Follow these steps after solving a puzzle:

1. Store the solution to an output file:

    ```console
    $ mix solve 2024 1 > lib/2024/01_the_battle_for_the_farmlands/output.ex.txt
    ```

2. Run benchmarks and add them to the README:

    ```console
    $ mix benchmark 2024 1
    ```

3. Update READMEs across all projects:

    ```console
    $ cd ..
    $ make
    ```
