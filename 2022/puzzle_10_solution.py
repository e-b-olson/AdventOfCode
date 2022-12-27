
def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))



def parse_input():
    data = None
    
    with open("puzzle_10_input.txt", 'r') as f:
        data = f.readlines()
    f.close()
    
    instructions = []
    for line in data:
        line = line.strip()
        cmd = line.split(' ')
        instructions.append(cmd)
    
    return instructions



def part_01(data):
    #print(data)
    cycles = [1]
    register = 1
 
    addx_vals = []
    instructions = data.copy()
    cycles_to_next_cmd = 0

    while instructions or addx_vals:
        cmd = ["noop"]
        if instructions and cycles_to_next_cmd == 0:
            cmd = instructions.pop(0)
        else:
            cycles_to_next_cmd = min(cycles_to_next_cmd - 1, 0)
        
        if addx_vals:
            val = addx_vals.pop(0)
            register += val

        if cmd[0] == "noop":
            pass

        if cmd[0] == "addx":
            val = int(cmd[1])
            addx_vals.append(0)
            addx_vals.append(val)
            cycles_to_next_cmd = 1

        cycles.append(register)

    '''
    while addx_vals:
        val = addx_vals.pop(0)
        register += val
        cycles.append(register)
    '''

    #print(cycles)

    sig_strength_20 = cycles[20] * 20
    sig_strength_60 = cycles[60] * 60
    sig_strength_100 = cycles[100] * 100
    sig_strength_140 = cycles[140] * 140
    sig_strength_180 = cycles[180] * 180
    sig_strength_220 = cycles[220] * 220
    '''
    print(sig_strength_20)
    print("...{}... * 60 = {}".format(cycles[59:62], sig_strength_60))
    print(sig_strength_100)
    print(sig_strength_140)
    print(sig_strength_180)
    print(sig_strength_220)
    '''

    result = sig_strength_20 + sig_strength_60 + sig_strength_100
    result += sig_strength_140 + sig_strength_180 + sig_strength_220

    return result
    
def part_02(data):
    cycles = [1]
    register = 1
 
    addx_vals = []
    instructions = data.copy()
    cycles_to_next_cmd = 0

    while instructions or addx_vals:
        cmd = ["noop"]
        if instructions and cycles_to_next_cmd == 0:
            cmd = instructions.pop(0)
        else:
            cycles_to_next_cmd = min(cycles_to_next_cmd - 1, 0)
        
        if addx_vals:
            val = addx_vals.pop(0)
            register += val

        if cmd[0] == "noop":
            pass

        if cmd[0] == "addx":
            val = int(cmd[1])
            addx_vals.append(0)
            addx_vals.append(val)
            cycles_to_next_cmd = 1

        cycles.append(register)

    # generate pixels
    display = ["", "", "", "", "", ""]

    line = 0
    pixel = 0

    for cycle, val in enumerate(cycles[1:]):
        line = cycle // 40
        pixel = cycle % 40

        if (pixel < (val - 1)) or (pixel > (val + 1)):
            display[line] += ' '
        else:
            display[line] += '#'

    for line in display:
        print(line)



if __name__ == "__main__":
    main()
    
