import collections
import math

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diagonal_1 = [rows[i] + cols[i] for i in range(len(row_units))]
diagonal_2 = [rows[i] + cols[::-1][i] for i in range(len(row_units))]


square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
unitlist.append(diagonal_1)
unitlist.append(diagonal_2)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

        Args:
            grid: Sudoku grid in string form, 81 characters long
        Returns:
            Sudoku grid in dictionary form:
            - keys: Box labels, e.g. 'A1'
            - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
        """

    all_digits = '123456789'

    if len(grid) != 81:
        raise ValueError("The length of the parameter must be 81")

    gridDict = dict()

    for item in zip(boxes, grid):
        gridDict[item[0]] = item[1] if item[1] != '.' else all_digits

    return gridDict

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_values = {unit_key for (unit_key, unit_value) in values.items() if len(unit_value) == 1}

    for box in solved_values:

        box_value = values[box]

        for peer in peers[box]:
            if values[peer] != box_value:
                values[peer] = values[peer].replace(box_value, '')

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    keep_going = True

    while keep_going:

        keep_going = False

        solved_boxes_before = len([unit_key for unit_key in values.keys() if len(values[unit_key]) == 1])

        for unit in unitlist:

            all_unit_digits = {unit_key: unit_value for (unit_key, unit_value) in values.items() if
                               unit_key in unit and len(unit_value)}

            all_unit_digits_str = ''.join(all_unit_digits.values())

            digit_counter = {digit_key for (digit_key, digit_count) in collections.Counter(all_unit_digits_str).items()
                if digit_count == 1}

            for digit_key in digit_counter:
                unit_keys = []
                for unit_key in unit:

                    if len(values[unit_key]) > 1 and values[unit_key].find(digit_key) > -1:
                        unit_keys.append(unit_key)

                    for u in unit_keys:
                        values[u] = digit_key

        solved_boxes_after = len([unit_key for unit_key in values.keys() if len(values[unit_key]) == 1])

        keep_going = solved_boxes_before != solved_boxes_after

    return values

def reduce_puzzle(values):


    stalled = False
    while not stalled:

        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

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

