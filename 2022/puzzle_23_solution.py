from copy import deepcopy


def main():
    data = parse_input()

    answer_01 = part_01(data)
    print("Answer 01: {}".format(answer_01))

    answer_02 = part_02(data)
    print("Answer 02: {}".format(answer_02))



def parse_input():
    data = None

    with open("puzzle_23_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    elves = []
    for line in data:
        line = line.strip()
        row = list(line)
        elves.append(row)
    
    return elves


def print_grid(grid):
    for row in grid:
        print(''.join(row))


def add(A1, A2):
    return list(map(lambda x, y: x + y, A1, A2))
        

# mutates grid
def step(elves, directions):
    N_MASK = [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    S_MASK = [[0, 0, 0], [0, 0, 0], [1, 1, 1]]
    W_MASK = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
    E_MASK = [[0, 0, 1], [0, 0, 1], [0, 0, 1]]

    N = [0, -1]
    S = [0, 1]
    W = [-1, 0]
    E = [1, 0]

    DIR_MASKS = {'N': N_MASK,
                 'S': S_MASK,
                 'W': W_MASK,
                 'E': E_MASK
                 }

    DIR_STEPS = {'N': N,
                 'S': S,
                 'W': W,
                 'E': E}

    
    def grid(x, y):
        key = (x, y)
        if key in elves:
            return '#'
        return '.'
    
    
    def check_direction(pos, d):
        mask = DIR_MASKS[d]
        start_x = pos[0] - 1
        start_y = pos[1] - 1

        for i in range(3):
            for j in range(3):
                grid_x = start_x + j
                grid_y = start_y + i
                
                if mask[i][j] == 1 and grid(grid_x, grid_y) == '#':
                    return False
        return True
    
    
    def get_proposal(pos):
        proposal = pos
        options = []
        
        for d in directions:
            if check_direction(pos, d):
                proposal = add(pos, DIR_STEPS[d])
                options.append(tuple(proposal))

        if len(options) == 4 or len(options) == 0:
            return tuple(pos)
        
        return tuple(options[0])

    
    def move_elf(cur_pos, new_pos):
        cur_x = cur_pos[0]
        cur_y = cur_pos[1]

        new_x = new_pos[0]
        new_y = new_pos[1]

        '''
        # Not sure about this (a move out of bounds was not
        # addressed in the problem description)
        # CORRECTION - it says the area is infinite!
        if new_x < 0 or new_x > len(grid[0]) or \
           new_y < 0 or new_y > len(grid):
            return
        '''
        
        del elves[(cur_x, cur_y)]
        elves[(new_x, new_y)] = '#'
            
    # PROPOSALS
    proposals = {}

    for elf in elves:
        pos = list(elf)
        prop = get_proposal(pos)

        if prop in proposals:
            proposals[prop].append(pos)
        else:
            proposals[prop] = [pos]

    # MOVES
    for prop in proposals:
        if len(proposals[prop]) > 1:
            continue

        elf = proposals[prop][0]
        move_elf(elf, list(prop))

    # UPDATE START DIRECTION
    next_directions = directions[1:] + [directions[0]]
    return next_directions

        
def part_01(data):
    elves = {}
    directions = ['N', 'S', 'W', 'E']

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                elves[(x, y)] = '#'

    #print_elves(elves)
                
    #print(directions)
    #print_grid(elves)
    #print()

    count = 10
    for i in range(count):
        directions = step(elves, directions)
        #print_elves(elves)
        #print(directions)
        #print_grid(elves)
        #print()

    # calc score
    bounds = get_bounds(elves)
    min_x = bounds[0][0]
    min_y = bounds[0][1]
    max_x = bounds[1][0]
    max_y = bounds[1][1]

    score = (max_x - min_x + 1) * (max_y - min_y + 1)
    score -= len(elves)
    
    return score


def get_bounds(elves):
    first_elf = list(elves.keys())[0]
    min_x = first_elf[0]
    max_x = min_x
    min_y = first_elf[1]
    max_y = min_y

    for elf in elves:
        x = elf[0]
        y = elf[1]
        
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    return ((min_x, min_y), (max_x, max_y))


def print_elves(elves):
    bounds = get_bounds(elves)
    for y in range(bounds[0][1], bounds[1][1] + 1):
        scan_row = ""
        for x in range(bounds[0][0], bounds[1][0] + 1):
            if (x, y) in elves:
                scan_row += '#'
            else:
                scan_row += '.'

        print(scan_row)

    print()

def part_02(data):
    elves = {}
    directions = ['N', 'S', 'W', 'E']
    
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                elves[(x, y)] = '#'

    round = 0
    round_start_state = None

    while round_start_state != elves:
        round += 1
        round_start_state = elves.copy()
        directions = step(elves, directions)
        
    return round




if __name__ == "__main__":
    main()
