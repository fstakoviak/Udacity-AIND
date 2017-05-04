from function import *

# grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# values = grid_values(grid1)
# values = reduce_puzzle(values)

# display(values)


grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid2 = '..5.......32..695..8..1..23.2.........7...4.........6.54..2..8..963..27.......5..'
grid2 = '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
values = grid_values(grid2)

values = search(values)

display(values)


s = ''
for r in rows:
    for c in cols:
        s += values[(r+c)] + ','
print (s)

print (units['A1'])