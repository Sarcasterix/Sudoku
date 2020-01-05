"""
Class definition for the importing of sudoku games.
Games can be stored in the following string types:
    81-character single line string
    9 lines of 9-character strings
"""
import re

class ReadGame:
    def __init__(self, fileName):
        self.lines = []
        self.board = []
        with open(fileName, 'r') as f:
            for line in f:
                self.lines.append(line.strip())
        if len(self.lines) == 1:
            inString = self.lines[0]
            if "." in inString:
                inString = re.sub(r'\.', '0', inString)
                for row in [inString[i:i+9] for i in range(0, len(inString), 9)]:
                    self.board.append([int(c) for c in row])           
        elif len(self.lines) == 9:
            for line in self.lines:
                if "." in line:
                    line = re.sub(r'.', '0', line)
                self.board.append([int(c) for c in line])
        else:
            print("Please enter a file in one of the allowable formats")