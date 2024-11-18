defmodule EverybodyCodes2024.Day03.Test do
  @moduledoc """
  Tests for Everybody Codes 2024, day 3: Mining Maestro
  """
  use ExUnit.Case, async: true
  require EverybodyCodes
  import EverybodyCodes2024.Day03, only: [part1: 1, part2: 1, part3: 1]

  @puzzle_dir "lib/2024/03_mining_maestro/"
  setup_all do
    {:ok,
     [
       example1: @puzzle_dir |> Path.join("example_p1.txt") |> EverybodyCodes.read_text(),
       example2: @puzzle_dir |> Path.join("example_p2.txt") |> EverybodyCodes.read_text(),
       example3: @puzzle_dir |> Path.join("example_p3.txt") |> EverybodyCodes.read_text(),
       input1:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q03_p1.txt")
         |> EverybodyCodes.read_text(),
       input2:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q03_p2.txt")
         |> EverybodyCodes.read_text(),
       input3:
         @puzzle_dir
         |> Path.join("everybody_codes_e2024_q03_p3.txt")
         |> EverybodyCodes.read_text()
     ]}
  end

  @tag :example
  test "part 1 example 1", %{example1: example1} do
    assert part1(example1) == 35
  end

  @tag :example
  test "part 2 example 2", %{example2: example2} do
    assert part2(example2) == 35
  end

  @tag :example
  test "part 3 example 3", %{example3: example3} do
    assert part3(example3) == 29
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 1 solved", %{input1: input1} do
    assert part1(input1) == 125
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 2 solved", %{input2: input2} do
    assert part2(input2) == 2798
  end

  @tag :solution
  @tag :year2024
  @tag :day1
  test "part 3 solved", %{input3: input3} do
    assert part3(input3) == 10_089
  end
end
