
def main():
    with open("puzzle_04_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))

def parse_data(data):
    pairs = []
    for pair in data:
        pair = pair.strip()
        if not pair:
            continue

        # "94-97,31-95"
        ranges = pair.split(',')
        elf_1_range_str = ranges[0]
        elf_2_range_str = ranges[1]

        # "94-97"
        elf_1_range_list = elf_1_range_str.split('-')
        elf_2_range_list = elf_2_range_str.split('-')

        elf_1 = tuple(map(int, elf_1_range_list))
        elf_2 = tuple(map(int, elf_2_range_list))

        pairs.append((elf_1, elf_2))

    return pairs
        
    # arg!  just realized... I didn't convert to INT!!!
    
def part_01(data):
    result = 0

    pairs = parse_data(data)

    for pair in pairs:
        elf_1 = pair[0]
        elf_2 = pair[1]
        
        overlap = False
        if elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
            overlap = True

        if elf_2[0] <= elf_1[0] and elf_2[1] >= elf_1[1]:
            overlap = True
            
        if overlap:
            result += 1

    return result

    
def part_01_orig(data):
    result = 0

    pairs = set()
    
    for pair in data:
        pair = pair.strip()

        elves = pair.split(',')
        elf_1_range = elves[0]
        elf_2_range = elves[1]

        elf_1 = tuple(map(int, elf_1_range.split('-')))
        elf_2 = tuple(map(int, elf_2_range.split('-')))

        elf_pair_list = sorted([elf_1, elf_2])
        elf_pair = (elf_pair_list[0], elf_pair_list[1])
        pairs.add(elf_pair)

    for pair in pairs:
        elf_1 = pair[0]
        elf_2 = pair[1]
        
        overlap = False
        if elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
            overlap = True

        if elf_2[0] <= elf_1[0] and elf_2[1] >= elf_1[1]:
            overlap = True

        if overlap:
            result += 1

        # print("{}: {}".format(pair, overlap))
    
    return result

def part_02(data):
    result = 0

    pairs = parse_data(data)

    for pair in pairs:
        elf_1 = pair[0]
        elf_2 = pair[1]
        
        overlap = True
        if elf_1[1] < elf_2[0] or elf_1[0] > elf_2[1]:
            overlap = False

        if elf_2[1] < elf_1[0] or elf_2[0] > elf_1[1]:
            overlap = False

        # print("{}: {}".format(pair, overlap))
            
        if overlap:
            result += 1

    return result


if __name__ == "__main__":
    main()
