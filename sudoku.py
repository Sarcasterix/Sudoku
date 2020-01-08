import copy
"""
Board Class, to hold game state and manipluations
Takes in the GRID, which is a list of lists, [9,9]
"""
theSet = {1,2,3,4,5,6,7,8,9}
class Board:
    def __init__(self, grid):
        #Grid holds our game state.
        self.originals = grid
        #Originals holds the opriginal state, allowing for reset.
        self.grid = copy.deepcopy(grid)
        self.finished = False
        self.lastMove = []
        '''
        TO DO Fully implement helper mode flag, to enable next-move, and to allow/block illegal lastMove.
        '''

    """
    Draws the board, so that we can see what we're doing
    """
    def draw(self):
        for i, row in enumerate(self.grid):
            toPrint = ""
            if i in [3, 6]:
                print(" ------+-------+------")
            for j, column in enumerate(row):
                if j in [3, 6]:
                    toPrint += ' |'
                toPrint+=" "+str(column)
            print(toPrint)
        print()

    """
    Basic getter functions
    """
    def getNum(self, col, row):
        return self.grid[row][col]

    def getOrig(self, col, row):
        return self.originals[row][col]

    """
    Basic Setter function
    """
    def setNum(self, col, row, n):
        if self.isValid(col, row, n):
            self.lastMove.append(((col, row), self.getNum(col, row)))
            self.grid[row][col] = n
        else:
            print("Invalid Move")

    """
    Set function to be exclusively used in undo-moves.
    """
    def undoNum(self, col, row, n):
        self.grid[row][col] = n

    """
    Resets the board to original state
    """
    def resetGrid(self):
        self.draw()
        for c, i in enumerate(self.originals):
            for d, j in enumerate(i):
                self.grid[c][d] = j 
        self.draw()

    """
    Basic Get functions for row and column. X and Y are reversed for the data structure used here.
    """
    def getRow(self, row):
        return self.grid[row]#, [(col, row) for col in range(9)]

    def getCol(self, col):
        toReturn = []
        #coords = []
        for row in range(9):
            toReturn.append(self.grid[row][col])
            #coords.append((col, row))
        return toReturn#, coords

    """
    Returns the 3x3 subsquare, alongside the top-left co-ordinates of that square
    """
    def getSqr(self, col, row):
        positionals = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for pos in positionals:
            if col in pos:
                cols = pos
            if row in pos:
                rows = pos
        toReturn = []
        coords = [(col, row) for col in cols for row in rows]
        for col in cols:
            for row in rows:
                toReturn.append(self.grid[row][col])
        return toReturn, coords
    
    def getPossibilities(self, col, row):
        sqrPoss = theSet - set(self.getSqr(col,row)[0])
        rowPoss = theSet - set(self.getRow(row))#[0])
        colPoss = theSet - set(self.getCol(col))#[0])
        poss_vals = list(sqrPoss.intersection(rowPoss).intersection(colPoss))
        #poss_vals = list((theSet - set(self.getSqr(x,y)[0])).intersection(theSet - set(self.getRow(y))).intersection(theSet - set(self.getCol(x))))
        return poss_vals

    """
    Tests for Validity of setting grid(col, row) to n.
    Using set subtraction, we whittle down from 1-9 to only numbers not present in row, column and s
    """
    def isValid(self, col, row, n):
        possibles = self.getPossibilities(col, row)
        if n in possibles:
            return True
        return False

    '''
    Solves all squares with only one possible number.
    '''
    def findSingle(self):
        for row in range(9):
            for col in range(9):
                if (self.grid[row][col]) == 0 and len(self.getPossibilities(col, row)) == 1:
                    print("The only possible number at position {}, {} is {}".format(col, row, self.getPossibilities(col, row)[0]))
                    self.setNum(col, row, self.getPossibilities(col, row)[0])
                    return True
        return False

    '''
    Helper Function for column possibility set generation
    Row is the index of the row we are looking at,
    x is the column of the square we are checking from.
    '''
    def findCol(self, x, row):
        toReturn = []
        for i in range(9):
            if i == row:
                continue
            if self.getNum(x, i) == 0:
                toReturn.extend(self.getPossibilities(x, i))
        return set(toReturn)
    '''
    Helper Function for row possibility set generation
    Col is the index of the column we are looking at,
    y is the row of the square we are checking from.
    '''
    def findRow(self, col, y):
        toReturn = []
        for i in range(9):
            if i == col:
                continue
            if self.getNum(i, y) == 0:
                toReturn.extend(self.getPossibilities(i, y))
        return set(toReturn)
        
    '''
    Helper Function for square possibility set generation
    '''
    def findSqr(self, coords):
        toReturn = []
        for col, row in coords:
            if self.grid[row][col] == 0:
                toReturn.extend(self.getPossibilities(col, row))
        return set(toReturn)

    '''
    Inductive solver. This uses the possibilities present within all other squares in the row, col and sqr
    around our input tile to check if this tile has a possibility no other has. In that case, that must be
    what we input.
    '''
    def findMulti(self, col, row):
        if self.getNum(col, row) == 0:
            tilePossSet = set(self.getPossibilities(col, row))

            rowPoss = self.findRow(col, row)
            colPoss = self.findCol(col, row)
            sqrCoords = self.getSqr(col, row)[1]
            sqrCoords.remove((col, row))
            sqrPoss = self.findSqr(sqrCoords)
            possibilities = []
            for l in [rowPoss, colPoss, sqrPoss]:
                if len(tilePossSet-l) == 1:
                    possibilities.append((tilePossSet-l).pop())
            if len(set(possibilities)) == 1:
                value = possibilities.pop()
                print("By induction, the only value possible at {}, {} is {}".format(col, row, value))
                self.setNum(col, row, value)
                return True   
            #if len(tilePoss) == 1:
      
        return False

    
    def isFinished(self):
        if not any(0 in row for row in self.grid):
            print("Board complete!")
            self.finished = True
            return True
        return False