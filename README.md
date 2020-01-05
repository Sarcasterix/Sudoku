# Sudoku
This is a program to allow for the importing, playing and solving of Sudoku.
## Files
### sudoku.py
This contains the basic board state, alongside manipulation functions.
The main method within this file allows for testing of game logic, through three included games.
Both Implicit and Explicit solution algorithms are included. Explicit solutions are found when there is only a single allowable number for a given space. Implicit solutions are found when only one of the multiple possible numbers within a space are not possible within any others in the Row, Column or Square being checked.

### gui.py
This is the main method, which runs the application.
This file draws the GUI for the program, and allows for user interaction.

### readgame.py
This contains the logic for reading gamefiles (*.sud).
Games can be stored in the following string types:
    81-character single line string
    9 lines of 9-character strings
Any "." characters are automatically convered to "0"

