from SudokuGame import SudokuGame
from SudokuUI import SudokuUI, WIDTH, HEIGHT
from tkinter import Tk


if __name__ == '__main__':
    game = SudokuGame()
    game.start()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 105))
    root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
    root.mainloop()