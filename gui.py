from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import sys, re
from sudoku import Board

board1 = [[2,1,0,3,8,5,4,6,9],
          [3,8,5,4,6,9,7,1,2],
          [4,9,6,7,2,1,8,0,5],
          [5,0,4,8,1,6,9,7,3],
          [6,3,9,5,4,7,2,8,1],
          [8,7,1,2,0,3,5,4,6],
          [7,6,2,1,5,8,0,9,4],
          [9,5,0,6,7,4,1,2,8],
          [1,4,8,9,3,2,6,5,0]]

board2 = [[2,1,0,0,0,0,4,0,0],
          [3,8,0,4,0,0,7,0,2],
          [0,0,0,7,2,0,0,0,0],
          [0,2,4,8,0,6,9,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,1,2,0,3,5,4,0],
          [0,0,0,0,5,8,0,0,0],
          [9,0,3,0,0,4,0,2,8],
          [0,0,8,0,0,0,0,5,7]]

board3 = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
          [6, 8, 0, 0, 7, 0, 0, 9, 0],
          [1, 9, 0, 0, 0, 4, 5, 0, 0],
          [8, 2, 0, 1, 0, 0, 0, 4, 0],
          [0, 0, 4, 6, 0, 2, 9, 0, 0],
          [0, 5, 0, 0, 0, 3, 0, 2, 8],
          [0, 0, 9, 3, 0, 0, 0, 7, 4],
          [0, 4, 0, 0, 5, 0, 0, 3, 6],
          [7, 0, 3, 0, 1, 8, 0, 0, 0]]

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  

class SudokuGui(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, board):
        self.board = board
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
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
        #Clear all displayed numbers, just to be safe
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                tile = self.board.getNum(j, i)
                if tile != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.board.getOrig(j, i)
                    color = "black" if tile == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=tile, tags="numbers", fill=color
                    )

    def __clear_answers(self):
        self.board.resetGrid()
        self.canvas.delete("victory")
        self.__draw_puzzle()

    def __cell_clicked(self, event):
        if self.board.finished:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.board.getNum(col, row) == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __key_pressed(self, event):
        if self.board.finished:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.board.setNum(self.col, self.row, int(event.char))  #game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.board.isFinished():
                self.__draw_victory()

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32))


                    
def main(theBoard=board1, debug=0):
    testBoard = Board(theBoard)
    testBoard.draw()

    root = Tk()

    SudokuGui(root, testBoard)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()

if __name__ == "__main__":
    main()