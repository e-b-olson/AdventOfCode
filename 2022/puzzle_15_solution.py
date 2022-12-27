from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))



def parse_input():
    data = None

    with open("puzzle_15_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    sensors = []
    for line in data:
        line = line.strip()
        line = line.split(' ')
        sx = int(line[2].replace(',','').split('=')[1])
        sy = int(line[3].replace(':', '').split('=')[1])
        bx = int(line[8].replace(',','').split('=')[1])
        by = int(line[9].split('=')[1])

        sensor = (sx, sy, bx, by)
        sensors.append(sensor)
        
    return sensors



def part_01(data):
    #for sensor in data:
    #    print(sensor)

    beacons = set()
    exclusion_zone = set()
    for sensor in data:
        bx = sensor[2]
        by = sensor[3]
        beacons.add((bx, by))
        
        dx = abs(sensor[0] - sensor[2])
        dy = abs(sensor[1] - sensor[3])

        radius = dx + dy

        y = 2000000

        #y = 10
        # ^^^ for test input
        
        distance_to_row = abs(sensor[1] - y)
        if distance_to_row < radius:
            exclusion_distance = radius - distance_to_row
            min_x = sensor[0] - exclusion_distance
            max_x = sensor[0] + exclusion_distance
            for x in range(min_x, max_x + 1):
                exclusion_zone.add((x, y))


    exclusion_zone = exclusion_zone - beacons
    return len(exclusion_zone)


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] -  p2[1])


def sensor_x_range(sensor, radius, y):
    distance_to_row = abs(sensor[1] - y)
    if distance_to_row < radius:
        exclusion_distance = radius - distance_to_row
        min_x = sensor[0] - exclusion_distance
        max_x = sensor[0] + exclusion_distance

        # clamp for part 2
        min_x = max(0, min_x)
        max_x = min(4000000, max_x)
        
        return min_x, max_x
    return None, None


def sensor_y_range(sensor, radius, x):
    distance_to_col = abs(sensor[0] - x)
    if distance_to_col < radius:
        exclusion_distance = radius - distance_to_col
        min_y = sensor[1] - exclusion_distance
        max_y = sensor[1] + exclusion_distance
        
        return min_y, max_y
    return None, None

    

def part_02(data):
    result = -1
    sensors = {}

    for sensor in data:
        dx = abs(sensor[0] - sensor[2])
        dy = abs(sensor[1] - sensor[3])

        radius = dx + dy
        sensors[sensor] = radius
        
    max_val = 4000000 + 1
    #max_val = 20 + 1    
    beacon = [None, None]

    x_options = []
    y_options = []
    
    for y in range(0, max_val):
        x_ranges = []
        
        for sensor in sensors:
            min_x, max_x = sensor_x_range(sensor, sensors[sensor], y)
            if min_x != None:
                x_ranges.append([min_x, max_x])

        merged_x_ranges = []
        cur_range = None
        
        x_ranges.sort()
        for x_range in x_ranges:
            if cur_range == None:
                cur_range = x_range
                continue

            if x_range[0] > cur_range[1] + 1:
                merged_x_ranges.append(cur_range)
                cur_range = x_range
            else:
                cur_range[1] = max(cur_range[1], x_range[1])

        merged_x_ranges.append(cur_range)

        if len(merged_x_ranges) > 1:
            print(x_ranges)
            print(merged_x_ranges)
        
        if len(merged_x_ranges) > 1:
            beacon[0] = merged_x_ranges[0][1] + 1
            beacon[1] = y

            
    '''
    for x in range(0, max_val):
        for y in range(0, max_val):
            beacon = (x, y)
            for sensor in sensors:
                if beacon:
                    if distance(beacon, sensor) <= sensors[sensor]:
                        beacon = None

            if beacon != None:
                result = (beacon[0] * 4000000) + beacon[1]
                print(beacon)
                return result
    '''

    if beacon != None:
        result = (beacon[0] * 4000000) + beacon[1]
        print(beacon)
    return result


if __name__ == "__main__":
    main()
