from copy import deepcopy

def main():
    with open("puzzle_05_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    state, moves = parse_data(data)

    state_01 = deepcopy(state)
    state_02 = deepcopy(state)

    answer_01 = part_01(state_01, moves)
    answer_02 = part_02(state_02, moves)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_data(data):
    state = [[] for _ in range(9)]
    moves = []

    parsing_state = True
    for line in data:
        line = line.strip()
        if not line:
            parsing_state = False
            continue

        # state
        if parsing_state:
            for i, c in enumerate(line):
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    index = (i // 4)
                    state[index].append(c)
            continue

        # moves
        split_line = line.split(' ')
        m = split_line[1]
        f = split_line[3]
        t = split_line[5]

        move = (int(m), int(f), int(t))
        moves.append(move)

    for i, s in enumerate(state):
        state[i] = state[i][::-1]

    '''
    for s in state:
        print(s)
    '''

    '''
    for move in moves:
        print(move)
    '''

    return state, moves


def part_01(state, moves):
    for move in moves:
        c = move[0]
        f = move[1] - 1
        t = move[2] - 1

        from_state = state[f]
        to_state = state[t]
        stack = from_state[-c:]
        stack = stack[::-1]

        from_state = from_state[:-c]
        to_state.extend(stack)

        state[f] = from_state
        state[t] = to_state

    result = ""
    for s in state:
        top = s[-1] if s else ""
        result += top

    return result

def part_02(state, moves):
    for move in moves:
        c = move[0]
        f = move[1] - 1
        t = move[2] - 1

        from_state = state[f]
        to_state = state[t]
        stack = from_state[-c:]

        from_state = from_state[:-c]
        to_state.extend(stack)

        state[f] = from_state
        state[t] = to_state

    result = ""
    for s in state:
        top = s[-1] if s else ""
        result += top

    return result



if __name__ == "__main__":
    main()
