from utils import *

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False;
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    box_val_len, box_key = min([(len(values[s]), s) for s in boxes if (len(values[s]) > 1)])

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[box_key]:
        new_sudoku = values.copy()
        new_sudoku[box_key] = digit
        values_new_sudoku = search(new_sudoku)
        if values_new_sudoku:
            return values_new_sudoku



