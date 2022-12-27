from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 1: {}".format(answer_01))
    print("Answer 2: {}".format(answer_02))


def normalize_data(data):
    test = data.pop()
    
    min_x = test[0]
    min_y = test[1]
    min_z = test[2]

    max_x = test[0]
    max_y = test[1]
    max_z = test[2]

    data.add(test)

    for cube in data:
        min_x = min_x if min_x <= cube[0] else cube[0]
        min_y = min_y if min_y <= cube[1] else cube[1]
        min_z = min_z if min_z <= cube[2] else cube[2]

        max_x = max_x if max_x >= cube[0] else cube[0]
        max_y = max_y if max_y >= cube[1] else cube[1]
        max_z = max_z if max_z >= cube[2] else cube[2]

    # so i don't need to worry about bounds checks
    min_x -= 1
    min_y -= 1
    min_z -= 1
        
    x_range = range(min_x, max_x + 2)
    y_range = range(min_y, max_y + 2)
    z_range = range(min_z, max_z + 2)
        
    normalized_data = set()
    for cube in data:
        x, y, z = cube
        normalized_cube = (x - min_x, y - min_y, z - min_z)
        normalized_data.add(normalized_cube)
    
    return normalized_data


def build_space(data):
    test = data.pop()
    
    min_x = test[0]
    min_y = test[1]
    min_z = test[2]

    max_x = test[0]
    max_y = test[1]
    max_z = test[2]

    data.add(test)

    for cube in data:
        min_x = min_x if min_x <= cube[0] else cube[0]
        min_y = min_y if min_y <= cube[1] else cube[1]
        min_z = min_z if min_z <= cube[2] else cube[2]

        max_x = max_x if max_x >= cube[0] else cube[0]
        max_y = max_y if max_y >= cube[1] else cube[1]
        max_z = max_z if max_z >= cube[2] else cube[2]

    # so i don't need to worry about bounds checks
    min_x -= 1
    min_y -= 1
    min_z -= 1
        
    x_range = range(min_x, max_x + 2)
    y_range = range(min_y, max_y + 2)
    z_range = range(min_z, max_z + 2)
        
    space = [[[0 for _ in z_range] for _ in y_range] for _ in x_range]

    normalized_data = set()
    for cube in data:
        x, y, z = cube
        normalized_cube = (x - min_x, y - min_y, z - min_z)
        normalized_data.add(normalized_cube)
    
    for cube in normalized_data:
        x, y, z = cube
        space[x][y][z] = 1
    
    return space


def parse_input():
    data = None

    with open("puzzle_18_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    droplet = set()

    for line in data:
        a =  line.strip().split(',')
        coord = (int(a[0]), int(a[1]), int(a[2]))
        droplet.add(coord)

    return droplet


def part_01(data):
    test = data.pop()
    
    min_x = test[0]
    min_y = test[1]
    min_z = test[2]

    max_x = test[0]
    max_y = test[1]
    max_z = test[2]

    data.add(test)

    for cube in data:
        min_x = min_x if min_x <= cube[0] else cube[0]
        min_y = min_y if min_y <= cube[1] else cube[1]
        min_z = min_z if min_z <= cube[2] else cube[2]

        max_x = max_x if max_x >= cube[0] else cube[0]
        max_y = max_y if max_y >= cube[1] else cube[1]
        max_z = max_z if max_z >= cube[2] else cube[2]

    # so i don't need to worry about bounds checks
    min_x -= 1
    min_y -= 1
    min_z -= 1
        
    x_range = range(min_x, max_x + 2)
    y_range = range(min_y, max_y + 2)
    z_range = range(min_z, max_z + 2)
        
    space = [[[0 for _ in z_range] for _ in y_range] for _ in x_range]

    normalized_data = set()
    for cube in data:
        x, y, z = cube
        normalized_cube = (x - min_x, y - min_y, z - min_z)
        normalized_data.add(normalized_cube)
    
    for cube in normalized_data:
        x, y, z = cube
        space[x][y][z] = 1

    #print(space)

    count = 0

    for cube in normalized_data:
        x, y, z = cube

        up = space[x][y + 1][z]
        dn = space[x][y - 1][z]
        lt = space[x - 1][y][z]
        rt = space[x + 1][y][z]
        nn = space[x][y][z + 1]
        ot = space[x][y][z - 1]

        surface = 6 - sum([up, dn, lt, rt, nn, ot])
        count += surface

    return count


def part_02(data):
    space = build_space(data)

    max_x = len(space) - 1
    max_y = len(space[0]) - 1
    max_z = len(space[0][0]) - 1

    # fill external spaces with -1
    stack = [(0, 0, 0)]

    while stack:
        cur = stack.pop()
        x, y, z = cur
        
        if space[x][y][z] == 0:
            space[x][y][z] = -1

        # add directionals
        if y < max_y and space[x][y + 1][z] == 0:
            stack.append((x, y + 1, z))
            
        if y > 0 and space[x][y - 1][z] == 0:
            stack.append((x, y - 1, z))
            
        if x > 0 and space[x - 1][y][z] == 0:
            stack.append((x - 1, y, z))
            
        if x < max_x and space[x + 1][y][z] == 0:
            stack.append((x + 1, y, z))
            
        if z < max_z and space[x][y][z + 1] == 0:
            stack.append((x, y, z + 1))
            
        if z > 0 and space[x][y][z - 1] == 0:
            stack.append((x, y, z - 1))

        count = 0

    normalized_data = normalize_data(data)
        
    for cube in normalized_data:
        x, y, z = cube

        up = 0 if space[x][y + 1][z] == -1 else 1
        dn = 0 if space[x][y - 1][z] == -1 else 1
        lt = 0 if space[x - 1][y][z] == -1 else 1
        rt = 0 if space[x + 1][y][z] == -1 else 1
        nn = 0 if space[x][y][z + 1] == -1 else 1
        ot = 0 if space[x][y][z - 1] == -1 else 1

        surface = 6 - sum([up, dn, lt, rt, nn, ot])
        count += surface

    return count


if __name__ == "__main__":
    main()
