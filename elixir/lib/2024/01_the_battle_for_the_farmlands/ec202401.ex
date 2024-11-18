defmodule EverybodyCodes2024.Day01 do
  @moduledoc """
  Everybody Codes 2024, day 1: The Battle for the Farmlands
  """
  require EverybodyCodes

  @insects %{"A" => 0, "B" => 1, "C" => 3, "D" => 5, "x" => 0}
  @powerup %{0 => 0, 1 => 0, 2 => 2, 3 => 6}

  @doc """
  Solve part 1
  """
  def part1(puzzle_input) do
    puzzle_input
    |> String.split("", trim: true)
    |> Enum.map(fn insect -> @insects[insect] end)
    |> Enum.sum()
  end

  @doc """
  Solve part 2
  """
  def part2(puzzle_input) do
    puzzle_input
    |> String.split("", trim: true)
    |> Enum.chunk_every(2)
    |> Enum.map(fn pair ->
      (Enum.map(pair, fn insect -> @insects[insect] end) |> Enum.sum()) +
        @powerup[Enum.count(pair, fn insect -> insect != "x" end)]
    end)
    |> Enum.sum()
  end

  @doc """
  Solve part 3
  """
  def part3(puzzle_input) do
    puzzle_input
    |> String.split("", trim: true)
    |> Enum.chunk_every(3)
    |> Enum.map(fn pair ->
      (Enum.map(pair, fn insect -> @insects[insect] end) |> Enum.sum()) +
        @powerup[Enum.count(pair, fn insect -> insect != "x" end)]
    end)
    |> Enum.sum()
  end

  def main(path1, path2, path3) do
    EverybodyCodes.solve(&part1/1, &part2/1, &part3/1, path1, path2, path3)
  end
end
