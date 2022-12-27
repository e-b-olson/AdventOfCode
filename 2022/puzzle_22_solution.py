from copy import deepcopy

DEBUG = True

def debug_print(*args):
    if DEBUG:
        print(*args)


def main():
    data = parse_input()

    answer_01 = part_01(data)
    print("Answer 01: {}".format(answer_01))

    answer_02 = part_02(data)
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None

    with open("puzzle_22_input.txt", "r") as f:
        data = f.readlines()
    f.close()

    diagram = []
    directions = None

    get_directions = False
    for line in data:
        line = line.replace('\n' ,'')

        if not line:
            get_directions = True
            continue
        
        if not get_directions:
            row = list(line)
            diagram.append(row)
        else:
            directions = line

    # parse directions
    path = []
    steps = ""
    for c in line:
        if c in "0123456789":
            steps += c
            continue
        if c in "RL":
            path.append(int(steps))
            path.append(c)
            steps = ""

    if steps:
        path.append(int(steps))

    data = (diagram, path)

    # Fixup Gaps (IMPORTANT)
    max_x = 0
    for row in diagram:
        max_x = max(max_x, len(row))

    for row in diagram:
        row += [' ' for _ in range(max_x - len(row))]
    
    # TEST INPUT PARSING
    x_count = len(diagram[0])
    y_count = len(diagram)

    for i, row in enumerate(diagram):
        if len(row) != x_count:
            print("ERROR ({}): Expected {}, got {}.".format(i, x_count, len(row)))
            return None
  
    return data

def add(A1, A2):
    return list(map(lambda x, y: x + y, A1, A2))


def delta_for_facing(facing):
    R = 0
    D = 1
    L = 2
    U = 3

    delta = [0, 0]
    if facing == R:
        delta = [1, 0]

    if facing == L:
        delta = [-1, 0]

    if facing == U:
        delta = [0, -1]

    if facing == D:
        delta = [0, 1]

    return delta


def teleport_01(pos, delta, diagram):
    x_count = len(diagram[0])
    y_count = len(diagram)

    next_pos = add(pos, delta)

    next_pos[0] = next_pos[0] % x_count
    next_pos[1] = next_pos[1] % y_count
    x = next_pos[0]
    y = next_pos[1]

    # find the next legit spot
    #print("START ----> {} ({})".format([x, y], [x_count, y_count]))
    while diagram[y][x] == ' ':
        next_pos = add(next_pos, delta)
        next_pos[0] = next_pos[0] % x_count
        next_pos[1] = next_pos[1] % y_count
        x = next_pos[0] % x_count
        y = next_pos[1] % y_count
        #print("----> {}".format([x, y]))

    x = x % x_count
    y = y % y_count
    next_pos[0] = x
    next_pos[1] = y
    
    return next_pos


# Part 1 or Part 2
def sim(pos, facing, step, diagram, part = 1):
    R = 0
    D = 1
    L = 2
    U = 3

    S = '.'
    W = '#'

    x_count = len(diagram[0])
    y_count = len(diagram)
    
    if step == 'R':
        facing = (facing + 1) % 4
        return pos, facing

    if step == 'L':
        facing = (facing - 1) % 4
        return pos, facing

    delta = delta_for_facing(facing)
    
    count = step
    done = False
    while count > 0 and not done:
        next_pos = add(pos, delta)
        next_facing = facing
        next_delta = delta
        
        #print("STEP: {} + {} --> {}".format(pos, delta, next_pos))
        count -= 1

        # check for collisions and wrapping
        next_pos[0] = next_pos[0] % x_count
        next_pos[1] = next_pos[1] % y_count
        x = next_pos[0]
        y = next_pos[1]

        # find the next legit spot
        #print("START ----> {} ({})".format([x, y], [x_count, y_count]))
        if diagram[y][x] == ' ':
            if part == 1:
                next_pos = teleport_01(pos, delta, diagram)
            if part == 2:
                next_pos, next_facing, next_delta = teleport_02(pos, delta, diagram)
                #print("TELEPORT")
                #print("{} ({} {}) --> {} ({} {})".format(pos, facing, delta, next_pos, next_facing, next_delta))

        x = next_pos[0] % x_count
        y = next_pos[1] % y_count
            
        if diagram[y][x] == '.':
            pos = [x, y]
            facing = next_facing
            delta = next_delta
            continue

        if diagram[y][x] == '#':
            done = True
            continue

    return pos, facing


def part_01(data):
    diagram = data[0]
    path = data[1]

    print("Map: {}".format([len(diagram[0]), len(diagram)]))
    
    '''
    for row in diagram:
        print(row)

    print(path)
    '''

    R = 0
    D = 1
    L = 2
    U = 3

    S = '.'
    W = '#'
    
    pos = [0, 0]
    facing = R

    # find start
    for i, x in enumerate(diagram[0]):
        if x == S:
            pos = [i, 0]
            break

    print("Start: {}".format(pos))

    # follow path
    for step in path:
        #print("START: {} ({})".format(pos, facing))
        pos, facing = sim(pos, facing, step, diagram)
        #print("END: {} ({})".format(pos, facing))

    row = pos[1] + 1
    col = pos[0] + 1
    result = (1000 * row) + (4 * col) + facing
    #print("1000 * {} + 4 * {} + {} ".format(row, col, facing))
    return result

#DEBUG
tele = set()

def teleport_02(pos, delta, diagram):
    R = 0
    D = 1
    L = 2
    U = 3

    x_count = len(diagram[0])
    y_count = len(diagram)

    next_pos = add(pos, delta)
    next_pos[0] = next_pos[0] % x_count
    next_pos[1] = next_pos[1] % y_count

    x = next_pos[0]
    y = next_pos[1]

    # DEBUG
    global tele
    side = None
    ds = None
    
    '''
    DIAGRAM

          _A_ _B_
        E|   |   |   
         |___|___|D
        F|   | C
      _F_|___|C
    E|   |   |
     |___|___|D
    A|   | G
     |___|G
       B
    '''
    
    next_facing = None
    next_x = None
    next_y = None

    # STEP RIGHT
    if delta == [1, 0]:
        next_facing = R
        if x == 0:                  # <-- D
            next_facing = L
            next_x = 99
            next_y = 149 - y
            
            side = 'D'
            ds = tuple(delta)

        if x >= 100 and y < 100:    # <-- C
            next_facing = U
            next_x = 50 + y
            next_y = 49

            side = 'C'
            ds = tuple(delta)

        if x >= 100 and y >= 100:   # <-- D
            next_facing = L
            next_x = 149
            next_y = 149 - y

            side = 'D'
            ds = tuple(delta)

        if x >= 50 and x < 100:     # <-- G
            next_facing = U
            next_x = 100 - (200 - y)
            next_y = 149

            side = 'G'
            ds = tuple(delta)

    # STEP LEFT
    if delta == [-1, 0]:
        next_facing = L
        if x > 50 and y < 150:      # <-- E
            next_facing = R
            next_x = 50
            next_y = 49 - (y - 100)

            side = 'E'
            ds = tuple(delta)
            
        if x > 50 and y >= 150:     # <-- A
            next_facing = D
            next_x = 50 + (y - 150)
            next_y = 0

            side = 'A'
            ds = tuple(delta)
            
        if x < 50 and y < 50:       # <-- E
            next_facing = R
            next_x = 0
            next_y = 149 - y

            side = 'E'
            ds = tuple(delta)

        if x < 50 and y >= 50:      # <-- F
            next_facing = D
            next_x = y - 50
            next_y = 100

            side = 'F'
            ds = tuple(delta)

    # STEP DOWN
    if delta == [0, 1]:
        next_facing = D
        if x < 50:                  # <-- B
            next_y = 0
            next_x = 100 + x

            side = 'B'
            ds = tuple(delta)

        if x >= 50 and x < 100:     # <-- G
            next_facing = L
            next_y = 150 + (x - 50)
            next_x = 49

            side = 'G'
            ds = tuple(delta)

        if x >= 100:                # <-- C
            next_facing = L
            next_y = 50 + (x - 100)
            next_x = 99

            side = 'C'
            ds = tuple(delta)

    # STEP UP
    if delta == [0, -1]:
        next_facing = U
        if x < 50:                  # <-- F
            next_facing = R
            next_y = 50 + x
            next_x = 50

            side = 'F'
            ds = tuple(delta)

        if x >= 50 and x < 100:     # <-- A
            next_facing = R
            next_y = 150 + (x - 50)
            next_x = 0

            side = 'A'
            ds = tuple(delta)

        if x >= 100:                # <-- B
            next_y = 199
            next_x = x - 100

            side = 'B'
            ds = tuple(delta)

    # new delta?
    next_delta = delta_for_facing(next_facing)    
    next_pos = [next_x, next_y]

    # DEBUG
    t = (side, ds)
    if t not in tele:
        tele.add(t)
        print("TELEPORT")
        print("{}: {} ({}) --> {} ({})".format(side, pos, delta, next_pos, next_delta))
        
    return next_pos, next_facing, next_delta


def part_02(data):
    diagram = data[0]
    path = data[1]

    R = 0
    D = 1
    L = 2
    U = 3

    S = '.'

    pos = [0, 0]
    facing = R

    # find start
    for i, x in enumerate(diagram[0]):
        if x == S:
            pos = [i, 0]
            break

    print("Start: {}".format(pos))

    # follow path
    for step in path:
        #print("START: {} ({})".format(pos, facing))
        pos, facing = sim(pos, facing, step, diagram, 2)
        #print("END: {} ({})".format(pos, facing))

    row = pos[1] + 1
    col = pos[0] + 1
    result = (1000 * row) + (4 * col) + facing
    #print("1000 * {} + 4 * {} + {} ".format(row, col, facing))
    return result


if __name__ == "__main__":
    main()
