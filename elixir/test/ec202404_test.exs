defmodule EverybodyCodes2024.Day04.Test do
  @moduledoc """
  Tests for Everybody Codes 2024, day 4: Royal Smith's Puzzle
  """
  use ExUnit.Case, async: true
  require EverybodyCodes
  import EverybodyCodes2024.Day04, only: [part1: 1, part2: 1, part3: 1]
  doctest(EverybodyCodes2024.Day04, import: true)

  @puzzle_dir "lib/2024/04_royal_smiths_puzzle/"
  setup_all do
    {:ok,
     [
       example1: @puzzle_dir |> Path.join("example_p1.txt") |> EverybodyCodes.read_text(),
       example2: @puzzle_dir |> Path.join("example_p2.txt") |> EverybodyCodes.read_text(),
       example3: @puzzle_dir |> Path.join("example_p3.txt") |> EverybodyCodes.read_text(),
       input1:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q04_p1.txt")
         |> EverybodyCodes.read_text(),
       input2:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q04_p2.txt")
         |> EverybodyCodes.read_text(),
       input3:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q04_p3.txt")
         |> EverybodyCodes.read_text()
     ]}
  end

  @tag :example
  test "part 1 example 1", %{example1: example1} do
    assert part1(example1) == 10
  end

  @tag :example
  test "part 2 example 2", %{example2: example2} do
    assert part2(example2) == 10
  end

  @tag :example
  test "part 3 example 3", %{example3: example3} do
    assert part3(example3) == 8
  end

  @tag :solution
  @tag :year2024
  @tag :day4
  test "part 1 solved", %{input1: input1} do
    assert part1(input1) == 87
  end

  @tag :solution
  @tag :year2024
  @tag :day4
  test "part 2 solved", %{input2: input2} do
    assert part2(input2) == 870_691
  end

  @tag :solution
  @tag :year2024
  @tag :day4
  test "part 3 solved", %{input3: input3} do
    assert part3(input3) == 119_340_747
  end
end
