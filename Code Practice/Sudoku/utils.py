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

# unitlist.append(diagonal_1)
# unitlist.append(diagonal_2)

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

    # for unit_key in unsolved_boxes:
    #     for unit_boxes in units[unit_key]:
    #         if len([k for k in unit_boxes if len(values[k]) > 1]) == 1:
    #             box_current_value = values[unit_key]
    #             unit_values = [v for (k, v) in values.items() if k in unit_boxes and k != unit_key]
    #             print('===========')
    #             print (unit_key)
    #             print (box_current_value)
    #             print (unit_boxes)
    #             print(unit_values)
    #             print('=')
    #             box_new_value = [k for k in list(box_current_value) if k not in unit_values][0]
    #             print(box_new_value)
    #             print('===========')
    #
    #             values[unit_key] = box_new_value
    #
    #             break

    stalled = False
    while not stalled:

        solved_boxes_before = [unit_key for unit_key in boxes if len(values[unit_key]) > 1]

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

        solved_boxes_after = [unit_key for unit_key in boxes if len(values[unit_key]) > 1]

        stalled = solved_boxes_after == solved_boxes_after

    return values

def reduce_puzzle(values):


    stalled = False
    while not stalled:

        # Check how many boxes have a determined value
        solved_values_before = len([box for box in boxes if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        # values = naked_twins(values)


        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in boxes if len(values[box]) == 0]):
            return False

    return values

def search(values):

    print('called')

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


def naked_twins(values):

    twins_candidate = set([unit_key for (unit_key, unit_value) in values.items() if len(unit_value) == 2])

    while len(twins_candidate) > 1:

        x_key = twins_candidate.pop()
        x_value = values[x_key]

        # x_candidates = [unit_key for (unit_key, unit_value) in twins_candidate.items() if unit_value == x_value]
        #
        # if len([box for box in peers[x_key] if values[box] == x_value]) == 2:
        #     for box in x_unit:
        #         if len(values[box]) > 1 and values[box] != x_value:
        #             for digit in x_value:
        #                 values[box] = values[box].replace(digit, '')
        #
        if len(x_value) == 2:
            for x_unit in units[x_key]:
                if len([box for box in x_unit if values[box] == x_value]) == 2:
                    for box in x_unit:
                        if len(values[box]) > 1 and values[box] != x_value:
                            for digit in x_value:
                                values[box] = values[box].replace(digit, '')

        # for peer_boxes in peers[x_key]:
        #
        #     x_candidate_twins = [box for box in twins_candidate if values[box] == x_value]
        #     if len(x_candadidate_twins) == 1:
        #         for box in peer_boxes:
        #             if len(values[box]) > 1 and values[box] != x_value:
        #                 # print(x_value)
        #                 # print(values[box])
        #                 for digit in x_value:
        #                     values[box] = values[box].replace(digit, '')
        #                 # print(values[box])
        #

            # if len([unit_key for unit_key in unit_boxes if values[unit_key] == x_value]) == 2:
            #     for box in unit_boxes:
            #         if len(values[box]) > 1 and values[box] != x_value:
            #             # print(x_value)
            #             # print(values[box])
            #             for digit in x_value:
            #                 values[box] = values[box].replace(digit, '')
            #             # print(values[box])

        # if len(x_candidates) > 0:
        #     for unit_boxes in units[x_key]:
        #
        #         if len([k for k in unit_boxes if k in x_candidates]) == 1:
        #             for box in unit_boxes:
        #                 if len(values[box]) > 1 and values[box] != x_value:
        #                     print (x_value)
        #                     print (values[box])
        #                     for digit in x_value:
        #                         values[box] = values[box].replace(digit, '')
        #                     print(values[box])

                # y_not_twins = [k for k in y if k not in x_candidates and k != x_key and len(values[k]) > 1]
                #
                # for z in y_not_twins:
                #     for digit in x_value:
                #         values[z] = values[z].replace(digit, '')

    return values
