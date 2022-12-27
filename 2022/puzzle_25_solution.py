from copy import deepcopy

def main():
    data = parse_input()

    answer_01 = part_01(data)
    print("Answer 01: {}".format(answer_01))



def parse_input():
    data = None

    with open("puzzle_25_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    SNAFU_Nums = []
    for line in data:
        line = line.strip()
        SNAFU_Nums.append(line)

    return SNAFU_Nums


def SNAFU_to_decimal(SNAFU):
    result = 0

    num_map = {'9': 9,
               '8': 8,
               '7': 7,
               '6': 6,
               '5': 5,
               '4': 4,
               '3': 3,
               '2': 2,
               '1': 1,
               '0': 0,
               '-': -1,
               '=': -2}

    place = 0
    for c in SNAFU[::-1]:
        val = num_map[c]
        mul = (5**place)
        result += (val * mul)
        place += 1
    
    return result


def decimal_to_base_five(num):
    result = ""

    remaining = num
    while remaining:
        val = remaining % 5
        remaining = remaining // 5
        result += str(val)

    result = result[::-1]
    
    return result


def decimal_to_SNAFU(num):
    result = ""

    base_five = decimal_to_base_five(num)

    num_map = {0: '0',
               1: '1',
               2: '2',
               3: '1=',
               4: '1-',
               5: '10',
               6: '11',
               7: '12',
               8: '2=',
               9: '2-'
               }

    carry = 0
    for c in base_five[::-1]:
        val = int(c) + carry

        if val < 3:
            result += str(val)
            carry = 0

        if val == 3:
            result += '='
            carry = 1

        if val == 4:
            result += '-'
            carry = 1

        if val == 5:
            result += '0'
            carry = 1

    if carry:
        result += '1'
        
    result = result[::-1]
    #result = result.replace('3', num_map[3])
    #result = result.replace('4', num_map[4])
    return result


def part_01(data):
    result = 0

    for SNAFU in data:
        num = SNAFU_to_decimal(SNAFU)
        result += num
        #reverse = decimal_to_SNAFU(num)
        #print("{}\t{}\t{}".format(SNAFU, num, reverse))

    snafu_result = decimal_to_SNAFU(result)
    #print("Result: {} ({})".format(result, snafu_result))
    
    return snafu_result


def part_02(data):
    pass


if __name__ == "__main__":
    main()
