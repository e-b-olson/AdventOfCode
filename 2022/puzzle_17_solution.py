from copy import deepcopy

def main():

    s0 = [[1, 1, 1, 1]]
    s1 = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    s2 = [[1, 1, 1], [0, 0, 1], [0, 0, 1]]
    s3 = [[1], [1], [1], [1]]
    s4 = [[1, 1], [1, 1]]

    shapes = [s0, s1, s2, s3, s4]

    wind = parse_input()

    answer_01 = part_01(shapes, wind)
    answer_02 = part_02(shapes, wind)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None

    with open("puzzle_17_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    winds = []
    for line in data:
        line = line.strip()
        if not line:
            continue

        for c in line:
            if c == "<":
                winds.append(-1)

            if c == ">":
                winds.append(1)
    
    return winds


def print_chamber(chamber, top):
    for y in range(top + 7, -1, -1):
        s = ""
        for x in range(7):
            s += ' ' if (x, y) not in chamber else '#'

        print(s)
    print("----------")


def part_01(shapes, winds, max_count=2022):
    bottom = 0
    top = 0
    left = 0
    right = 6
    
    shape_index = 0
    wind_step = 0

    #max_count = 2022
    
    chamber = set()
    for i in range(7):
        chamber.add((i, -1))
    
    for count in range(max_count):
        shape = deepcopy(shapes[shape_index])
        shape_index = (shape_index + 1) % 5

        start_x = left + 2
        start_y = top + 3
        
        coords = []
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x]:
                    coord = [start_x + x, start_y + y]
                    coords.append(coord)

        '''
        for y in range(7):
            s = ""
            for x in range(7):
                s += ' ' if [x, y] not in coords else '#'

            print(s)

        print()
        '''

        # simulate
        prev_coords_set = set()
        coords_set = set()
        for coord in coords:
            coords_set.add(tuple(coord))

        step = 0
        while not coords_set.intersection(chamber):
            next_coords = set()
            
            if step % 2:
                # move down    
                for coord in coords_set:
                    next_coords.add((coord[0], coord[1] - 1))

            else: 
                # move wind
                wind = winds[wind_step]
                adjustment = 0
                for coord in coords_set:
                    x = coord[0] + wind
                    if x > 6:
                        adjustment = min(adjustment, 6 - x)

                    if x < 0:
                        adjustment = max(adjustment, 0 - x)
                    next_coords.add((x, coord[1]))

                if adjustment:
                    adjusted_coords = set()
                    for coord in next_coords:
                        adjusted_coords.add((coord[0] + adjustment, coord[1]))

                    next_coords = adjusted_coords

                wind_step = (wind_step + 1) % len(winds)

            prev_coords_set = coords_set
            coords_set = next_coords

            # only stop on downward step
            if step % 2 == 0 and coords_set.intersection(chamber):
                coords_set = prev_coords_set
            
            step += 1

            #next_chamber = chamber.copy()
            #next_chamber = next_chamber.union(prev_coords_set)
            #print_chamber(next_chamber, top)

        chamber = chamber.union(prev_coords_set)

        # get the top
        for coord in prev_coords_set:
            if coord[1] + 1 > top:
                top = coord[1] + 1
        

        #print_chamber(chamber, top)

    return top
        
def part_02(shapes, winds):
    #return part_01(shapes, winds, 1000000000000)

    bottom = 0
    top = 0
    left = 0
    right = 6
    
    shape_index = 0
    wind_step = 0

    rejected_patterns = set()
    best_pattern_start = None
    best_pattern_len = None
    
    max_count = 1000000000000
    
    chamber = set()
    for i in range(7):
        chamber.add((i, -1))

    dp = [0]
    top_deltas = []
        
    for count in range(max_count):

        # build current shape
        shape = deepcopy(shapes[shape_index])
        shape_index = (shape_index + 1) % 5

        start_x = left + 2
        start_y = top + 3
        
        coords = []
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if shape[y][x]:
                    coord = [start_x + x, start_y + y]
                    coords.append(coord)

        # simulate
        prev_coords_set = set()
        coords_set = set()
        for coord in coords:
            coords_set.add(tuple(coord))

        step = 0
        while not coords_set.intersection(chamber):
            next_coords = set()
            
            if step % 2:
                # move down    
                for coord in coords_set:
                    next_coords.add((coord[0], coord[1] - 1))

            else: 
                # move wind
                wind = winds[wind_step]
                adjustment = 0
                for coord in coords_set:
                    x = coord[0] + wind
                    if x > 6:
                        adjustment = min(adjustment, 6 - x)

                    if x < 0:
                        adjustment = max(adjustment, 0 - x)
                    next_coords.add((x, coord[1]))

                if adjustment:
                    adjusted_coords = set()
                    for coord in next_coords:
                        adjusted_coords.add((coord[0] + adjustment, coord[1]))

                    next_coords = adjusted_coords

                wind_step = (wind_step + 1) % len(winds)

            prev_coords_set = coords_set
            coords_set = next_coords

            # only stop on downward step
            if step % 2 == 0 and coords_set.intersection(chamber):
                coords_set = prev_coords_set
            
            step += 1

            #next_chamber = chamber.copy()
            #next_chamber = next_chamber.union(prev_coords_set)
            #print_chamber(next_chamber, top)

        chamber = chamber.union(prev_coords_set)

        # get the top
        for coord in prev_coords_set:
            if coord[1] + 1 > top:
                top = coord[1] + 1
        

        # check for total blockage
        '''
        y_vals = set()
        for coord in prev_coords_set:
            y_vals.add(coord[1])

        for y in y_vals:
            total_blockage = True
            for x in range(7):
                if (x, y) not in chamber:
                    total_blockage = False
                    break

            if total_blockage:
                # clear out everything below!
                remove_set = set()
                for coord in chamber:
                    if coord[1] < y:
                        remove_set.add(coord)

                print("clearing")
                before = len(chamber)
                chamber = chamber.remove(remove_set)
                after = len(chamber)
                print("({} -> {})".format(before, after))
        '''

        top_deltas.append(top - dp[-1])
        dp.append(top)
        
        pattern_start, pattern_len = find_pattern(top_deltas, rejected_patterns)
        if pattern_start and pattern_len:
            if best_pattern_start != pattern_start or \
               best_pattern_len != pattern_len:
                best_pattern_start = pattern_start
                best_pattern_len = pattern_len
                print("Pattern: {} ({})".format(best_pattern_start, best_pattern_len))
                # ^^^ using this, I was able to see the pattern starts at
                # rock 15 and repeats every 35 rocks SO...

                bottom_rocks = dp[pattern_start]
                unit_height = dp[pattern_start + pattern_len] - bottom_rocks
                unit_count = (max_count - pattern_start) // pattern_len
                top_rocks_count = (max_count - pattern_start) % pattern_len
                top_rocks = dp[pattern_start + top_rocks_count] - bottom_rocks

                total = bottom_rocks + top_rocks + (unit_count * unit_height)
                return total

        # check for stackable unit
        if wind_step == 0 and shape_index == 0:
            unit_size = len(dp)
            unit_top = dp[-1]

            unit_count = 1000000000000 // unit_size
            partial_unit = 1000000000000 % unit_size

            total = unit_count * unit_size
            total += dp[partial_unit]

            return total
                
        #print_chamber(chamber, top)

    return top


def find_pattern(data, rejected_patterns):
    pattern_start = None
    pattern_size = None
    
    max_size = len(data) // 2
    for size in range(12, max_size + 1):
        if data[-size:] != data[-(2*size):-size]:
            continue
        
        for start in range(len(data) - size):
            #if (start, size) in rejected_patterns:
            #    break
            
            if data[start:start+size] == data[start+size: start+size+size]:
                if pattern_size == None or pattern_size < size:
                    pattern_start = start
                    pattern_size = size
            #else:
            #    rejected_patterns.add((start, size))

    return pattern_start, pattern_size


    
    possible_patterns = {}
    
    max_size = len(data) // 2
    for size in range(2, max_size + 1):
        dp = set()
        for start in range(0, len(data) - size):
            window = str(data[start:start+size])
            if window in dp:
                if window in possible_patterns:
                    possible_patterns[window].append((start, size))
                else:
                    possible_patterns[window] = [(start, size)]
            else:
                dp.add(window)

    pattern_start = None
    pattern_len = None
    
    patterns = []
    for pattern in possible_patterns:
        possible_pattern = True
        
        starts = possible_patterns[pattern]
        if len(starts) < 2:
            continue

        delta = starts[1][0] - starts[0][0]
        for i in range(len(starts)):
            if starts[i][0] - starts[i-1][0] != delta:
                possible_pattern = False
                break

        if delta != starts[0][1]:
            possible_pattern = False

        if possible_pattern:
            patterns.append(starts[0])


        sorted_patterns = sorted(patterns, key=lambda x: -x[1])

        pattern_start = sorted_patterns[0][0] if sorted_patterns else None
        pattern_len = sorted_patterns[0][1] if sorted_patterns else None
                
    return pattern_start, pattern_len


if __name__ == "__main__":
    main()
