from random import sample

base = 3
side = base * base


# pattern for a baseline valid solution
def pattern(r, c): return (base*(r % base)+r//base+c) % side


# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s): return sample(s, len(s))


def make_board():
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    board = clear_board(board, 40)

    return board


def clear_board(board, number):
    i = 81-number
    for p in sample(range(81), i):
        board[p // 9][p % 9] = 0
    return board


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None


def valid(board, number, position):
    # check row
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False

    # check column
    for i in range(len(board[0])):
        if board[i][position[1]] == number and position[0] != i:
            return False

    # check box
    x = position[1]//3
    y = position[0]//3

    for i in range(y * 3, y * 3 + 3):
        for j in range(x * 3, x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False