
DEBUG = False

def debug_print(*args):
    if not DEBUG:
        return
    print(*args)


def main():
    with open("puzzle_01_input.txt", 'r') as f:
        data = f.readlines()        
    f.close()

    part_01(data)
    part_02(data)


def part_01(data):
    result = 0
    elf = 0
    for cals in data:
        if not cals or cals == '\n':
            debug_print("--------------------")
            debug_print(elf)
            debug_print()
            result = max(result, elf)
            elf = 0
            continue

        cals_val = int(cals)
        debug_print(cals_val)
        elf += cals_val

    print("Answer 01: {}".format(result))

def part_02(data):
    result = 0
    elf = 0
    elves = []
    for cals in data:
        if not cals or cals == '\n':
            elves.append(elf)
            elf = 0
            continue

        cals_val = int(cals)
        elf += cals_val

    sorted_elves = sorted(elves)
    top_three = sorted_elves[-3:]
    print("Top Three: {}".format(top_three))
    result = sum(top_three)

    print("Answer 02: {}".format(result))

    
if __name__ == "__main__":
    main()
