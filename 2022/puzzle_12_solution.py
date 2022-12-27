from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def print_grid(grid):
    if type(grid[0][0]) == type(" "):
        for row in grid:
            s = ''.join(row)
            print(s)
        return

    for row in grid:
        print(row)

def parse_input():
    data = None

    with open("puzzle_12_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    grid = []
    for line in data:
        line = line.strip()
        row = []
        for c in line:
            row.append(c)
        grid.append(row)

    return grid


def find_start(grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == 'S':
                return (j, i)

    return None


def find_end(grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == 'E':
                return (j, i)

    return None


def find_shortest_path(data, start, end):
    result = None
    
    grid = deepcopy(data)

    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

    # fix-up start and end
    grid[start[1]][start[0]] = 'a'
    grid[end[1]][end[0]] = 'z'
    
    working_grid = [[None for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    working_grid[start[1]][start[0]] = 0

    stack = [start]
    while stack:
        pos = stack.pop(0)

        x = pos[0]
        y = pos[1]

        pos_val = grid[y][x]
        pos_step = working_grid[y][x]

        up = (x, y - 1) if y > 0 else None
        down = (x, y + 1) if y < y_max else None
        left = (x - 1, y) if x > 0 else None
        right = (x + 1, y) if x < x_max else None

        steps = [up, down, left, right]
        for step in steps:
            if step:
                step_x = step[0]
                step_y = step[1]
                step_val = grid[step_y][step_x]
                
                if ord(step_val) <= (ord(pos_val) + 1):
                    cur_step = working_grid[step_y][step_x]
                    if cur_step == None or cur_step > (pos_step + 1):
                        #print("{} -> {}".format(pos_val, step_val))
                        working_grid[step_y][step_x] = pos_step + 1
                        stack.append(step)
        #print_grid(working_grid)
        #s = input()

    #print_grid(working_grid)
    return working_grid[end[1]][end[0]]    
    


def part_01(data):
    result = None
    
    grid = deepcopy(data)
    start = find_start(grid)
    end = find_end(grid)

    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

    # fix-up start and end
    grid[start[1]][start[0]] = 'a'
    grid[end[1]][end[0]] = 'z'
    
    working_grid = [[None for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    working_grid[start[1]][start[0]] = 0

    stack = [start]
    while stack:
        pos = stack.pop(0)

        x = pos[0]
        y = pos[1]

        pos_val = grid[y][x]
        pos_step = working_grid[y][x]

        up = (x, y - 1) if y > 0 else None
        down = (x, y + 1) if y < y_max else None
        left = (x - 1, y) if x > 0 else None
        right = (x + 1, y) if x < x_max else None

        steps = [up, down, left, right]
        for step in steps:
            if step:
                step_x = step[0]
                step_y = step[1]
                step_val = grid[step_y][step_x]
                
                if ord(step_val) <= (ord(pos_val) + 1):
                    cur_step = working_grid[step_y][step_x]
                    if cur_step == None or cur_step > (pos_step + 1):
                        #print("{} -> {}".format(pos_val, step_val))
                        working_grid[step_y][step_x] = pos_step + 1
                        stack.append(step)
        #print_grid(working_grid)
        #s = input()

    #print_grid(working_grid)
    return working_grid[end[1]][end[0]]    
    
    '''
    def part_01_recurse(pos, visited):
        result = None
        
        new_visited = visited.copy()
        new_visited.add(pos)

        if pos == end:
            return len(new_visited)

        x = pos[0]
        y = pos[1]
        pos_val = grid[pos[1]][pos[0]]

        # Start special case
        if pos == start:
            pos_val = 'a'

        up = (x, y - 1) if y > 0 else None
        down = (x, y + 1) if y < y_max else None
        left = (x - 1, y) if x > 0 else None
        right = (x + 1, y) if x < x_max else None

        steps = [up, down, left, right]
        for step in steps:
            if step and step not in visited:
                step_x = step[0]
                step_y = step[1]
                step_val = grid[step_y][step_x]
                #print("{} -> {}".format(pos_val, step_val))
                if ord(step_val) <= (ord(pos_val) + 1):
                    option = part_01_recurse(step, visited)
                    result = option if result == None or option < result else result

        return result
    '''

    result = part_01_recurse(start, set())

    return result

def part_02(data):
    start = find_start(data)
    end = find_end(data)

    result = find_shortest_path(data, start, end)
    starts = []
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == 'a':
                start = (j, i)
                starts.append(start)

    for start in starts:
        option = find_shortest_path(data, start, end)
        if option and option < result:
            result = option

    return result



if __name__ == "__main__":
    main()
