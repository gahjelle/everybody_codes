defmodule EverybodyCodes2024.Day11 do
  @moduledoc """
  Everybody Codes 2024, day 11: Biological Warfare
  """
  require EverybodyCodes

  @doc """
  Parse the input data
  """
  def parse(puzzle_input) do
    puzzle_input
    |> String.split("\n", trim: true)
    |> Enum.map(fn line ->
      [parent, children] = String.split(line, ":")
      {parent, children |> String.split(",") |> Enum.frequencies()}
    end)
    |> Enum.into(%{})
  end

  @doc """
  Solve part 1
  """
  def part1(puzzle_input) do
    puzzle_input |> parse() |> calculate_population(%{"A" => 1}, 4)
  end

  @doc """
  Solve part 2
  """
  def part2(puzzle_input) do
    puzzle_input |> parse() |> calculate_population(%{"Z" => 1}, 10)
  end

  @doc """
  Solve part 3
  """
  def part3(puzzle_input) do
    conversions = puzzle_input |> parse()

    conversions
    |> Map.keys()
    |> Enum.map(&calculate_population(conversions, %{&1 => 1}, 20))
    |> then(fn populations -> Enum.max(populations) - Enum.min(populations) end)
  end

  @doc """
  Calculate the population n days into the future.

  ## Example

      A -> BC -> AAB -> BCBCAA -> AABAABBCBC -> BCBCAABCBCAAAABAAB

      iex> conversions = %{"A" => %{"B" => 1, "C" => 1}, "B" => %{"A" => 2}, "C" => %{"B" => 1}}
      iex> calculate_population(conversions, %{"A" => 1}, 5)
      18
  """
  def calculate_population(_, population, 0), do: population |> Map.values() |> Enum.sum()

  def calculate_population(conversions, population, num_days) do
    calculate_population(
      conversions,
      Enum.reduce(population, %{}, fn {termite, count}, acc ->
        Enum.reduce(conversions[termite], acc, fn {child, child_count}, acc ->
          Map.update(acc, child, count * child_count, &(&1 + count * child_count))
        end)
      end),
      num_days - 1
    )
  end

  def main(path1, path2, path3) do
    EverybodyCodes.solve(&part1/1, &part2/1, &part3/1, path1, path2, path3)
  end
end
