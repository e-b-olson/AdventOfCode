from copy import deepcopy

DEBUG = False

def debug_print(*args):
    if DEBUG:
        print(args)


def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None

    with open("puzzle_09_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    return data



def part_01(data):
    tail_set = set()

    head = [0, 0]
    tail = [0, 0]

    tail_set.add(tuple(tail))

    for cmd in data:
        cmd = cmd.strip()
        if not cmd or cmd[0] == '#':
            continue
        
        cmd = cmd.split(" ")
        d = cmd[0]
        c = int(cmd[1])

        for step in range(c):
            if d == 'U':
                head[1] += 1
                if head[1] - tail[1] > 1:
                    tail[1] = head[1] - 1
                    tail[0] = head[0]
            if d == 'D':
                head[1] -= 1
                if tail[1] - head[1] > 1:
                    tail[1] = head[1] + 1
                    tail[0] = head[0]
            if d == 'L':
                head[0] -= 1
                if tail[0] - head[0] > 1:
                    tail[0] = head[0] + 1
                    tail[1] = head[1]
            if d == 'R':
                head[0] += 1
                if head[0] - tail[0] > 1:
                    tail[0] = head[0] - 1
                    tail[1] = head[1]

            tail_set.add(tuple(tail))
                
    #print(tail_set)
    return len(tail_set)


def print_rope(rope):
    if not DEBUG:
        return

    grid = [['.' for _ in range(28)] for _ in range(28)]
    min_x = -11
    min_y = -5
    
    for i, n in enumerate(rope):
        x = -min_x + n[0]
        y = -min_y + n[1]
        grid[y][x] = str(i)

    for row in grid[::-1]:
        print(''.join(row))

    string = input()



def part_02(data):
    tail_set = set()

    rope = [[0, 0] for _ in range(10)]

    #tail_set.add(tuple(rope[-1]))

    def simulate(d):
        for i, n in enumerate(rope):
            if i == 0:
                if d == 'U':
                    rope[i][1] += 1
                if d == 'D':
                    rope[i][1] -= 1
                if d == 'L':
                    rope[i][0] -= 1
                if d == 'R':
                    rope[i][0] += 1
                continue

            prev = rope[i - 1].copy()
            node = rope[i].copy()

            x_delta = prev[0] - node[0]
            y_delta = prev[1] - node[1]

            #print(rope)
            #print("dx: {}\tdy: {}".format(x_delta, y_delta))

            x_step = 1 if x_delta > 0 else -1 if x_delta < 0 else 0
            y_step = 1 if y_delta > 0 else -1 if y_delta < 0 else 0

            if abs(x_delta) > 1 or abs(y_delta) > 1:
                node[0] += x_step
                node[1] += y_step

            '''
            if x_delta == 2 and y_delta == 0:
                node[0] += 1

            if x_delta == -2 and y_delta == 0:
                node[0] -= 1

            if y_delta == 2 and x_delta == 0:
                node[1] += 1

            if y_delta == -2 and x_delta == 0:
                node[1] -= 1
            '''

            '''
            if x_delta > 1 and y_delta > 0:
                node[0] += 1
                node[1] += 1
            if x_delta > 1 and y_delta < 0:
                node[0] += 1
                node[1] -= 1
            if x_delta < -1 and y_delta > 0:
                node[0] -= 1
                node[1] += 1
            if x_delta < -1 and y_delta < 0:
                node[0] -= 1
                node[1] -= 1

            if y_delta > 1 and x_delta > 0:
                node[0] += 1
                node[1] += 1
            if y_delta > 1 and x_delta < 0:
                node[0] -= 1
                node[1] += 1
            if y_delta < -1 and x_delta > 0:
                node[0] += 1
                node[1] -= 1
            if y_delta < -1 and x_delta < 0:
                node[0] -= 1
                node[1] -= 1
            '''
            
            rope[i] = node
            #print_rope(rope)

    for cmd in data:
        cmd = cmd.strip()
        if not cmd or cmd[0] == '#':
            continue
        
        cmd = cmd.split(" ")
        d = cmd[0]
        c = int(cmd[1])

        for step in range(c):
            simulate(d)
            tail_set.add(tuple(rope[-1]))
            #print_rope(rope)
            #print(rope)
                
    #print(tail_set)

    def print_tail_set():
        if not DEBUG:
            return

        min_x = 2**16
        max_x = -min_x
        min_y = 2**16
        max_y = -min_y

        for coord in tail_set:
            min_x = min(min_x, coord[0])
            max_x = max(max_x, coord[0])
            min_y = min(min_y, coord[1])
            max_y = max(max_y, coord[1])

        x_count = (max_x - min_x) + 1
        y_count = (max_y - min_y) + 1

        grid = [['.' for _ in range(x_count)] for _ in range(y_count)]

        for coord in tail_set:
            x = -min_x + coord[0]
            y = -min_y + coord[1]
            grid[y][x] = '#'

        for row in grid[::-1]:
            print(''.join(row))

    print_tail_set()
    return len(tail_set)



if __name__ == "__main__":
    main()
