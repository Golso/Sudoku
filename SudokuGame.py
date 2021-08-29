from random import sample

BASE = 3
WHOLE = BASE * BASE


class SudokuGame(object):
    def __init__(self):
        self.start_puzzle = self.__make_board()

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    # pattern for a baseline valid solution
    def __pattern(self, r, c):
        return (BASE * (r % BASE) + r // BASE + c) % WHOLE

    # randomize rows, columns and numbers (of valid base pattern)
    def __shuffle(self, s):
        return sample(s, len(s))

    def __make_board(self):
        rBase = range(BASE)
        rows = [g * BASE + r for g in self.__shuffle(rBase) for r in self.__shuffle(rBase)]
        cols = [g * BASE + c for g in self.__shuffle(rBase) for c in self.__shuffle(rBase)]
        nums = self.__shuffle(range(1, BASE * BASE + 1))

        # produce board using randomized baseline pattern
        board = [[nums[self.__pattern(r, c)] for c in cols] for r in rows]

        board = self.__clear_board(board, 40)

        return board

    def __clear_board(self, board, number):
        i = 81 - number
        for p in sample(range(81), i):
            board[p // 9][p % 9] = 0
        return board

    def valid(self, board, number, position):
        # check row
        for i in range(len(board[0])):
            if board[position[0]][i] == number and position[1] != i:
                return False

        # check column
        for i in range(len(board[0])):
            if board[i][position[1]] == number and position[0] != i:
                return False

        # check box
        x = position[1] // 3
        y = position[0] // 3

        for i in range(y * 3, y * 3 + 3):
            for j in range(x * 3, x * 3 + 3):
                if board[i][j] == number and (i, j) != position:
                    return False

        return True

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block([self.puzzle[row][column] for row in range(9)])

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )
