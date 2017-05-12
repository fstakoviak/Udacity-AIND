# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins problem consists in finding all units that belongs in the same peer that satisfies the condition of having exactly two possible values for their respective unit. 
Applying constrain propagation, first it is necessary to select all units that have exactly two possible values (candidates).
After that, all candidates are analyzed and checked if they are false candidates or not, by checking into each unit peer of the candidate if there is another unit with the same two possible values.
Selecting those units, it is eliminate from the other units of the same peer the possible values that match any of the naked twins values.
The process is repeated until no other replacement is made.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku consists in guarantee that all diagonal values of the grid is unique.
Applying constrain propagation, it is necessary to map all diagonal units and add them to the unitlist.
In this way, the peers of each unit will also contain the diagonal units if they are under any diagonal coverage.
If all the conditions above are respected it is possible to assure that diagonal sudokus are covered by the same rules of traditional sudoku.