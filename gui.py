from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT, filedialog
import sys, re
from sudoku import Board
from readgame import ReadGame

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
        Initialisation function for our UI, 
        setting up the space we'll be working in.
        """
        #Set the name of the window
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        top = Frame(self)
        bottom = Frame(self)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM)#, fill=BOTH, expand=True)
        #Build a canvas to draw on
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(in_=top, fill=BOTH, side=TOP)
        #Add a button at the base of the screen to reset the game
        clearButton = Button(bottom,
                              text="Clear answers",
                              #width=WIDTH//2,
                              command=self.clearBoard)
        nextButton = Button(bottom,
                              text="Next Move",
                              #width=(WIDTH//2),
                              command=self.nextMove)
        undoButton = Button(bottom,
                              text="Undo",
                              command=self.undoMove)
        finishButton = Button(bottom,
                                text="Finish Game",
                                command=self.finishGame)
        clearButton.pack(in_=bottom, side=LEFT)
        nextButton.pack(in_=bottom, side=LEFT)
        undoButton.pack(in_=bottom, side=LEFT)
        finishButton.pack(in_=bottom, side=LEFT)
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
            if i % 3 == 0:
                colour = "black"
                lineWidth = 3
                x0 = MARGIN  + i * SIDE
                x1 = MARGIN + i * SIDE
            else:
                colour = "gray"
                lineWidth = 2
                x0 = MARGIN + i * SIDE                
                x1 = MARGIN + i * SIDE
            #Draw the vertical lines
            y0 = MARGIN
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, width = lineWidth, fill=colour)
            #Draw the horizontal lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, width = lineWidth, fill=colour)
        for i in range(0, 10, 3):
            colour = "black"
            lineWidth = 3
            x0 = MARGIN  + i * SIDE
            y0 = MARGIN -1
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN +2
            self.canvas.create_line(x0, y0, x1, y1, width = lineWidth, fill=colour)
            #Draw the horizontal lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, width = lineWidth, fill=colour)

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
                    colour = "black" if tile == original else "green"
                    self.canvas.create_text(
                        x, y, text=tile, tags="numbers", fill=colour
                    )

    def clearBoard(self):
        """
        Wipe all written answers from the board
        """
        print("Clear Answers Clicked")
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
                self.drawWin()

    def drawWin(self):
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
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32))

    """
    Next move button, fills in the next tile which has only one possible number
    """
    def nextMove(self):
        #Running findSingle updates board, otherwise returns false
        if not self.board.findSingle():
            #Iterate over board
            for row in range(9):
                for col in range(9):
                    #findMulti also updates game state, we can break on return
                    if self.board.findMulti(col, row):
                        break
                else:
                    continue # Safeguard to break nested for loop
                break
        self.drawGame()

        if self.board.isFinished():
                self.drawWin()

    def finishGame(self):
        while(not self.board.isFinished()):
            self.nextMove()
        self.drawWin

    def undoMove(self):
        if len(self.board.lastMove) >= 1:
            print(self.board.lastMove)
            ((col, row), old) = self.board.lastMove.pop(-1)
            print(col, row, old)
            print(self.board.lastMove)
            self.board.undoNum(col, row, old)
            self.drawGame()
                    
def main():
    """
    Main loop, to run the game.
    """
    #Build our gamestate from loaded variable


    #Start tkinter
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir = "./gameFiles",title = "Select file",filetypes = (("Sudoku Files","*.sud"),("all files","*.*")))
    theGame = Board(ReadGame(root.filename).board)
    theGame.draw()
    #Set our GUI up
    SudokuGui(root, theGame)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    #Lets
    root.mainloop()

if __name__ == "__main__":
    main()