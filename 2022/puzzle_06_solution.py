
DEBUG = False

def debug_print(*args):
    if DEBUG:
        print(*args)

def main():
    data = parse_input()
    data = ''.join(data)
    data = data.strip()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None

    with open("puzzle_06_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    return data


def part_01(data):
    result = None
    debug_print(data)

    for i in range(4, len(data)):
        s = set(data[i-4:i])
        if len(s) == 4:
            result = i
            break

    return result


def part_02(data):
    result = None
    debug_print(data)

    for i in range(14, len(data)):
        s = set(data[i-14:i])
        if len(s) == 14:
            result = i
            break

    return result

    
if __name__ == "__main__":
    main()
