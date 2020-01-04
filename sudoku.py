"""
Board Class, to hold game state and manipluations
Takes in the GRID, which is a list of lists, [9,9]
"""
theSet = {1,2,3,4,5,6,7,8,9}
class Board:
    def __init__(self, grid):
        #Grid holds our game state.
        self.grid = grid
        #Originals holds the opriginal state, allowing for reset.
        self.originals = grid
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
    def getNum(self, x, y):
        return self.grid[y][x]

    def getOrig(self, x, y):
        return self.originals[y][x]

    """
    Basic Setter function
    """
    def setNum(self, x, y, n):
        if self.isValid(x, y, n):
            self.grid[y][x] = n
        else:
            print("Invalid Move")

    """
    Resets the board to original state
    """
    def resetGrid(self):
        for c, i in enumerate(self.originals):
            for d, j in enumerate(i):
                self.grid[c][d] = j 

    """
    Basic Get functions for row and column. X and Y are reversed for the data structure used here.
    """
    def getRow(self, y):
        return self.grid[y]

    def getCol(self, x):
        toReturn = []
        for y in range(9):
            toReturn.append(self.grid[y][x])
        return toReturn    

    """
    Returns the 3x3 subsquare, alongside the top-left co-ordinates of that square
    """
    def getSqr(self, x, y):
        positionals = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for pos in positionals:
            if x in pos:
                cols = pos
            if y in pos:
                rows = pos
        toReturn = []
        tlxy = [(x, y) for x in cols for y in rows]
        for x in cols:
            for y in rows:
                toReturn.append(self.grid[y][x])
        return toReturn, tlxy
    
    def getPossibilities(self, x, y):
        sqrPoss = theSet - set(self.getSqr(x,y)[0])
        rowPoss = theSet - set(self.getRow(y))
        colPoss = theSet - set(self.getCol(x))
        poss_vals = list(sqrPoss.intersection(rowPoss).intersection(colPoss))
        #poss_vals = list((theSet - set(self.getSqr(x,y)[0])).intersection(theSet - set(self.getRow(y))).intersection(theSet - set(self.getCol(x))))
        return poss_vals

    """
    Tests for Validity of setting grid(x, y) to n.
    Using set subtraction, we whittle down from 1-9 to only numbers not present in row, column and s
    """
    def isValid(self, x, y, n):
        possibles = self.getPossibilities(x, y)
        if n in possibles:
            return True
        return False

    '''
    Solves all squares with only one possible number.
    '''
    def findSingle(self):
        for y in range(9):
            for x in range(9):
                if (self.grid[y][x]) == 0 and len(self.getPossibilities(x, y)) == 1:
                    if x == 4 and y == 1:
                        pass
                    print("The only possible number at position {}, {} is {}".format(x, y, self.getPossibilities(x, y)[0]))
                    self.setNum(x, y, self.getPossibilities(x, y)[0])
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
        for x, y in coords:
            if self.grid[y][x] == 0:
                toReturn.extend(self.getPossibilities(x, y))
        return set(toReturn)

    '''
    Inductive solver. This uses the possibilities present within all other squares in the row, col and sqr
    around our input tile to check if this tile has a possibility no other has. In that case, that must be
    what we input.
    '''
    def findMulti(self, x, y):
        if self.grid[y][x] == 0:
            tilePossSet = set(self.getPossibilities(x, y))

            rowPoss = self.findColRow(x, self.getRow(y))
            colPoss = self.findColRow(y, self.getCol(x))
            sqrCoords = self.getSqr(x, y)[1]
            sqrCoords.remove((x, y))
            sqrPoss = self.findSqr(sqrCoords)
            tilePoss = tilePossSet - rowPoss - colPoss - sqrPoss
            if len(tilePoss) == 1:
                value = tilePoss.pop()
                print("By induction, the only value possible at {}, {} is {}".format(x, y, value))
                self.setNum(x, y, value)
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