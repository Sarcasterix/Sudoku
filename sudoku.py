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
        '''
        TO DO Fully implement helper mode flag, to enable next-move, and to allow/block illegal moves.
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
            self.grid[row][col] = n
        else:
            print("Invalid Move")

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
        return self.grid[row]

    def getCol(self, col):
        toReturn = []
        for row in range(9):
            toReturn.append(self.grid[row][col])
        return toReturn    

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
        sqrCoords = [(col, row) for col in cols for row in rows]
        for col in cols:
            for row in rows:
                toReturn.append(self.grid[row][col])
        return toReturn, sqrCoords
    
    def getPossibilities(self, col, row):
        sqrPoss = theSet - set(self.getSqr(col,row)[0])
        rowPoss = theSet - set(self.getRow(row))
        colPoss = theSet - set(self.getCol(col))
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
                    if col == 4 and row == 1:
                        pass
                    print("The only possible number at position {}, {} is {}".format(col, row, self.getPossibilities(col, row)[0]))
                    self.setNum(col, row, self.getPossibilities(col, row)[0])
                    return True
        return False

    '''
    Helper Function for column and row possibility set generation
    '''
    def findColRow(self, xy, toCheck):
        toReturn = []
        for c, i in enumerate(toCheck):
            if c == xy:
                continue
            if i == 0:
                toReturn.extend(self.getPossibilities(xy, c))
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
        if self.grid[row][col] == 0:
            tilePossSet = set(self.getPossibilities(col, row))

            rowPoss = self.findColRow(col, self.getRow(row))
            colPoss = self.findColRow(row, self.getCol(col))
            sqrCoords = self.getSqr(col, row)[1]
            sqrCoords.remove((col, row))
            sqrPoss = self.findSqr(sqrCoords)
            tilePoss = tilePossSet - rowPoss - colPoss - sqrPoss
            if len(tilePoss) == 1:
                value = tilePoss.pop()
                print("By induction, the only value possible at {}, {} is {}".format(col, row, value))
                self.setNum(col, row, value)
                return True         
        else:
            print("The given tile is already filled")
        return False
    
    def isFinished(self):
        if not any(0 in row for row in self.grid):
            print("Board complete!")
            self.finished = True
            return True
        return False