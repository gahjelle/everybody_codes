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
  def part1(puzzle_input), do: fight(puzzle_input, 1)

  @doc """
  Solve part 2
  """
  def part2(puzzle_input), do: fight(puzzle_input, 2)

  @doc """
  Solve part 3
  """
  def part3(puzzle_input), do: fight(puzzle_input, 3)

  @doc """
  Calculate number of potions needed for different group sizes

  ## Examples

      iex> fight("AxBCDDCAxDxx", 1)
      0 + 0 + 1 + 3 + 5 + 5 + 3 + 0 + 0 + 5 + 0 + 0
      iex> fight("AxBCDDCAxDxx", 2)
      0 + 6 + 12 + 5 + 5 + 0
      iex> fight("AxBCDDCAxDxx", 3)
      3 + 19 + 5 + 5
  """
  def fight(puzzle_input, group_size) do
    puzzle_input
    |> String.split("", trim: true)
    |> Enum.chunk_every(group_size)
    |> Enum.map(fn group ->
      (Enum.map(group, fn insect -> @insects[insect] end) |> Enum.sum()) +
        @powerup[Enum.count(group, fn insect -> insect != "x" end)]
    end)
    |> Enum.sum()
  end

  def main(path1, path2, path3) do
    EverybodyCodes.solve(&part1/1, &part2/1, &part3/1, path1, path2, path3)
  end
end
