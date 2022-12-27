from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None
    with open("puzzle_14_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    rock = []
    for line in data:
        line = line.strip()
        coords = line.split(" -> ")

        point = None
        for coord in coords:
            point_coords = coord.split(",")
            x = point_coords[0]
            y = point_coords[1]
            
            p = (int(x), int(y))
            if point == None:
                point = p
                continue

            rock_line = (point, p)
            rock.append(rock_line)
            
            point = p

    return rock


def get_grid_range(data):
    min_x = None
    min_y = 0

    max_x = None
    max_y = None

    for line in data:
        p0 = line[0]
        p1 = line[1]

        x0 = p0[0]
        y0 = p0[1]

        x1 = p1[0]
        y1 = p1[1]

        if min_x == None:
            min_x = x0

        if min_y == None:
            min_y = y0

        if max_x == None:
            max_x = x0

        if max_y == None:
            max_y = y0

        min_x = min(min_x, x0, x1)
        min_y = min(min_y, y0, y1)

        max_x = max(max_x, x0, x1)
        max_y = max(max_y, y0, y1)

    # Adjust x_range for part 2
    x_range = max_x - min_x
    y_range = max_y - min_y

    min_x = 500 - y_range - 2
    max_x = 500 + y_range + 2
    x_range = max_x - min_x + 1


    return (min_x, min_y), (max_x, max_y)


def build_grid(data):
    min_x = None
    min_y = 0

    max_x = None
    max_y = None

    for line in data:
        p0 = line[0]
        p1 = line[1]

        x0 = p0[0]
        y0 = p0[1]

        x1 = p1[0]
        y1 = p1[1]

        if min_x == None:
            min_x = x0

        if min_y == None:
            min_y = y0

        if max_x == None:
            max_x = x0

        if max_y == None:
            max_y = y0

        min_x = min(min_x, x0, x1)
        min_y = min(min_y, y0, y1)

        max_x = max(max_x, x0, x1)
        max_y = max(max_y, y0, y1)


    x_range = max_x - min_x
    y_range = max_y - min_y

    # Adjust x_range for part 2
    min_x = 500 - y_range - 2
    max_x = 500 + y_range + 2
    x_range = max_x - min_x + 1

    grid = [['.' for _ in range(x_range + 3)] for _ in range(y_range + 3)]

    normalized_data = []
    for line in data:
        start = line[0]
        end = line[1]

        new_start = (start[0] - min_x, start[1] - min_y)
        new_end = (end[0] - min_x, end[1] - min_y)

        normalized_data.append((new_start, new_end))


    #for i in range(len(data)):
    #    print("{} -> {}".format(data[i], normalized_data[i]))

    for line in normalized_data:
        start = line[0]
        end = line[1]

        line_min_x = min(start[0], end[0])
        line_max_x = max(start[0], end[0])
        line_min_y = min(start[1], end[1])
        line_max_y = max(start[1], end[1])

        for x in range(line_min_x, line_max_x + 1):
            for y in range(line_min_y, line_max_y + 1):
                grid[y][x] = '#'

    return grid


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def part_01(data):
    #for line in data:
    #    print(line)

    grid = build_grid(data)
    #print_grid(grid)

    grid_start, grid_end = get_grid_range(data)

    sand_start = (500 - grid_start[0], 0)
    sand_unit = [sand_start[0], 0]
    count = 0

    while sand_unit[1] < len(grid) - 3:
        x = sand_unit[0]
        y = sand_unit[1]
        
        # down
        if grid[y + 1][x] == '.':
            sand_unit[1] += 1
            continue

        # left
        if grid[y + 1][x - 1] == '.':
            sand_unit[0] -= 1
            sand_unit[1] += 1
            continue

        # right
        if grid[y + 1][x + 1] == '.':
            sand_unit[0] += 1
            sand_unit[1] += 1
            continue

        # next
        grid[y][x] = 'o'
        sand_unit[0] = sand_start[0]
        sand_unit[1] = 0

        count += 1

    return count

def part_02(data):
    grid = build_grid(data)
    grid[-1] = ['#' for _ in range(len(grid[0]))]
    
    #print_grid(grid)
    
    grid_start, grid_end = get_grid_range(data)

    sand_start = (500 - grid_start[0], 0)
    sand_unit = [sand_start[0], 0]
    count = 0

    while grid[0][sand_start[0]] != 'o':
        x = sand_unit[0]
        y = sand_unit[1]

        # down
        if grid[y + 1][x] == '.':
            sand_unit[1] += 1
            continue

        # left
        if grid[y + 1][x - 1] == '.':
            sand_unit[0] -= 1
            sand_unit[1] += 1
            continue

        # right
        if grid[y + 1][x + 1] == '.':
            sand_unit[0] += 1
            sand_unit[1] += 1
            continue

        # next
        grid[y][x] = 'o'
        sand_unit[0] = sand_start[0]
        sand_unit[1] = 0

        count += 1

    #print()
    #print_grid(grid)
        
    return count


if __name__ == "__main__":
    main()
