defmodule EverybodyCodes2024.Day04 do
  @moduledoc """
  Everybody Codes 2024, day 4: Royal Smith's Puzzle
  """
  require EverybodyCodes

  @doc """
  Parse the input data
  """
  def parse(puzzle_input) do
    puzzle_input |> String.split("\n", trim: true) |> Enum.map(&String.to_integer/1)
  end

  @doc """
  Solve part 1
  """
  def part1(puzzle_input) do
    puzzle_input
    |> parse()
    |> then(fn nails -> count_strikes(nails, Enum.min(nails)) end)
  end

  @doc """
  Solve part 2
  """
  def part2(puzzle_input), do: part1(puzzle_input)

  @doc """
  Solve part 3
  """
  def part3(puzzle_input) do
    nails = puzzle_input |> parse()

    {_, approx_target} =
      Enum.min(nails)..Enum.max(nails)//1000
      |> Task.async_stream(fn target -> {count_strikes(nails, target), target} end)
      |> Enum.map(fn {:ok, result} -> result end)
      |> Enum.min()

    (approx_target - 1000)..(approx_target + 1000)
    |> Task.async_stream(&count_strikes(nails, &1))
    |> Enum.map(fn {:ok, result} -> result end)
    |> Enum.min()
  end

  @doc """
  Count the number of hammer strikes needed to align nails at target

  ## Example

      iex> count_strikes([2, 8, 1, 1, 9, 7, 7], 3)
      24
  """
  def count_strikes(nails, target) do
    nails |> Enum.map(&abs(&1 - target)) |> Enum.sum()
  end

  def main(path1, path2, path3) do
    EverybodyCodes.solve(&part1/1, &part2/1, &part3/1, path1, path2, path3)
  end
end
