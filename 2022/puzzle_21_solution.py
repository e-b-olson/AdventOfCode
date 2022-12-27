from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    print("Answer 01: {}".format(answer_01))

    answer_02 = part_02(data)
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None

    with open("puzzle_21_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    monkey_names = set()
    monkeys = {}
    for line in data:
        line = line.strip()
        m = line.split(' ')

        name = m[0].replace(':', '')
        monkey = [None, None, None, None]
        if len(m) == 2:
            num = int(m[1])
            monkey[0] = num
        else:
            m1 = m[1]
            m2 = m[3]
            op = m[2]
            monkey_names.add(m1)
            monkey_names.add(m2)
            monkey = [None, op, m1, m2]

        monkey_names.add(name)
        
        #print(monkey)
        monkeys[name] = monkey

    for monkey_name in monkey_names:
        if monkey_name not in monkeys:
            monkeys[monkey_name] = [None, None, None, None]
        
    return monkeys


def op(fn, a, b):
    if fn == '+':
        return a + b
    if fn == '-':
        return a - b
    if fn == '*':
        return a * b

    return a // b


def part_01(data):
    monkeys = deepcopy(data)
    
    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3
    
    stack = ["root"]

    while stack:
        name = stack.pop(-1)
        monkey = monkeys[name]

        if monkey[VAL]:
            continue

        V1 = monkeys[monkey[M1]][VAL] if monkey[M1] else None
        V2 = monkeys[monkey[M2]][VAL] if monkey[M2] else None

        if V1 != None and V2 != None:
            val = op(monkey[OP], V1, V2)
            monkey[VAL] = val
            continue

        stack.append(name)
        
        if V1 == None:
            stack.append(monkey[M1])

        if V2 == None:
            stack.append(monkey[M2])

    return monkeys["root"][VAL]

def part_01_init(data):
    monkeys = deepcopy(data)    
    result = 0

    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3

    subs = {}
    for name in monkeys:
        subs[name] = set()
        
    for name in monkeys:
        monkey = monkeys[name]

        if monkey[M1] or monkey[M2]:
            subs[monkey[M1]].add(name)
            subs[monkey[M2]].add(name)
            
    while monkeys["root"][VAL] == None:
        for k in monkeys:
            monkey = monkeys[k]
            if monkey[VAL] != None and subs[k]:
                for sub in subs:
                    if monkeys[sub][M1] == k:
                        monkeys[sub][M1] = monkey[VAL]
                    if monkeys[sub][M2] == k:
                        monkeys[sub][M2] == monkey[VAL]
                subs[k] = None

            if monkey[VAL] == None:
                if type(monkey[M1]) == type(0) and type(monkey[M2]) == type(0):
                    monkey[VAL] = op(monkey[M1], monkey[M2])

    result = monkeys["root"][VAL]
    return result


def update_monkey(X, monkeys):
    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3

    # TEST
    monkeys["humn"][VAL] = None

    stack = [X]

    while stack:
        name = stack.pop(-1)
        monkey = monkeys[name]
        
        if monkey[VAL] != None:
            continue

        N1 = monkey[M1]
        N2 = monkey[M2]

        # if N1 == "humn" or N2 == "humn":  
        
        V1 = monkeys[N1][VAL] if N1 else None
        V2 = monkeys[N2][VAL] if N2 else None
        
        if V1 != None and V2 != None:
            val = op(monkey[OP], V1, V2)
            monkey[VAL] = val
            continue

        #if name != "humn" and N1 != "humn" and N2 != "humn":
        stack.append(name)
        
        if V1 == None and N1 != "humn":
            stack.append(monkey[M1])

        if V2 == None and N2 != "humn":
            stack.append(monkey[M2])    


def print_monkey_stack(name, monkeys):
    monkey = monkeys[name]

    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3

    V1 = None
    V2 = None

    N1 = monkey[M1]
    N2 = monkey[M2]
    
    if N1 != None:
        V1 = monkeys[N1][VAL]
        print_monkey_stack(N1, monkeys)

    if N2 != None:
        V2 = monkeys[N2][VAL]
        print_monkey_stack(N2, monkeys)

    V = monkey[VAL]
    O = monkey[OP]

    if N1 != None or N2 != None:
        print("{}: {}\t\t{} {} {}\t({} {} {})".format(name, V, N1, O, N2, V1, O, V2)) 
    else:
        print("{}: {}".format(name, V))

        
def monkey_val_02(name, monkeys):
    monkey = monkeys[name]

    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3
    
    #if name == "humn":
    #    monkey[VAL] = None
    #    return monkey[VAL]
    
    if monkey[VAL] != None:
        return monkey[VAL]

    V1 = None
    V2 = None

    N1 = monkey[M1]
    N2 = monkey[M2]
    
    if N1 != None:
        V1 = monkey_val_02(N1, monkeys)

    if N2 != None:
        V2 = monkey_val_02(N2, monkeys)

    if V1 != None and V2 != None:
        val = op(monkey[OP], V1, V2)
        monkey[VAL] = val

    return monkey[VAL]
            

def part_02(data):
    monkeys = deepcopy(data)
    root = monkeys["root"]

    # HACK
    monkeys['humn'][0] = 3952673930912 #None
    
    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3
    
    X1 = root[M1]
    X2 = root[M2]

    Y1 = monkeys[X1]
    Y2 = monkeys[X2]

    Z1 = monkey_val_02(X1, monkeys)
    Z2 = monkey_val_02(X2, monkeys)

    if Z1 != None and Z2 != None and Z1 == Z2:
        print("DONE!")
        print("{}: {}".format(X1, Z1))
        print("{}: {}".format(X2, Z2))
        print("humn: {}".format(monkeys["humn"][VAL]))
        return monkeys["humn"][VAL]
    
    XX = X1 if Z1 == None else X2
    TARGET = Z1 if Z2 == None else Z2

    print("{}: {}".format(X1, Z1))
    print("{}: {}".format(X2, Z2))
    print("----------")
    print("{}: {}".format(XX, TARGET))
    print()

    #---------------------------------------
    mirror_ops = {'+': '-',
                  '-': '+',
                  '*': '/',
                  '/': '*'
                  }
    
    stack = [[XX, TARGET]]
    while stack:
        name, target = stack.pop(-1)
        monkey = monkeys[name]

        if name == "humn" and monkey[VAL] == None:
            monkey[VAL] = target
        
        if monkey[VAL] == target:
            print("{}: {}".format(name, target))
            continue

        N1 = monkey[M1]
        N2 = monkey[M2]
            
        V1 = monkeys[N1][VAL] #if N1 != "humn" else None
        V2 = monkeys[N2][VAL] #if N2 != "humn" else None

        if V1 == None and V2 == None:
            print("ERROR: {} ({}, {})".format(name, N1, N2))
            break

        print("{}: {}\t {} {} {} \t{}".format(name, target, V1, monkey[OP], V2, monkey))
        
        if V1 == None:
            # V1 + V2 = target --> V1 = target - V2
            # V1 - V2 = target --> V1 = target + V2
            # V1 * V2 = target --> V1 = target / V2
            # V1 / V2 = target --> V1 = target * V2
            mirror_op = mirror_ops[monkey[OP]]
            new_target = op(mirror_op, target, V2)
            stack.append([N1, new_target])

        if V2 == None:
            # V1 + V2 = target --> V2 = target - V1
            # V1 - V2 = target --> V2 = V1 - target
            # V1 * V2 = target --> V2 = target / V1
            # V1 / V2 = target --> V2 = V1 / target
            cur_op = monkey[OP]
            mirror_op = mirror_ops[cur_op]
            if cur_op == '-' or cur_op == '/':
                new_target = op(cur_op, V1, target)
            else:
                new_target = op(mirror_op, target, V1)
            stack.append([N2, new_target])

    print("ANSWER")
    print("{}: {}".format(X1, monkeys[X1][VAL]))
    print("{}: {}".format(X2, monkeys[X2][VAL]))

    print("-------------------------------")
    #print_monkey_stack(XX, monkeys)
    
    return monkeys['humn'][VAL]

    

def part_02_orig(data):
    monkeys = deepcopy(data)
    
    VAL = 0
    OP = 1
    M1 = 2
    M2 = 3

    # TEST
    monkeys["humn"][VAL] = None
    
    X1 = monkeys["root"][M1]
    X2 = monkeys["root"][M2]

    stack = [X2]

    while stack:
        name = stack.pop(-1)
        monkey = monkeys[name]
        
        if monkey[VAL] != None:
            if name == X1 or name == X2:
                print("FOUND: {}: {}".format(name, monkey[VAL]))
            continue

        N1 = monkey[M1]
        N2 = monkey[M2]

        # if N1 == "humn" or N2 == "humn":  
        
        V1 = monkeys[N1][VAL] if N1 else None
        V2 = monkeys[N2][VAL] if N2 else None
        
        if V1 != None and V2 != None:
            val = op(monkey[OP], V1, V2)
            monkey[VAL] = val
            continue

        #if name != "humn" and N1 != "humn" and N2 != "humn":
        stack.append(name)
        
        if V1 == None: # and N1 != "humn":
            stack.append(monkey[M1])

        if V2 == None: # and N2 != "humn":
            stack.append(monkey[M2])


    Z1 = monkeys[X1][VAL]
    Z2 = monkeys[X2][VAL]
    print("{}: {}\n{}: {}".format(X1, Z1, X2, Z2))
    
    mirror_ops = {'+': '-',
                  '-': '+',
                  '*': '/',
                  '/': '*'
                  }
    
    if monkeys[X1][VAL] != monkeys[X2][VAL]:
        target = Z1 if Z1 else Z2
        name = X1 if monkeys[X1][VAL] == None else X2

        stack = [[name, target]]
        while stack:
            name, target = stack.pop(-1)
            monkey = monkeys[name]

            print("{}: {}\t\t{}".format(name, target, monkey))

            if name == "humn":
                monkeys[name][VAL] = target

            if monkey[VAL] == target:
                continue

            N1 = monkey[M1]
            N2 = monkey[M2]
            
            V1 = monkeys[N1][VAL] if N1 != "humn" else None
            V2 = monkeys[N2][VAL] if N2 != "humn" else None

            if V1 == None and V2 == None:
                print("ERROR: {} ({}, {})".format(name, N1, N2))
                
                # try to update
                if N1 != None and N1 != "humn":
                    update_monkey(N1, monkeys)
                if N2 != None and N2 != "humn":
                    update_monkey(N2, monkeys)
                continue

            if V1 == None:
                mirror_op = mirror_ops[monkey[OP]]
                new_target = op(mirror_op, target, V2)
                stack.append([N1, new_target])

            if V2 == None:
                mirror_op = mirror_ops[monkey[OP]]
                new_target = op(mirror_op, target, V1)
                stack.append([N2, new_target])


    print("ANSWER")
    print("{}: {}".format(X1, monkeys[X1][VAL]))
    print("{}: {}".format(X2, monkeys[X2][VAL]))
                
    return monkeys['humn'][VAL]
        



if __name__ == "__main__":
    main()
