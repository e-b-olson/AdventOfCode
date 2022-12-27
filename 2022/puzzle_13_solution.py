from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))



def parse_input():
    data = None
    
    with open("puzzle_13_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    packets = []
    for line in data:
        line = line.strip()
        packet = parse_line(line)
        if packet != None:
            packets.append(packet)
    
    return packets


def parse_line(line):
    if not line:
        return None

    cur_array = None
    stack = []
    element = ""

    for c in line:
        if c == '[':
            if cur_array != None:
                stack.append(cur_array)
            cur_array = []
            continue

        if c == ']':
            if element:
                cur_array.append(int(element))

            if stack:
                element = cur_array
                cur_array = stack.pop(-1)
                cur_array.append(element)
                element = ""
            continue
            
        if c == ',':
            if element:
                cur_array.append(int(element))
                element = ""
            continue

        element += c
 
    result = cur_array
    return result


def correct_order(left, right):
    #print(left)
    #print(right)

    # both integers
    if type(left) == type(0) and type(right) == type(0):
        if left < right:
            return True

        if left > right:
            #print("False 0")
            return False

        return None

    # both lists
    if type(left) == type([]) and type(right) == type([]):
        for i in range(len(left)):
            if i >= len(right):
                #print("False 1")
                return False

            determined_order = correct_order(left[i], right[i])
            if determined_order != None:
                return determined_order

        if len(left) < len(right):
            return True
            
        return None

    if type(left) == type(0) and type(right) == type([]):
        return correct_order([left], right)

    if type(left) == type([]) and type(right) == type(0):
        return correct_order(left, [right])

    return None


def part_01(data):
    #print("PART 1")
    #for packet in data:
    #    print(packet)
    ordered_pairs = []
    
    for i, p in enumerate(data):
        if i % 2 == 1:
            if correct_order(data[i - 1], data[i]):
                index = (i // 2) + 1
                ordered_pairs.append(index)

    #print(ordered_pairs)
    result = sum(ordered_pairs)
    return result

def part_02(data):
    packets = deepcopy(data)
    packets.append([[2]])
    packets.append([[6]])

    '''
    def make_comparator(less_than):
        def compare(x, y):
            if less_than(x, y):
                return -1
            elif less_than(y, x):
                return 1
            else:
                return 0
        return compare
    '''

    from functools import cmp_to_key
    def packet_comparator(a, b):
        if correct_order(a, b):
            return -1
        if not correct_order(a, b):
            return 1
        return 0
    
    sorted_packets = sorted(packets, key=cmp_to_key(packet_comparator))
    index_2 = sorted_packets.index([[2]]) + 1
    index_6 = sorted_packets.index([[6]]) + 1
    #for packet in sorted_packets:
    #    print(packet)
    
    return index_2 * index_6

if __name__ == "__main__":
    main()
