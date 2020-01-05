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
        """
        Initialise our variables for use throughout the class
        """
        self.board = board
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = -1, -1

        self.__initUI()
    
    def __initUI(self):
        """
        Initialisation function for our UI, setting up the space we'll be working in.
        """
        #Set the name of the window
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        #Build a canvas to draw on
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        #Add a button at the base of the screen to reset the game
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.clearBoard)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        #Call our draw_grid function
        self.drawGrid()
        #draw the puzzle on the grid
        self.drawGame()

        #Get our hooks for mouse and keyboard interactions
        self.canvas.bind("<Button-1>", self.onCellClick)
        self.canvas.bind("<Key>", self.onKeyPress)

    def drawGrid(self):
        """
        Draws 9x9 grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"
            #Draw the vertical lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            #Draw the horizontal lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def drawGame(self):
        """
        Draws the numbers of the game onto the grid we are displaying
        """
        #Clear all displayed numbers, just to be safe
        self.canvas.delete("numbers")
        #For all spaces in our grid
        for row in range(9):
            for col in range(9):
                #Get the current game state for the tile we're working on
                tile = self.board.getNum(col, row)
                #If we have a number to write
                if tile != 0:
                    #Get our co-ordinates
                    x = MARGIN + col * SIDE + SIDE / 2
                    y = MARGIN + row * SIDE + SIDE / 2
                    #Check if we've changed this number from base game-state
                    original = self.board.getOrig(col, row)
                    #Draw number black if original, blue/green otherwise
                    color = "black" if tile == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=tile, tags="numbers", fill=color
                    )

    def clearBoard(self):
        """
        Wipe all written answers from the board
        """
        self.board.resetGrid()
        self.canvas.delete("victory")
        self.drawGame()

    def onCellClick(self, event):
        """
        Action for click event.
        """
        #No point doing anything if we've already finished the game
        if self.board.finished:
            return
        #Get our mouse co-ordinates
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
        #Call our outline method, as there's been a click event
        self.outlineCell()

    def outlineCell(self):
        """
        Draws a border around the cell we currently have selected
        """
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

    def onKeyPress(self, event):
        """
        Action for keypress event.
        """        
        #No point doing anything if we've already finished the game
        if self.board.finished:
            return
        #If we have a row and column selected, and the key pressed is a number
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            #Update our gamestate with the key pressed
            self.board.setNum(self.col, self.row, int(event.char))
            #Deselect our column and row
            self.col, self.row = -1, -1
            #Redraw the board
            self.drawGame()
            #clear the outline on the Cell
            self.outlineCell()
            #If this was the winning move, draw our completion image
            if self.board.isFinished():
                self.__draw_victory()

    def __draw_victory(self):
        """
        Draw the victory condition
        """
        #Get our x, y co-ords for drawing
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        #Build an oval to draw
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        #Draw text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32))
                    
def main(theBoard=board1, debug=0):
    """
    Main loop, to run the game.
    """
    #Build our gamestate from loaded variable
    testBoard = Board(theBoard)
    testBoard.draw()

    #Start tkinter
    root = Tk()

    #Set our GUI up
    SudokuGui(root, testBoard)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    #Lets
    root.mainloop()


if __name__ == "__main__":
    main()