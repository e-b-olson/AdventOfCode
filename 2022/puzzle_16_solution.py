from copy import deepcopy

class Valve():

    def __init__(self, name, flow = None):
        self.name = name
        self.flow = flow
        self.valves = set()

    def add_valve(self, valve):
        self.valves.add(valve)

    def __repr__(self):
        return "{} ({}): {}".format(self.name, self.flow, self.valves)
        
def main():
    data = parse_input()

    answer_1 = part_01(data)
    answer_2 = part_02(data)

    print("Answer 01: {}".format(answer_1))
    print("Answer 02: {}".format(answer_2))



def parse_input():
    data = None

    with open("puzzle_16_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    valves = {}

    for line in data:
        line = line.strip()
        elements = line.split(' ')
        name = elements[1]

        valve = None
        if name in valves:
            valve = valves[name]
        else:
            valve = Valve(name)
            valves[name] = valve
        
        flow = int(elements[4].replace('rate=', '').replace(';', ''))
        valve.flow = flow
        
        connections = elements[9:]
        for connection in connections:
            connection = connection.replace(',', '')
            valve.valves.add(connection)
        
    return valves



def part_01(valves):
    #for valve in valves:
    #    print(valves[valve])

    dp = {}
    
    def part_01_recurse(valve, open_valves, turns):
        if turns == 0:
            return 0

        key = valve.name + str(open_valves) + str(turns)
        if key in dp:
            return dp[key]
        
        result = 0
        
        if valve.flow > 0 and valve.name not in open_valves:
            do = open_valves.copy()
            do.append(valve.name)
            do.sort()

            dt = turns - 1
            score = (valve.flow * dt)
            
            option = score + part_01_recurse(valve, do, dt)
            result = max(result, option)

        for name in valve.valves:
            dv = valves[name]
            do = open_valves
            dt = turns - 1
            option = part_01_recurse(dv, do, dt)
            result = max(result, option)

        dp[key] = result
        return result

    return part_01_recurse(valves['AA'], [], 30)
    

def part_02(valves):
    dp = {}
    
    def part_02_recurse(v0, v1, open_valves, turns):
        if turns == 0:
            return 0

        locations = sorted([v0.name, v1.name])
        key = str(locations) + str(open_valves) + str(turns)
        if key in dp:
            return dp[key]
        
        result = 0

        # skip v0 / skip v1
        # open v0 / skip v1
        # skip v0 / open v1

        # open v0 / open v1
        if v0.flow > 0 and v0.name not in open_valves and \
           v1.flow > 0 and v1.name not in open_valves and \
           v0.name != v1.name:
            do = open_valves.copy()
            do.append(v0.name)
            do.append(v1.name)
            do.sort()

            dt = turns - 1
            score = (v0.flow * dt) + (v1.flow * dt)
            
            option = score + part_02_recurse(v0, v1, do, dt)
            result = max(result, option)
        
        # open v0 / skip v1
        if v0.flow > 0 and v0.name not in open_valves:
            do = open_valves.copy()
            do.append(v0.name)
            do.sort()

            dt = turns - 1
            score = (v0.flow * dt)

            for name in v1.valves:
            #for name in [v1.name]:
                dv = valves[name]
                option = score + part_02_recurse(v0, dv, do, dt)
                result = max(result, option)

        # skip v0 / open v1
        if v1.flow > 0 and v1.name not in open_valves:
            do = open_valves.copy()
            do.append(v1.name)
            do.sort()

            dt = turns - 1
            score = (v1.flow * dt)

            for name in v0.valves:
                dv = valves[name]
                option = score + part_02_recurse(dv, v1, do, dt)
                result = max(result, option)
        
        # skip v0 / skip v1
        for name0 in v0.valves:
            dv0 = valves[name0]
            for name1 in v1.valves:
            #for name1 in [v1.name]:
                dv1 = valves[name1]
                do = open_valves
                dt = turns - 1
                option = part_02_recurse(dv0, dv1, do, dt)
                result = max(result, option)

        dp[key] = result
        return result

    return part_02_recurse(valves['AA'], valves['AA'], [], 26)


if __name__ == "__main__":
    main()
