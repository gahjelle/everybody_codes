defmodule Mix.Tasks.Benchmark do
  @moduledoc """
  Benchmark Everybody Codes solutions
  """

  use Mix.Task
  require EverybodyCodes

  @bm_args [warmup: 0.1, time: 2]

  @shortdoc "Benchmark Everybody Codes"
  def run([year, day]) do
    day_string = String.pad_leading(day, 2, "0")

    ec_module =
      "Elixir.EverybodyCodes#{year}.Day#{day_string}"
      |> String.to_existing_atom()

    puzzle_dir = Path.wildcard("lib/#{year}/#{day_string}_*/") |> hd

    input1 =
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p1.txt")
      |> EverybodyCodes.read_text()

    input2 =
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p2.txt")
      |> EverybodyCodes.read_text()

    input3 =
      Path.join(puzzle_dir, "everybody_codes_e#{year}_q#{day_string}_p3.txt")
      |> EverybodyCodes.read_text()

    @bm_args
    |> Benchee.init()
    |> Benchee.system()
    |> Benchee.benchmark("#{year} day #{day}, part 1", fn -> ec_module.part1(input1) end)
    |> Benchee.benchmark("#{year} day #{day}, part 2", fn -> ec_module.part2(input2) end)
    |> Benchee.benchmark("#{year} day #{day}, part 3", fn -> ec_module.part3(input3) end)
    |> Benchee.collect()
    |> Benchee.statistics()
    |> Benchee.Formatter.output()
    |> format_as_markdown(puzzle_dir)
  end

  defp format_as_markdown(%{scenarios: scenarios}, puzzle_path) do
    [part1, part2, part3] =
      scenarios
      |> Enum.map(fn s -> s.run_time_data.statistics.median end)

    [part1, part2, part3, total] =
      [part1, part2, part3, part1 + part2 + part3] |> Enum.map(&format_as_timestring/1)

    [directory, year | _] = puzzle_path |> Path.split() |> Enum.reverse()
    day = directory |> String.slice(0..1) |> String.to_integer()
    file = "ec#{year}#{String.slice(directory, 0..1)}.ex"

    name =
      directory
      |> String.slice(3..99)
      |> String.replace("_", " ")
      |> String.split(" ")
      |> Enum.map_join(" ", &String.capitalize/1)

    "\n\n| #{day} | #{name} | [#{file}](#{directory}/#{file}) | #{part1} | #{part2} | #{part3} | #{total} |"
    |> IO.puts()
  end

  defp format_as_timestring(nanoseconds) do
    Number.SI.number_to_si(nanoseconds / 1_000_000_000, unit: "s", separator: " ", precision: 2)
    |> String.replace(" ns", " ns ⚪️")
    |> String.replace(" µs", " µs ⚪️")
    |> String.replace(" ms", " ms 🔵")
    |> String.replace(" s", " s 🔴")
  end
end
