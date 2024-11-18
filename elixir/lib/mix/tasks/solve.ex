defmodule Mix.Tasks.Solve do
  @moduledoc """
  Solve one Everybody Codes puzzle with the given input files
  """
  use Mix.Task

  @shortdoc "Solve Everybody Codes"
  def run([year, day]) do
    day_string = String.pad_leading(day, 2, "0")
    puzzle_dir = Path.wildcard("lib/#{year}/#{day_string}_*/") |> hd

    run([
      year,
      day,
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p1.txt"),
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p2.txt"),
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p3.txt")
    ])
  end

  def run([year, day | files]) do
    ec_module =
      "Elixir.EverybodyCodes#{year}.Day#{String.pad_leading(day, 2, "0")}"
      |> String.to_existing_atom()

    [path1, path2, path3] = files
    ec_module.main(path1, path2, path3)
  end
end
