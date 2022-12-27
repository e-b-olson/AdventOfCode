from copy import deepcopy
from datetime import datetime

def main():
    data = parse_input()

    print_time()
    answer_01 = part_01(data)
    print("Answer 01: {}".format(answer_01))

    print_time()
    answer_02 = part_02(data)
    print("Answer 02: {}".format(answer_02))
    print_time()


def print_time():
    now = datetime.now()
    now_string = now.strftime("%H:%M:%S")
    print("Time: ", now_string)
    

def parse_input():
    data = None

    with open("puzzle_24_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    blizzards = []
    start = None
    end = None
    
    for line in data:
        line = line.strip()
        row = []
        for c in line:
            row.append(c)
        blizzards.append(row)

            
    for y, row in enumerate(blizzards):
        for x, c in enumerate(row):
            if y == 0 and c == '.':
                start = (x, y)

            if y == len(data) - 1 and c == '.':
                end = (x, y)

    return (start, end, blizzards)


def print_grid(grid):
    for row in grid:
        print(''.join(row))

    print()


def print_blizzards(blizzards, max_x, max_y, pos=None):
    grid = [['.' for _ in range(max_x + 2)] for _ in range(max_y + 2)]

    if pos:
        grid[pos[1]][pos[0]] = 'E'
    
    for b in blizzards:
        x = b[0]
        y = b[1]
        b_list = blizzards[b]
        if len(b_list) > 1:
            grid[y][x] = str(len(b_list))
        else:
            grid[y][x] = b_list[0]

    print_grid(grid)


# HACK
blizzard_cache = {}
    
def blizzards_for_minute(m, blizzards, min_x, min_y, max_x, max_y):
    if m in blizzard_cache:
        return blizzard_cache[m]

    def add_to_next_blizzards(nb, coord, b):
        if coord in nb:
            nb[coord].append(b)
        else:
            nb[coord] = [b]

    prev_blizzards = blizzard_cache[m - 1] if m - 1 in blizzard_cache else blizzards
            
    next_blizzards = {}
    for coord in prev_blizzards:
        for b in prev_blizzards[coord]:
            x = coord[0]
            y = coord[1]
            
            if b == '^':
                next_y = (y - 1) if y > min_y else max_y
                add_to_next_blizzards(next_blizzards, (x, next_y), b) 
            if b == 'v':
                next_y = (y + 1) if y < max_y else min_y
                add_to_next_blizzards(next_blizzards, (x, next_y), b) 
            if b == '<':
                next_x = (x - 1) if x > min_x else max_x
                add_to_next_blizzards(next_blizzards, (next_x, y), b) 
            if b == '>':
                next_x = (x + 1) if x < max_x else min_x
                add_to_next_blizzards(next_blizzards, (next_x, y), b)

            if b == '#':
                add_to_next_blizzards(next_blizzards, (x, y), b) 

    blizzard_cache[m] = next_blizzards    
    return next_blizzards


seen_states = set()
def seen_state(pos, state, target = None):
    state_string = str(pos) + str(state)
    if target:
        state_string += str(target)
        
    if state_string in seen_states:
        return True
    return False


def record_state(pos, state, target = None):
    state_string = str(pos) + str(state)
    if target:
        state_string += str(target)
    seen_states.add(state_string)


def sim_part_01(blizzards, start, end, min_x, min_y, max_x, max_y):
    pos = start

    result = None
    stack = [(pos, 1)] #<-- need to look into the future!

    #count = 0

    # keep track of states (to avoid cycles)
    seen_states = set()
    
    while stack:
        state = stack.pop(0)
        
        # DEBUG
        '''
        count += 1
        if count > 10:
            break
        '''

        cur_pos = state[0]
        cur_time = state[1]
        
        if cur_pos == end:
            result = cur_time if result == None else min(result, cur_time)
            print("Complete: {}".format(cur_time))
            continue

        bliz_state = blizzards_for_minute(cur_time, blizzards, \
                                          min_x, min_y, max_x, max_y)


        if seen_state(cur_pos, bliz_state):
            continue
        record_state(cur_pos, bliz_state)

        # DEBUG
        '''
        if cur_time > 16 and cur_time < 19:
            print("STEP {}".format(cur_time))
            prev_state = blizzards_for_minute(cur_time - 1, blizzards, \
                                              min_x, min_y, max_x, max_y)
            print_blizzards(prev_state, max_x, max_y, cur_pos)
        '''
        
        # DEBUG
        #if cur_time >= 19:
        #    continue
        
        # OPTIONS
        x = cur_pos[0]
        y = cur_pos[1]
        
        wt = cur_pos
        up = (x, y - 1) if y > min_y else None 
        dn = (x, y + 1) if y <= max_y else None # <-- need <= for END point
        lt = (x - 1, y) if x >= min_x else None
        rt = (x + 1, y) if x <= max_x else None
        options = [up, dn, lt, rt, wt]

        # only wait if there are no other options
        if up == None and dn == None and lt == None and rt == None:
            options = [wt]

        do_not_wait = False
        
        for option in options:
            if option != None and option not in bliz_state:
                if option == wt and do_not_wait and False:
                    continue

                # don't wait, if we have other options
                do_not_wait = True

                # only push BETTER options
                if result and result < cur_time:
                    continue
                
                option_state = (option, cur_time + 1)
                stack.append(option_state)

                
    return result - 1
            

    
def part_01(data):
    start, end, grid = data
    print("Start: {}".format(start))
    print("End: {}".format(end))
    #print_grid(grid)

    min_x = 1
    max_x = len(grid[0]) - 2
    min_y = 1
    max_y = len(grid) - 2
    
    blizzards = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in "<>^v#":
                coord = (x, y)
                blizzards[coord] = [grid[y][x]]

    #print_blizzards(blizzards, max_x, max_y)

    # SIM
    '''
    for m in range(5):
        next_b = blizzards_for_minute(m, blizzards, min_x, min_y, max_x, max_y)
        print_blizzards(next_b, max_x, max_y)
    '''

    steps = sim_part_01(blizzards, start, end, min_x, min_y, max_x, max_y)

    return steps



def local_seen_state(state_set, pos, state, target = None):
    state_string = str(pos) + str(state)
    if target:
        state_string += str(target)
        
    if state_string in state_set:
        return True
    return False


def local_record_state(state_set, pos, state, target = None):
    state_string = str(pos) + str(state)
    if target:
        state_string += str(target)
    state_set.add(state_string)




def sim_part_02(blizzards, start, end, start_time, min_x, min_y, max_x, max_y):
    pos = start

    result = None
    stack = [(pos, start_time)] #<-- need to look into the future!

    #count = 0

    # keep track of states (to avoid cycles)
    seen_states = set()

    while stack:
        state = stack.pop(0)
        
        # DEBUG
        '''
        count += 1
        if count > 10:
            break
        '''

        cur_pos = state[0]
        cur_time = state[1]
        
        if cur_pos == end:
            result = cur_time if result == None else min(result, cur_time)
            continue

        bliz_state = blizzards_for_minute(cur_time, blizzards, \
                                          min_x, min_y, max_x, max_y)


        if local_seen_state(seen_states, cur_pos, bliz_state, end):
            #if cur_time > 19:
            #    print("Seen State: {} {}".format(cur_pos, phases[phase][1])) 
            continue
        local_record_state(seen_states, cur_pos, bliz_state, end)
        
        # DEBUG
        '''
        if cur_time > 20 and cur_time < 22:
            print("STEP {}".format(cur_time))
            prev_state = blizzards_for_minute(cur_time - 1, blizzards, \
                                              min_x, min_y, max_x, max_y)
            print_blizzards(prev_state, max_x, max_y, cur_pos)
        '''
        
        # DEBUG
        #if cur_time >= 19:
        #    continue
        
        # OPTIONS
        x = cur_pos[0]
        y = cur_pos[1]
        
        wt = cur_pos
        up = (x, y - 1) if y >= min_y else None 
        dn = (x, y + 1) if y <= max_y else None # <-- need <= for END point
        lt = (x - 1, y) if x >= min_x else None
        rt = (x + 1, y) if x <= max_x else None
        options = [up, dn, lt, rt, wt]

        for option in options:
            if option != None and option not in bliz_state:

                # only push BETTER options
                if result and result < cur_time:
                    continue

                # DEBUG HACK
                #if cur_time > 58:
                #    continue
                
                option_state = (option, cur_time + 1)
                stack.append(option_state)

                
    return result - 1 if result != None else None




def sim_part_02_old(blizzards, start, end, min_x, min_y, max_x, max_y):
    pos = start

    result = None
    stack = [(pos, 1)] #<-- need to look into the future!

    #count = 0

    # keep track of states (to avoid cycles)
    seen_states = set()


    phase_01 = [start, end]
    phase_02 = [end, start]
    phase_03 = [start, end]

    phases = [phase_01, phase_02, phase_03]
    phase_results = [set(), set(), set()]
    phase = 0
    phases = [phase_01, phase_02, phase_03]
        
    while stack or phase < len(phases) - 1:
        if not stack:
            phase += 1
            phase_data = phases[phase]
            start_pos = phase_data[0]
            stack = []
            result = None
            seen_states = set()
            
            for phase_result in phase_results[phase - 1]:
                start_time = phase_result - 1
                option = (start_pos, start_time)
                stack.append(option)

            print("STARTING PHASE {}".format(phase))
            print("Stack: {}".format(stack))

        search_type = 0 if phase == 0 else 0
        state = stack.pop(search_type)
        
        # DEBUG
        '''
        count += 1
        if count > 10:
            break
        '''

        cur_pos = state[0]
        cur_time = state[1]
        
        if cur_pos == phases[phase][1]:
            result = cur_time if result == None else min(result, cur_time)

            if cur_time not in phase_results[phase]:
                print("Phase {} Complete: {}".format(phase, cur_time))
                phase_results[phase].add(cur_time)
            
            continue

        bliz_state = blizzards_for_minute(cur_time, blizzards, \
                                          min_x, min_y, max_x, max_y)


        if seen_state(cur_pos, bliz_state, phases[phase][1]):
            #if cur_time > 19:
            #    print("Seen State: {} {}".format(cur_pos, phases[phase][1])) 
            continue
        record_state(cur_pos, bliz_state, phases[phase][1])
        
        # DEBUG
        '''
        if cur_time > 19 and cur_time < 21:
            print("STEP {}".format(cur_time))
            prev_state = blizzards_for_minute(cur_time - 1, blizzards, \
                                              min_x, min_y, max_x, max_y)
            print_blizzards(prev_state, max_x, max_y, cur_pos)
        '''
        
        # DEBUG
        #if cur_time >= 19:
        #    continue
        
        # OPTIONS
        x = cur_pos[0]
        y = cur_pos[1]
        
        wt = cur_pos
        up = (x, y - 1) if y > min_y else None 
        dn = (x, y + 1) if y <= max_y else None # <-- need <= for END point
        lt = (x - 1, y) if x >= min_x else None
        rt = (x + 1, y) if x <= max_x else None
        options = [up, dn, lt, rt, wt]

        # only wait if there are no other options
        if up == None and dn == None and lt == None and rt == None:
            options = [wt]

        do_not_wait = False
        
        for option in options:
            if option != None and option not in bliz_state:
                if option == wt and do_not_wait and False:
                    continue

                # don't wait, if we have other options
                do_not_wait = True

                # THIS WON'T WORK FOR PART TWO
                # only push BETTER options
                if result and result < cur_time - 57:
                    continue

                # DEBUG HACK
                if cur_time > 57:
                    continue
                
                option_state = (option, cur_time + 1)
                stack.append(option_state)

                
    return min(phase_results[-1])




    
def part_02(data):
    start, end, grid = data
    print("Start: {}".format(start))
    print("End: {}".format(end))
    #print_grid(grid)

    min_x = 1
    max_x = len(grid[0]) - 2
    min_y = 1
    max_y = len(grid) - 2
    
    blizzards = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in "<>^v#":
                coord = (x, y)
                blizzards[coord] = [grid[y][x]]

    #print_blizzards(blizzards, max_x, max_y)

    # SIM
    '''
    for m in range(5):
        next_b = blizzards_for_minute(m, blizzards, min_x, min_y, max_x, max_y)
        print_blizzards(next_b, max_x, max_y)
    '''

    steps = sim_part_02(blizzards, start, end, 1, min_x, min_y, max_x, max_y)
    steps = sim_part_02(blizzards, end, start, steps, min_x, min_y, max_x, max_y)
    steps = sim_part_02(blizzards, start, end, steps, min_x, min_y, max_x, max_y)

    return steps



if __name__ == "__main__":
    main()

