defmodule EverybodyCodes2024.Day01.Test do
  @moduledoc """
  Tests for Everybody Codes 2024, day 1: The Battle for the Farmlands
  """
  use ExUnit.Case, async: true
  require EverybodyCodes
  import EverybodyCodes2024.Day01, only: [part1: 1, part2: 1, part3: 1]
  doctest(EverybodyCodes2024.Day01, import: true)

  @puzzle_dir "lib/2024/01_the_battle_for_the_farmlands/"
  setup_all do
    {:ok,
     [
       example1: @puzzle_dir |> Path.join("example_p1.txt") |> EverybodyCodes.read_text(),
       example2: @puzzle_dir |> Path.join("example_p2.txt") |> EverybodyCodes.read_text(),
       example3: @puzzle_dir |> Path.join("example_p3.txt") |> EverybodyCodes.read_text(),
       input1:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q01_p1.txt")
         |> EverybodyCodes.read_text(),
       input2:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q01_p2.txt")
         |> EverybodyCodes.read_text(),
       input3:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q01_p3.txt")
         |> EverybodyCodes.read_text()
     ]}
  end

  @tag :example
  test "part 1 example 1", %{example1: example1} do
    assert part1(example1) == 5
  end

  @tag :example
  test "part 2 example 2", %{example2: example2} do
    assert part2(example2) == 28
  end

  @tag :example
  test "part 3 example 3", %{example3: example3} do
    assert part3(example3) == 30
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 1 solved", %{input1: input1} do
    assert part1(input1) == 1292
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 2 solved", %{input2: input2} do
    assert part2(input2) == 5458
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 3 solved", %{input3: input3} do
    assert part3(input3) == 27_463
  end
end
