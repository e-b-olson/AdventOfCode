from copy import deepcopy
from functools import cache

def main():
    data = parse_input()

    #answer_01 = part_01(data)
    answer_02 = part_02(data)

    #print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_blueprint(line):
    line = line.strip()
    elements = line.split(' ')

    bp = []
    for element in elements:
        if element[0] not in "0123456789":
            continue
        num = element.replace(":", '')
        bp.append(int(num))
    return bp

    
def parse_input():
    data = None

    with open("puzzle_19_input.txt", "r") as f:
        data = f.readlines()
    f.close()

    bps = []
    for line in data:
        bp = parse_blueprint(line)
        bps.append(bp)

    return bps


@cache
def subtract(iter_01, iter_02):
    result = tuple(map(lambda x, y: x - y, iter_01, iter_02))
    return result


@cache
def add(iter_01, iter_02):
    result = tuple(map(lambda x, y: x + y, iter_01, iter_02))
    return result


def part_01_process_bp(bp, t=24):

    ORE = 0
    CLA = 1
    OBS = 2
    GEO = 3

    # calc max needed values once
    max_ore = max([bp[1], bp[2], bp[3], bp[5]])
    max_cla = bp[4]
    max_obs = bp[6]
    
    @cache
    def process_bp_recurse(bp, resources, robots, time):
        #if time == 24:
        #    print("{}: {} {} {}".format(bp[0], resources, robots, time))

        # update resources
        next_resources = list(resources)
        next_resources[ORE] += robots[ORE]
        next_resources[CLA] += robots[CLA]
        next_resources[OBS] += robots[OBS]
        next_resources[GEO] += robots[GEO]
        next_resources = tuple(next_resources)

        if time == 0:
            return resources[GEO]

        # early out if impossible with remaining time
        # TODO

        # build robots
        ore_robot_count = resources[ORE] // bp[1]
        cla_robot_count = resources[ORE] // bp[2]
        obs_robot_count = min(resources[ORE] // bp[3], resources[CLA] // bp[4])
        geo_robot_count = min(resources[ORE] // bp[5], resources[OBS] // bp[6])

        #robot_counts = [ore_robot_count, cla_robot_count, obs_robot_count, geo_robot_count]
        #print("ROBOT COUNTS: {}".format(robot_counts))
        
        options = []
        if geo_robot_count > 0:
            new_resources = subtract(next_resources, (bp[5], 0, bp[6], 0))
            new_robots = add(robots, (0, 0, 0, 1))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

            # always build a geo robot if you can! 
            return option

        if obs_robot_count > 0 and robots[2] < max_obs:
            new_resources = subtract(next_resources, (bp[3], bp[4], 0, 0))
            new_robots = add(robots, (0, 0, 1, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        if cla_robot_count > 0 and robots[1] < max_cla:
            new_resources = subtract(next_resources, (bp[2], 0, 0, 0))
            new_robots = add(robots, (0, 1, 0, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        if ore_robot_count > 0 and robots[0] < max_ore:
            new_resources = subtract(next_resources, (bp[1], 0, 0, 0))
            new_robots = add(robots, (1, 0, 0, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        # skip building a robot (but limit this with best guess)
        if resources[0] < 6:
            option = process_bp_recurse(bp, tuple(next_resources), robots, time - 1)
            options.append(option)

        sorted_options = sorted(options)
        return sorted_options[-1]

    return process_bp_recurse(tuple(bp), (0, 0, 0, 0), (1, 0, 0, 0), t)


def part_01(bps):
    scores = []
    
    for bp in bps:
        geo = part_01_process_bp(bp)
        quality = geo * bp[0]
        scores.append(quality)

    return sum(scores)


# clamp resources
@cache
def clamp_resources(resources, max_ore, max_cla, max_obs):
    ore = min(resources[0], max_ore + 5) #if robots[0] >= max_ore else resources[0]
    cla = min(resources[1], max_cla + 9) #if robots[1] >= max_cla else resources[1]
    obs = min(resources[2], max_obs + 9) #if robots[2] >= max_obs else resources[2]
    geo = resources[3]
    return (ore, cla, obs, geo)


# time_sum
@cache
def time_sum(time):
    result = 0
    for i in range(time):
        result += i
    return result


# the max possible given the state and time
@cache
def max_geo(robots, time):
    result = (robots[3] * time)
    result += time_sum(time)
    return result

# SUPER HACK GLOBAL
part_02_max_result = 0

def part_02_process_bp(bp, t=24):
    global part_02_max_result
    part_02_max_result = 0
    
    ORE = 0
    CLA = 1
    OBS = 2
    GEO = 3

    # calc max needed values once
    max_ore = max([bp[1], bp[2], bp[3], bp[5]])
    max_cla = bp[4]
    max_obs = bp[6]

    @cache
    def process_bp_recurse(bp, resources, robots, time):
        global part_02_max_result

        #if time == 24:
        #    print("{}: {} {} {}".format(bp[0], resources, robots, time))

        # update resources
        production = (robots[ORE], robots[CLA], robots[OBS], robots[GEO])
        next_resources = add(resources, production)

        #if max_geo(robots, time) < part_02_max_result:
        #    return 0
        
        if time == 0:
            part_02_max_result = max(part_02_max_result, resources[GEO])
            return part_02_max_result

        # early out if impossible with remaining time
        # TODO

        # build robots
        ore_robot_available = resources[ORE] >= bp[1]
        cla_robot_available = resources[ORE] >= bp[2]
        obs_robot_available = resources[ORE] >= bp[3] and resources[CLA] >= bp[4]
        geo_robot_available = resources[ORE] >= bp[5] and resources[OBS] >= bp[6]

        
        options = []
        if geo_robot_available:
            new_resources = subtract(next_resources, (bp[5], 0, bp[6], 0))
            new_robots = add(robots, (0, 0, 0, 1))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

            # always build a geo robot if you can! 
            return option

        if obs_robot_available and robots[2] < max_obs:
            new_resources = subtract(next_resources, (bp[3], bp[4], 0, 0))
            new_resources = clamp_resources(new_resources, max_ore, max_cla, max_obs)
            new_robots = add(robots, (0, 0, 1, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        if cla_robot_available and robots[1] < max_cla:
            new_resources = subtract(next_resources, (bp[2], 0, 0, 0))
            new_resources = clamp_resources(new_resources, max_ore, max_cla, max_obs)
            new_robots = add(robots, (0, 1, 0, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        if ore_robot_available and robots[0] < max_ore:
            new_resources = subtract(next_resources, (bp[1], 0, 0, 0))
            new_resources = clamp_resources(new_resources, max_ore, max_cla, max_obs)
            new_robots = add(robots, (1, 0, 0, 0))
            option = process_bp_recurse(bp, new_resources, new_robots, time - 1)
            options.append(option)

        # skip building a robot (but limit this with best guess)
        if resources[0] < 6 or resources[2] < max_obs or True:
            new_resources = tuple(next_resources)
            new_resources = clamp_resources(new_resources, max_ore, max_cla, max_obs)
            option = process_bp_recurse(bp, new_resources, robots, time - 1)
            options.append(option)

        sorted_options = sorted(options)
        return sorted_options[-1]

    return process_bp_recurse(tuple(bp), (0, 0, 0, 0), (1, 0, 0, 0), t)


def part_02(bps):
    result = 1
    
    for bp in bps[:3]:
        geo = part_02_process_bp(bp, 32)
        print("{}: {}".format(bp, geo))
        result = result * geo

    return result



if __name__ == "__main__":
    main()
