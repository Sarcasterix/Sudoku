import sys, re

theSet = {1,2,3,4,5,6,7,8,9}

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

"""
Board Class, to hold game state and manipluations
Takes in the GRID, which is a list of lists, [9,9]
"""
class Board:
    def __init__(self, grid):
        self.grid = grid

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
    Basic Setter function
    """
    def setNum(self, x, y, n):
        if self.isValid(x, y, n):
            self.grid[y][x] = n
        else:
            print("Invalid Move")

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
        poss_vals = list((theSet - set(self.getSqr(x,y)[0])).intersection(theSet - set(self.getRow(y))).intersection(theSet - set(self.getCol(x))))
        return poss_vals

    """
    Tests for Validity of setting grid(x, y) to n.
    Using set subtraction, we whittle down from 1-9 to only numbers not present in row, column and s
    """
    def isValid(self, x, y, n):
        if n in self.getPossibilities(x, y):
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



                    
def main(theBoard=board1, debug=0):
    i = 0
    testBoard = Board(theBoard)
    testBoard.draw()
    complete = False
    moves = 0     
    loops = 0
    while not complete:
        if loops > 81:
            print("Board not completable")
            break
        if not any(0 in row for row in testBoard.grid):
            complete = True
            print("Board complete! This took {} moves".format(moves))
        if testBoard.findSingle():
            testBoard.draw()
            moves+=1

        for x in range(9):
            for y in range(9):
                if testBoard.grid[y][x] == 0:
                    if testBoard.findMulti(x, y):
                        testBoard.draw()
                        moves += 1

        loops += 1
if __name__ == "__main__":
    main()