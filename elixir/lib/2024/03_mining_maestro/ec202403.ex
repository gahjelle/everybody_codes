defmodule EverybodyCodes2024.Day03 do
  @moduledoc """
  Everybody Codes 2024, day 3: Mining Maestro
  """
  require EverybodyCodes

  @neighbors_adjacent [{-1, 0}, {0, -1}, {0, 1}, {1, 0}]
  @neighbors_diagonal [{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}]

  @doc """
  Solve part 1
  """
  def part1(puzzle_input) do
    puzzle_input |> parse_grid() |> count_blocks(@neighbors_adjacent)
  end

  @doc """
  Solve part 2
  """
  def part2(puzzle_input) do
    puzzle_input |> parse_grid() |> count_blocks(@neighbors_adjacent)
  end

  @doc """
  Solve part 3
  """
  def part3(puzzle_input) do
    puzzle_input |> parse_grid() |> count_blocks(@neighbors_diagonal)
  end

  def parse_grid(grid) do
    for {line, row} <- grid |> String.split("\n", trim: true) |> Enum.with_index(),
        {char, col} <- line |> String.to_charlist() |> Enum.with_index(),
        char == ?#,
        do: {row, col},
        into: MapSet.new()
  end

  def count_blocks(grid, neighbors) do
    if Enum.empty?(grid),
      do: 0,
      else: Enum.count(grid) + count_blocks(grid |> shrink(neighbors), neighbors)
  end

  def shrink(grid, neighbors) do
    grid
    |> Enum.filter(fn {row, col} ->
      Enum.all?(neighbors, fn {drow, dcol} -> {row + drow, col + dcol} in grid end)
    end)
    |> Enum.into(MapSet.new())
  end

  def main(path1, path2, path3) do
    EverybodyCodes.solve(&part1/1, &part2/1, &part3/1, path1, path2, path3)
  end
end
