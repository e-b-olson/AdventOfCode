from copy import deepcopy

class Monkey():
    def __init__(self):
        self.name = None
        self.items = []
        self.operation = None
        self.test = None
        self.count = 0

        # HACK
        self.lcm = (19 * 3 * 13 * 7 * 5 * 11 * 17 * 2)

    def turn(self, monkeys):
        while self.items:
            worry = self.items.pop(0)

            # inspect
            worry = self.operation(worry)
            worry = worry // 3
            
            # test
            dest_monkey = self.test(worry)
            monkeys[dest_monkey].items.append(worry)
            
            # count
            self.count += 1

    def turn_part_02(self, monkeys):
        while self.items:
            worry = self.items.pop(0)

            # inspect
            worry = self.operation(worry)

            # UPDATE: i did some reading.  And we can simplify worry here
            #         Since all the tests check if the worry is divisible
            #         by some number, we can reduce the number by the
            #         least common multiple
            worry = worry % self.lcm
            
            # test
            dest_monkey = self.test(worry)
            monkeys[dest_monkey].items.append(worry)
            
            # count
            self.count += 1


    def __repr__(self):
        return str("Monkey {}: {}".format(self.name, self.count))


def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))



def parse_input():
    '''
    There are only 8 monkeys... think it will
    be faster just to do this by hand.
    '''

    '''
    data = None
    with open("puzzle_11_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    monkeys = []
    monkey = None
    for line in data:
        line = line.strip()
        if not line:
            if monkey:
                monkeys.append(monkey)
            continue
        line = line.split(' ')

        if line[0] == "Monkey":
            monkey = Monkey()
            monkey.name = int(line[1][0])

        if line[0] == "Starting":
            for item in line[2:]:
                item_id = item.replace(',', '')
                monkey.items.append(int(item_id))
    '''

    monkeys = []
    monkey = Monkey()
    monkey.name = 0
    monkey.items = [85, 77, 77]
    monkey.operation = lambda x: x * 7
    monkey.test = lambda x: 6 if x % 19 == 0 else 7
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 1
    monkey.items = [80, 99]
    monkey.operation = lambda x: x * 11
    monkey.test = lambda x: 3 if x % 3 == 0 else 5
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 2
    monkey.items = [74, 60, 74, 63, 86, 92, 80]
    monkey.operation = lambda x: x + 8
    monkey.test = lambda x: 0 if x % 13 == 0 else 6
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 3
    monkey.items = [71, 58, 93, 65, 80, 68, 54, 71]
    monkey.operation = lambda x: x + 7
    monkey.test = lambda x: 2 if x % 7 == 0 else 4
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 4
    monkey.items = [97, 56, 79, 65, 58]
    monkey.operation = lambda x: x + 5
    monkey.test = lambda x: 2 if x % 5 == 0 else 0
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 5
    monkey.items = [77]
    monkey.operation = lambda x: x + 4
    monkey.test = lambda x: 4 if x % 11 == 0 else 3
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 6
    monkey.items = [99, 90, 84, 50]
    monkey.operation = lambda x: x * x
    monkey.test = lambda x: 7 if x % 17 == 0 else 1
    monkeys.append(monkey)

    monkey = Monkey()
    monkey.name = 7
    monkey.items = [50, 66, 61, 92, 64, 78]
    monkey.operation = lambda x: x + 3
    monkey.test = lambda x: 5 if x % 2 == 0 else 1
    monkeys.append(monkey)
    
    return monkeys


def part_01(data):
    monkeys = deepcopy(data)

    for turn in range(20):
        for monkey in monkeys:
            monkey.turn(monkeys)

    sorted_monkeys = sorted(monkeys, key=lambda x: -x.count)
    result = sorted_monkeys[0].count * sorted_monkeys[1].count
    
    return result


def part_02(data):
    monkeys = deepcopy(data)
    
    for turn in range(10000):
        for monkey in monkeys:
            monkey.turn_part_02(monkeys)

    sorted_monkeys = sorted(monkeys, key=lambda x: -x.count)
    result = sorted_monkeys[0].count * sorted_monkeys[1].count
    
    return result



if __name__ == "__main__":
    main()
