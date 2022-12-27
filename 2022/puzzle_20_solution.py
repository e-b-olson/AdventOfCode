from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)

    print("Answer 01: {}".format(answer_01))


def parse_input():
    data = None

    with open("puzzle_20_input.txt", 'r') as f:
        data = f.readlines()
    f.close()
    
    nums = []
    for line in data:
        line = line.strip()
        n = int(line)
        nums.append(n)
        
    return nums


def apply_offsets(data, offsets):
    result = [0 for _ in range(len(data))]
    for i, n in enumerate(data):
        index = (i + offsets[i]) % len(data)
        result[index] = n

    print("{} -> {}: {}".format(data, offsets, result))
    return result


def part_01(data):
    class Node():
        def __init__(self, val, rt=None, lt=None):
            test_offset = 7 if val > 0 else -7 if val < 0 else 0
            self.val = val * 811589153
            self.rt = rt
            self.lt = lt

    nodes = []
    for val in data:
        node = Node(val)
        nodes.append(node)

    node_count = len(nodes)

    # build list
    for i in range(node_count):
        right = (i + 1) % node_count
        left = (i - 1) % node_count
        nodes[i].rt = nodes[right]
        nodes[i].lt = nodes[left]

    def move_right(node):
        left = node.lt
        right = node.rt

        node.lt = None
        node.rt = None

        left.rt = right
        right.lt = left

        new_left = right
        new_right = right.rt
        
        node.rt = new_right
        node.lt = new_left

        new_right.lt = node
        new_left.rt = node

        #print("{} RIGHT -->".format(node.val))
        #print_zeroed_list()
        
    def move_left(node):
        left = node.lt
        right = node.rt

        node.lt = None
        node.rt = None

        left.rt = right
        right.lt = left

        new_left = left.lt
        new_right = left

        node.lt = new_left
        node.rt = new_right

        new_left.rt = node
        new_right.lt = node

        #print("{} LEFT <--".format(node.val))
        #print_zeroed_list()

    def print_list():
        head = nodes[0]
        cur = head
        tail = head.lt

        vals = []
        while cur != None and cur != tail:
            vals.append(cur.val)
            cur = cur.rt
        vals.append(cur.val)

        print(vals)

    def print_zeroed_list():
        head = nodes[0]
        for node in nodes:
            if node.val == 0:
                head = node

        cur = head
        tail = head.lt

        vals = []
        while cur != None and cur != tail:
            vals.append(cur.val)
            cur = cur.rt
        vals.append(cur.val)

        print(vals)


    #print_list()
    #print_zeroed_list()

    mod = node_count - 1
    
    for z in range(10):
        for node in nodes:
            count = 0
            if node.val < 0:
                count = abs(node.val) % mod
                if count == 0:
                    continue
                for i in range(count):
                    move_left(node)

            if node.val > 0:
                count = node.val % mod
                if count == 0:
                    continue
                for i in range(count):
                    move_right(node)

            #print(" -- STEP --")
            #print("{} -> {}".format(node.val, count * 1 if node.val > 0 else -1))
            #print_zeroed_list()

        #print("--------")
        #print_list()
        #print_zeroed_list()

    values = []
    head = nodes[0]
    cur = head
    tail = cur.lt

    while cur != None and cur != tail:
        values.append(cur.val)
        cur = cur.rt

    values.append(cur.val)
        
    start_index = 0
    for i, x in enumerate(values):
        if x == 0:
            start_index = i

    nums = []
    for i in range(1, 3 + 1):
        index = (start_index + (i * 1000)) % node_count
        nums.append(values[index])

    print(nums)
    return sum(nums)    



def unmix(data):
    elements = deepcopy(data)
    element_count = len(elements)
    
    IDX = 0
    VAL = 1

    for i in range(element_count):
        e = elements[i]

        if e[VAL] == 0:
            continue
        
        start = e[IDX]
        end = (start + e[VAL]) % element_count

        if e[VAL] > 0:
            if start > end:
                end = end + 1

        if e[VAL] < 0:
            end = (end - 1) % element_count

        step = 1 if start > end else -1

        before = deepcopy(elements)

        range_start = min(start, end)
        range_end = max(start, end)
        
        for x in elements:
            if x[IDX] >= range_start and x[IDX] <= range_end:
                x[IDX] += step

        elements[i][IDX] = end

        #print("{}: {} -> {}\t{}".format(e[VAL], start, end, elements))
        ##print("{}: {} -> {}".format(e[VAL], start, end))
        
        ##before_elements = ["x" for _ in range(len(elements))]
        ##after_elements = ["x" for _ in range(len(elements))]

        ##for e in before:
        ##    before_elements[e[0]] = e[1]

        ##for e in elements:
        ##    after_elements[e[0]] = e[1]
        
        ##print("{} --> {}".format(before_elements, after_elements))

    return elements

        

def part_01_nope(data):
    working_data = []
    for i, n in enumerate(data):
        working_data.append([i, n])

    elements = unmix(working_data)
    elements_len = len(elements)
    
    values = ["x" for _ in range(elements_len)]

    for x in elements:
        values[x[0]] = x[1]

    ##print(values)
    ##return

    start_index = 0
    for i, x in enumerate(values):
        if x == 0:
            start_index = i

    nums = []
    for i in range(1, 3 + 1):
        index = (start_index + (i * 1000)) % elements_len
        nums.append(values[index])

    print(nums)
    return sum(nums)    


    
    IDX = 0
    VAL = 1

    expected_dst = [1, 2, 4, 5, 6, 3, 3]
    actual_dst =   [1, 2, 5, 5, 0, 3]
    
    working_data = []
    for i, n in enumerate(data):
        working_data.append([i, n])

    len_data = len(data)
    
    for i in range(len_data):
        e = working_data[i]

        if e[VAL] == 0:
            continue

        moving_right = e[VAL] > 0
        moving_left = e[VAL] < 0
        
        start = e[IDX]
        end = (e[IDX] + e[VAL]) % len_data

        # adjust end
        if moving_right and end < start:
            end = (end + 1) % len_data

        if moving_left:
            end = (end - 1) % len_data

        if moving_left and start < end:
            end = (end - 1) % len_data
        
        if start == end:
            continue

        if start < end:
            for x in working_data:
                if x[IDX] >= start and x[IDX] <= end:
                    x[IDX] = (x[IDX] - 1) % len_data

        if start > end:
            for x in working_data:
                if x[IDX] >= end and x[IDX] <= start:
                    x[IDX] = (x[IDX] + 1) % len_data

        e[IDX] = end

        result_data = ['x' for _ in range(len_data)]
        for x in working_data:
            result_data[x[IDX]] = x[VAL]
            
        #sorted_data = sorted(working_data, key=lambda x: x[IDX])
        #for x in sorted_data:
        #    result_data.append(x[1])
        print("{}: {} -> {}\t{}".format(e[VAL], start, end, result_data))
        #print("{}\t\t[{}]".format(result_data, working_data))

    nums = []
    start_index = 0
    for i, x in enumerate(result_data):
        if x == 0:
            start_index = i
    
    for i in range(1, 3 + 1):
        index = (start_index + (i * 1000)) % len_data
        nums.append(result_data[index])

    print(nums)
    return sum(nums)    

    
def part_01_maybe(data):
    IDX = 0
    VAL = 1
    
    working_data = []
    for i, n in enumerate(data):
        working_data.append([i, n])

    len_data = len(data)
        
    for i in range(len_data):
        e = working_data[i]

        if e[VAL] == 0:
            continue

        moving_right = e[VAL] > 0
        moving_left = e[VAL] < 0
        
        start = e[IDX]
        offset = e[IDX] + e[VAL]
        end = offset % len_data

        # handle wrapping
        if moving_right and start > end:
            end = (end + 1) % len_data
        
        if moving_left:
            end = (end - 1) % len_data

        if start == end:
            continue

        range_start = min(start, end)
        range_end = max(start, end)

        shift = -1 if start < end else 1
        
        for x in working_data:
            if x[IDX] >= range_start and x[IDX] <= range_end:
                x[IDX] = (x[IDX] + shift) % len_data
                
        e[IDX] = end

        result_data = ['x' for _ in range(len_data)]
        for x in working_data:
            result_data[x[IDX]] = x[VAL]
            
        #sorted_data = sorted(working_data, key=lambda x: x[IDX])
        #for x in sorted_data:
        #    result_data.append(x[1])
        ##print("{}: {} -> {}\t{}".format(e[VAL], start, end, result_data))
        #print("{}\t\t[{}]".format(result_data, working_data))

    nums = []
    start_index = 0
    for i, x in enumerate(result_data):
        if x == 0:
            start_index = i
    
    for i in range(1, 3 + 1):
        index = (start_index + (i * 1000)) % len_data
        nums.append(result_data[index])

    print(nums)
    return sum(nums)

def part_01_orig(data):
    len_data = len(data)
    
    offsets = data.copy()
    blank_offsets = [0 for _ in range(len_data)]

    for i in range(len_data):
        start = i
        cur_offset = offsets[i]
        
        dst_index = (start + cur_offset) % len_data
        offset = dst_index - start

        #print("{} -> {} ({})".format(start, dst_index, offset))
        
        if offset:
            if offset > 0:
                for j in range(i + 1, dst_index + 1):
                    offsets[j] -= 1
                    blank_offsets[j] -= 1
            
            if offset < 0:
                for j in range(dst_index, i):
                    offsets[j] += 1
                    blank_offsets[j] += 1

        offsets[i] = offset
        blank_offsets[i] = offset

        #print(blank_offsets)
        apply_offsets(data, offsets)

    result = [0 for _ in range(len_data)]
    for i, offset in enumerate(offsets):
        index = (i + offset) % len_data
        result[index] = data[i]

    return result

def part_02(data):
    pass



if __name__ == "__main__":
    main()
