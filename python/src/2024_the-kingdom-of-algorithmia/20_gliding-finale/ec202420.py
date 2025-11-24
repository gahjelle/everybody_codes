"""Everybody Codes 20, 2024: Gliding Finale."""

import collections
import heapq

from codetiming import Timer

NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
TURNS = {
    NORTH: [EAST, NORTH, WEST],
    EAST: [SOUTH, EAST, NORTH],
    SOUTH: [WEST, SOUTH, EAST],
    WEST: [NORTH, WEST, SOUTH],
}
UPLIFT = {"S": -1, ".": -1, "-": -2, "+": 1, "A": -1, "B": -1, "C": -1}


def parse_grid(puzzle_input):
    """Parse the puzzle input."""
    grid = {
        (row, col): char
        for row, line in enumerate(puzzle_input.split("\n"))
        for col, char in enumerate(line)
        if char != "#"
    }
    start = next(pos for pos, char in grid.items() if char == "S")
    return grid, start


@Timer()
def part1(puzzle_input, seconds=100):
    """Solve part 1."""
    grid, start = parse_grid(puzzle_input)
    return optimize_heights(grid, start, seconds)


@Timer()
def part2(puzzle_input):
    """Solve part 2."""
    grid, start = parse_grid(puzzle_input)
    checkpoints = tuple(
        dict(
            sorted((char, pos) for pos, char in grid.items() if char in "ABC")
        ).values()
    )
    # return 536
    return glide_2(grid, start, SOUTH, checkpoints)


@Timer()
def part3(puzzle_input, start_height=384_400):
    """Solve part 3."""
    grid, start = parse_grid(puzzle_input)
    return glide_to_ground(grid, start, start_height)


def optimize_heights(grid, start, seconds):
    """Find the highest heights after flying for a number of seconds."""
    positions = {(start, SOUTH): 1000}
    max_height = 1000
    for _ in range(seconds):
        new_positions = {}
        for (pos, dir), height in positions.items():
            for new_dir in TURNS[dir]:
                new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
                if new_pos not in grid:
                    continue
                new_height = height + UPLIFT[grid[new_pos]]
                new_positions[(new_pos, new_dir)] = max(
                    new_positions.get((new_pos, new_dir), 0), new_height
                )
        positions = new_positions
        max_height = max(max_height, max(positions.values()))
    return max_height


def glide_to_ground(grid, start, height):
    """Glide as far south as possible before hitting the ground.

    1. Find optimal column to glide within
    2. Navigate to optimal column
    3. Glide until hitting the ground
    """
    num_rows = max(row for row, _ in grid) + 1
    open_cols = [
        col
        for col, count in collections.Counter(col for _, col in grid).items()
        if count == num_rows
    ]
    column_uplift = {
        col: sum(UPLIFT[grid[r, col]] for r in range(num_rows)) for col in open_cols
    }
    column, dheight = max(
        column_uplift.items(), key=lambda item: (item[1], -abs(item[0] - start[1]))
    )

    height = navigate_to(grid, start, (num_rows - 1, column), height)
    south = num_rows - 1

    jumps = height // -dheight
    south += jumps * num_rows
    height += jumps * dheight

    # TODO: account for left_over height
    return south


def navigate_to(grid, start, end, height):
    """Glide from start to end aiming for the heighest height."""
    return height - (abs(end[0] - start[0]) + abs(end[1] - start[1]) - 3 * 2)


def glide_one_segment(grid, start, dir, height):
    num_rows = len({row for row, _ in grid})
    queue = [(-height, 0, start, dir)]
    heights = {}
    best = {}
    has_jumped = False
    while queue:
        neg_height, south, pos, dir = heapq.heappop(queue)
        if neg_height >= 0:
            return max(heights) + 1
        # if south not in heights:
        #     print(south, -neg_height)
        heights[south] = max(-neg_height, heights.get(south, 0))
        if (
            south >= 2 * num_rows
            and not has_jumped
            and all(
                (heights[south - n] - heights[south - n - num_rows])
                - (heights[south - n - 1] - heights[south - n - num_rows - 1])
                == 0
                for n in range(num_rows)
            )
        ):
            step = heights[south] - heights[south - num_rows]
            skips = neg_height // step
            neg_height = neg_height - step * skips
            queue = []
            south += num_rows * skips
            has_jumped = True
        if best.get((south, pos, dir), 0) > -neg_height:
            continue

        best[south, pos, dir] = -neg_height
        for new_dir in TURNS[dir]:
            if new_dir[0] == -1:
                continue
            new_pos = ((pos[0] + new_dir[0]) % num_rows, pos[1] + new_dir[1])
            if new_pos not in grid:
                continue
            new_neg_height = neg_height - UPLIFT.get(grid[new_pos], -1)
            new_south = south + new_dir[0]
            if best.get((new_south, new_pos, new_dir), 0) > -new_neg_height:
                continue
            heapq.heappush(queue, (new_neg_height, new_south, new_pos, new_dir))


# def glide_(grid, start, dir, rounds):
#     queue = collections.deque([(0, 1000, start, dir)])
#     seen = set()
#     current_round = 0
#     max_height = 0
#     while queue:
#         round, height, pos, dir = queue.popleft()
#         if round > current_round:
#             print(round)
#             current_round = round
#             seen.clear()

#         max_height = max(height, max_height)
#         for drow, dcol in TURNS[dir]:
#             new_pos = (pos[0] + drow, pos[1] + dcol)
#             new_dir = (drow, dcol)
#             new_height = height + grid[new_pos]


def glide_1(grid, start, dir, rounds):
    """Glide around and find the optimal height"""
    queue = [(0, 0, -1000, start, dir, 1000)]
    best = {}
    seen = set()
    current_round = 0
    while True:
        _, round, neg_height, pos, dir, max_height = status = heapq.heappop(queue)
        if round == rounds:
            return max_height
        if status in seen:
            continue
        seen.add(status)
        if max_height < best.get(round, 0) - 10:
            continue
        if max_height > best.get(round, 0):
            best[round] = max_height

        if round > current_round:
            print(round, max_height, -neg_height)
            current_round = round

        for drow, dcol in TURNS[dir]:
            new_pos = (pos[0] + drow, pos[1] + dcol)
            if new_pos in grid:
                new_height = -neg_height + UPLIFT[grid[new_pos]]
                heapq.heappush(
                    queue,
                    (
                        -new_height + 2 * round,
                        round + 1,
                        -new_height,
                        new_pos,
                        (drow, dcol),
                        max(max_height, new_height),
                    ),
                )


def glide_2(grid, start, dir, checkpoints):
    queue = [(0, 0, start, dir, checkpoints, 10000)]
    seen = set()
    cps = {}
    best = {}
    current_round = 0
    num_checkpoints = len(checkpoints)
    while queue:
        _, time, pos, dir, checkpoints, height = heapq.heappop(queue)
        if pos == start and not checkpoints and height >= 10000:
            return time
        if (pos, dir, checkpoints, height) in seen:
            continue
        seen.add((pos, dir, checkpoints, height))
        if not checkpoints:
            best[pos, dir] = max(best.get((pos, dir), 0), height)

        if time > current_round:
            print(time, num_checkpoints, height, cps)
            current_round = time
        if len(checkpoints) < num_checkpoints:
            num_checkpoints = len(checkpoints)
            cps[num_checkpoints] = time

        for new_dir in TURNS[dir]:
            new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
            if new_pos not in grid:
                continue
            new_height = height + UPLIFT.get(grid[new_pos], -1)
            if new_height < 0:
                continue
            new_checkpoints = (
                checkpoints[1:]
                if checkpoints and checkpoints[0] == new_pos
                else checkpoints
            )
            if not new_checkpoints and best.get((new_pos, new_dir), 0) > new_height:
                continue
            if cps.get(len(new_checkpoints) - 1, 999) < time - 25:
                continue
            new_h = time + 1
            queue.append(
                (new_h, time + 1, new_pos, new_dir, new_checkpoints, new_height)
            )


# def glide_2_(grid, start, dir, checkpoints):
#     """Explore the grid while hitting checkpoints"""
#     targets = set(checkpoints)
#     queue = [((0, 0, 0), 0, start, dir, (), 1000)]
#     seen = {}
#     current_round = 0
#     while queue:
#         _, num_steps, pos, dir, checkpoints, height = heapq.heappop(queue)
#         if (pos, dir, height, checkpoints) in seen:
#             continue
#         if pos == start and set(checkpoints) == targets and height >= 1000:
#             return num_steps
#         if num_steps > current_round:
#             print(num_steps, len(queue))
#             current_round = num_steps

#         seen[pos, dir, height, checkpoints] = num_steps
#         for drow, dcol in TURNS[dir]:
#             new_pos = (pos[0] + drow, pos[1] + dcol)
#             new_dir = (drow, dcol)
#             if new_pos in grid:
#                 new_herbs = (
#                     tuple(sorted(checkpoints + (grid[pos],)))
#                     if grid[pos] in targets and grid[pos] not in checkpoints
#                     else checkpoints
#                 )
#                 new_height = height + UPLIFT.get(grid[new_pos], -1)
#                 if num_steps + 1 < seen.get(
#                     (new_pos, new_dir, new_height, new_herbs), 9_999
#                 ):
#                     heapq.heappush(
#                         queue,
#                         (
#                             (num_steps + 1, 0, 0),
#                             num_steps + 1,
#                             new_pos,
#                             new_dir,
#                             new_herbs,
#                             new_height,
#                         ),
#                     )
#     return 9_999


# def glide_2_(grid, start, dir, checkpoints):
#     """Glide around and find the optimal height"""
#     queue = [(0, 0, -1000, start, dir, checkpoints)]
#     best = {}
#     seen = set()
#     current_round = 0
#     while True:
#         _, round, neg_height, pos, dir, checkpoints = status = heapq.heappop(queue)
#         if grid[pos] == "S" and -neg_height >= 1000 and not checkpoints:
#             return round
#         if status in seen:
#             continue
#         seen.add(status)
#         if round > current_round:
#             print(round, pos, checkpoints, -neg_height)
#             current_round = round

#         for drow, dcol in TURNS[dir]:
#             new_pos = (pos[0] + drow, pos[1] + dcol)
#             if new_pos in grid:
#                 new_height = -neg_height + UPLIFT.get(grid[new_pos], -1)
#                 new_checkpoints = tuple(pos for pos in checkpoints if pos != new_pos)
#                 heapq.heappush(
#                     queue,
#                     (
#                         len(new_checkpoints) - (-new_height >= 1000),
#                         round + 1,
#                         -new_height,
#                         new_pos,
#                         (drow, dcol),
#                         new_checkpoints,
#                     ),
#                 )
