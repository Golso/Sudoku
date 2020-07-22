from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP
from random import sample
import time

MARGIN = 20 # Pixels around the board
SIDE = 50 # Width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of the whole board
BASE = 3
WHOLE = BASE * BASE
TIMETICK = 0.05 # Smaller number -> faster work of algorithm


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

        board = self.__clear_board(board, 50)

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
                for r in range(row*3, (row+1)*3)
                for c in range(column*3, (column+1)*3)
            ]
        )


class SudokuUI(Frame):
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height = HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        newgame_button = Button(self, text="New game", command=self.__new_game)
        newgame_button.pack(fill=BOTH)
        solve_button = Button(self, text="Solve using backtracking algorithm", command=self.__solve_game)
        solve_button.pack(fill=BOTH)
        clear_button = Button(self, text="Clear answers", command=self.__clear_answers)
        clear_button.pack(fill=BOTH)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)
        root.update_idletasks()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("winner")
        self.canvas.delete("cursor")
        self.__draw_puzzle()

    def __new_game(self):
        self.game = SudokuGame()
        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("winner")
        self.canvas.delete("cursor")
        self.__draw_puzzle()

    def __solve_game(self):
        self.__clear_answers()
        self.__solve()

    def __cell_clicked(self, event):
        if self.game.game_over:
            return

        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()

            row, col = int((y-MARGIN)/SIDE), int((x-MARGIN)/SIDE)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.start_puzzle[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="cursor")

    def __draw_cursor_backtracking(self, row, col, color):
        if row >= 0 and col >= 0:
            x0 = MARGIN + col * SIDE + 1
            y0 = MARGIN + row * SIDE + 1
            x1 = MARGIN + (col + 1) * SIDE - 1
            y1 = MARGIN + (row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, tags="cursor")

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __draw_victory(self):
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")

        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y, text="Congratulations!", tags="winner", fill="white", font=("Arial", 25))

    def __find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def __solve(self):
        self.__draw_puzzle()
        find = self.__find_empty(self.game.puzzle)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.game.valid(self.game.puzzle, i, (row, col)):
                self.game.puzzle[row][col] = i
                self.__draw_puzzle()
                self.__draw_cursor_backtracking(row, col, "green")
                time.sleep(TIMETICK)

                if self.__solve():
                    return True

                self.game.puzzle[row][col] = 0
                self.__draw_puzzle()
                self.__draw_cursor_backtracking(row, col, "red")
                time.sleep(TIMETICK)

        return False


if __name__ == '__main__':
    game = SudokuGame()
    game.start()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 80))
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()
