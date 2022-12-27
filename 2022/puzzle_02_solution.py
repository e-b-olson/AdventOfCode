
def main():
    with open("puzzle_02_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    answer_01 = calculate_score_01(data)
    answer_02 = calculate_score_02(data)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))

def calculate_score_01(data):
    '''
    A: ROCK
    B: PAPER
    C: SCISSORS

    X: ROCK
    Y: PAPER
    Z: SCISSORS

    === SCORE ===
    ROCK:     1
    PAPER:    2
    SCISSORS: 3

    WIN       6
    LOSE      0
    DRAW      3
    '''

    matrix = {
        'A': {'X': 1+3, 'Y': 2+6, 'Z': 3+0},
        'B': {'X': 1+0, 'Y': 2+3, 'Z': 3+6},
        'C': {'X': 1+6, 'Y': 2+0, 'Z': 3+3}}

    result = 0

    for round in data:
        them = round[0]
        me = round[2]

        result += matrix[them][me]

    return result

def calculate_score_02(data):
    '''
    A: ROCK
    B: PAPER
    C: SCISSORS

    X: LOSE
    Y: DRAW
    Z: WIN

    === SCORE ===
    ROCK:     1
    PAPER:    2
    SCISSORS: 3

    WIN       6
    LOSE      0
    DRAW      3
    '''

    matrix = {
        'A': {'X': 0+3, 'Y': 3+1, 'Z': 6+2},
        'B': {'X': 0+1, 'Y': 3+2, 'Z': 6+3},
        'C': {'X': 0+2, 'Y': 3+3, 'Z': 6+1}}

    result = 0

    for round in data:
        them = round[0]
        me = round[2]

        result += matrix[them][me]

    return result


if __name__ == "__main__":
    main()
