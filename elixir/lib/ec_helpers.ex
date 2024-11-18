defmodule EverybodyCodes do
  @moduledoc """
  Advent of Code helper functions and macros
  """

  defmacro __using__(_) do
    quote do
      import EverybodyCodes
    end
  end

  @doc """
  Read text from the given path.
  """
  def read_text(path) do
    with {:ok, file} <- File.read(path), do: file |> String.trim_trailing()
  end

  @doc """
  Solve one EverybodyCodes puzzle given input path and part1(), part2(), and part3() functions.
  """
  def solve(part1_func, part2_func, part3_func, path1, path2, path3) do
    IO.puts(
      "\n#{path1 |> Path.basename()}, #{path2 |> Path.basename()}, #{path3 |> Path.basename()}:"
    )

    read_text(path1) |> part1_func.() |> IO.puts()
    read_text(path2) |> part2_func.() |> IO.puts()
    read_text(path3) |> part3_func.() |> IO.puts()
  end
end
