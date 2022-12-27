
def main():
    with open("puzzle_03_input.txt", 'r') as f:
        data = f.readlines()

    f.close()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 1: {}".format(answer_01))
    print("Answer 2: {}".format(answer_02))

def item_score(item):
    if item.isupper():
        return ord(item) - ord('A') + 27
    return ord(item) - ord('a') + 1

def part_01(data):
    result = 0

    for rucksack in data:
        size = len(rucksack)
        mid = size // 2

        left = set(rucksack[:mid])
        right = set(rucksack[mid:])

        intersection = left.intersection(right)
        value = item_score(list(intersection)[0])

        result += value

    return result

def part_02(data):
    result = 0

    group = []
    
    for i, rucksack in enumerate(data):
        if i % 3 == 0:
            if group:
                s0 = set(group[0])
                s1 = set(group[1])
                s2 = set(group[2])

                intersection = s0.intersection(s1, s2)
                value = item_score(list(intersection)[0])
                result += value

            group = []

        group.append(rucksack.strip())        

    if group:
        s0 = set(group[0])
        s1 = set(group[1])
        s2 = set(group[2])

        intersection = s0.intersection(s1, s2)
        value = item_score(list(intersection)[0])
        result += value
        
    return result


if __name__ == "__main__":
    main()
