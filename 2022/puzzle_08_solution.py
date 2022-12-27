
def main():
    data = parse_input()

    answer_01 = part_01(data)
    answer_02 = part_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))



def parse_input():
    data = None
    
    with open("puzzle_08_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    grid = []
    for line in data:
        line = line.strip()
        row = []
        for c in line:
            n = int(c)
            row.append(n)
        grid.append(row)
    
    return grid


def part_01(data):
    result = 0
    seen_trees = set()

    x_max = len(data[0]) - 1
    y_max = len(data) - 1
    
    for i in range(x_max + 1):
        top_max = -1
        bottom_max = -1

        for j in range(y_max + 1):
            top_val = data[j][i]
            bottom_val = data[-(j+1)][i]

            if top_val > top_max:
                x = i
                y = j
                seen_trees.add((x, y))
                top_max = top_val

            if bottom_val > bottom_max:
                x = i
                y = y_max - j
                seen_trees.add((x, y))
                bottom_max = bottom_val

    # left/right
    for i in range(y_max + 1):
        left_max = -1
        right_max = -1    

        for j in range(x_max + 1):
            left_val = data[i][j]
            right_val = data[i][-(j+1)]

            if left_val > left_max:
                x = j
                y = i
                seen_trees.add((x, y))
                left_max = left_val

            if right_val > right_max:
                x = x_max - j
                y = i
                seen_trees.add((x, y))
                right_max = right_val

    result = len(seen_trees)
    return result


def part_02(data):
    result = 0

    x_max = len(data[0]) - 1
    y_max = len(data) - 1
    
    def scenic_score(x, y):
        score = 1
        tree = data[y][x]

        # up
        up_count = 0
        n = y - 1
        while n >= 0:
            up_count += 1
            if data[n][x] >= tree:
                break
            n -= 1
        
        # down
        down_count = 0
        n = y + 1
        while n <= y_max:
            down_count += 1
            if data[n][x] >= tree:
                break
            n += 1
            
        # left
        left_count = 0
        n = x - 1
        while n >= 0:
            left_count += 1
            if data[y][n] >= tree:
                break
            n -= 1
            
        # right
        right_count = 0
        n = x + 1
        while n <= x_max:
            right_count += 1
            if data[y][n] >= tree:
                break
            n += 1

        left_mult = max(left_count, 0)
        right_mult = max(right_count, 0)
        up_mult = max(up_count, 0)
        down_mult = max(down_count, 0)
        
        score = left_mult * right_mult * up_mult * down_mult
        return score

    scores = [[0 for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    for x in range(len(data[0])):
        for y in range(len(data)):
            score = scenic_score(x, y)
            scores[y][x] = score
            if score > result:
                result = score

    #for score in scores:
    #    print(score)
    return result


if __name__ == "__main__":
    main()
