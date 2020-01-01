# -*- coding: utf-8 -*-
"""

"""

'''
==================
KUROSU solver
==================

A simple python script to solve 6x6 KUROSU puzzles
Written by RR on 30 Dec 19 using Spyder Editor (Python 3.7)

==================
How it works
==================

Set up array including a valid lines array
define input module to allo manual entry of a puzzle grid
define a function to check one line of the input puzzle grid against valid lines

Compare/decide algorithm for each line (row or column):
-see which valid lines this line *could* be and make a new array of these valid lines
-compare all entries in the valid lines and see if any are common to all valid lines
-if an x or o is common to all valid lines, then this entry must be that x or o
-if that's the case, write a change to the puzzle grid

There are two compare/decide functions - one for rows, one for columns. 
They're the same except the columns one transposes the array before and after the comparison

Finally, there is a main loop which:
-performs the compare/decide function for each row
-performs the compare/decide function for each column
-iterates until the grid is stable between iterations

NB.The source of the sample puzzles is the Daily Mail article here:
https://www.dailymail.co.uk/news/article-5774235/Prepare-Kurosu-ed-latest-brilliant-puzzle-Japan.html

'''


# =========================================== 
# Set up and initialise with some arrays
# ===========================================

import numpy as np

# a blank array that the input_grid function can populate

initial_grid = np.array([['?', '?', '?', '?', '?', '?'], 
                         ['?', '?', '?', '?', '?', '?'],
                         ['?', '?', '?', '?', '?', '?'],
                         ['?', '?', '?', '?', '?', '?'],
                         ['?', '?', '?', '?', '?', '?'],
                         ['?', '?', '?', '?', '?', '?']], dtype=object)

# The array of valid six-character lines - can be rows or columns

valid_solutions = np.array([['o', 'o', 'x', 'o', 'x', 'x'],
                            ['o', 'o', 'x', 'x', 'o', 'x'],
                            ['o', 'x', 'o', 'o', 'x', 'x'],
                            ['o', 'x', 'o', 'x', 'o', 'x'],
                            ['o', 'x', 'o', 'x', 'x', 'o'],
                            ['o', 'x', 'x', 'o', 'o', 'x'],
                            ['o', 'x', 'x', 'o', 'x', 'o'],
                            ['x', 'o', 'o', 'x', 'o', 'x'],
                            ['x', 'o', 'o', 'x', 'x', 'o'],
                            ['x', 'o', 'x', 'o', 'o', 'x'],
                            ['x', 'o', 'x', 'o', 'x', 'o'],
                            ['x', 'o', 'x', 'x', 'o', 'o'],
                            ['x', 'x', 'o', 'o', 'x', 'o'],
                            ['x', 'x', 'o', 'x', 'o', 'o']], dtype=object)
                            
# set up a sample puzzle grid, to be solved. This is an alternative to using the input_grid Fn

sample_grid_hard = np.array([['?', '?', 'o', '?', 'o', 'o'],
                             ['?', '?', '?', 'x', '?', 'x'],
                             ['o', '?', '?', '?', '?', '?'],
                             ['?', '?', '?', '?', '?', 'x'],
                             ['o', '?', '?', 'x', '?', '?'],
                             ['?', '?', '?', '?', '?', '?']], dtype=object)

sample_grid_easy = np.array([['?', '?', '?', 'o', '?', '?'],
                             ['?', '?', '?', 'o', 'o', '?'],
                             ['?', '?', '?', '?', '?', '?'],
                             ['?', '?', 'o', '?', '?', 'x'],
                             ['?', '?', '?', '?', 'x', 'x'],
                             ['?', '?', 'x', '?', '?', '?']], dtype=object)


# =========================================== 
# Define functions =
# =========================================== 

# Function for manually inputting a grid
    
def input_grid(grid):
    
    for i in range (0,6):    
        for j in range (0,6):

            while True:    # infinite loop
                test_input = input('enter row '+ str(i+1) + ', column ' + str(j+1) + ': ')
                if test_input == 'o' or test_input == 'x' or test_input == '?':
                    break  # stops the loop
                elif test_input == 'quit':
                    return
                else: 
                    print('Valid entries are o/x/?/quit')
            
            grid [i,j] = test_input
            
    return grid

# Function which tests whether the line under test could be the current one of the 14 valid lines
    
def could_be_this_line (test_line, valid_line):
  
    test1 = (test_line == valid_line)
    test2 = (test_line == '?')
    test3 = test2
    
    for i in range(0,6):
        test3[i] = test1[i] or test2[i]

    return np.all(test3)

# Main function to test a whole row and look for entries that can be completed

def test_a_row (sample_grid, valid_solutions, index):

#    print('=== test_a_row function - index=', index)
    
    valid_lines_list = []

    for i in range (0,14):
    
        if (could_be_this_line(sample_grid[index], valid_solutions[i])): 
    
            valid_lines_list.append(valid_solutions[i])
  
    valid_lines_list = np.asarray(valid_lines_list)
    
#    print('valid_lines_list=', valid_lines_list)
    
    numOfRows = valid_lines_list.shape[0]
    numOfCols = valid_lines_list.shape[1]

#    print('numOfRows= ' , numOfRows)
#    print('numOfCols= ' , numOfCols)

    updated_grid = sample_grid

# fudge to ensure we only loop if there is >1 possible line that this line could be

    if numOfRows > 1:
        
        for j in range (0,numOfCols):
    
            all_same = True
#           print('j=', j)
            
            for i in range (0,numOfRows-1):
            
                if valid_lines_list[i+1,j] != valid_lines_list[i,j]:
                    all_same = False
               
#                print('i= ', i, 'j=', j, 'allsame=', all_same )
              
            if all_same:
                updated_grid[index,j] = valid_lines_list[i,j]
        
    else:
        updated_grid[index] = valid_lines_list[0]
            
    sample_grid = updated_grid

    return sample_grid
         

# Main function to test a whole column and look for entries that can be completed

def test_a_col (sample_grid, valid_solutions, index):

#    print('=== test_a_col function - index=', index)

    valid_lines_list = []

    sample_grid = sample_grid.transpose()
    
#    print(sample_grid)
    
    for i in range (0,14):
    
        if (could_be_this_line(sample_grid[index], valid_solutions[i])): 
    
            valid_lines_list.append(valid_solutions[i])

    valid_lines_list = np.asarray(valid_lines_list)
    
#    print('valid_lines_list=', valid_lines_list)
    
    numOfRows = valid_lines_list.shape[0]
    numOfCols = valid_lines_list.shape[1]

#    print('numOfRows= ' , numOfRows)
#    print('numOfCols= ' , numOfCols)

    updated_grid = sample_grid
    
# fudge to ensure we only loop if there is >1 possible line that this line could be

    if numOfRows > 1:  
        
        for j in range (0,numOfCols):
    
            all_same = True
 #           print('j=', j)
            
            for i in range (0,numOfRows-1):
            
                if valid_lines_list[i+1,j] != valid_lines_list[i,j]:
                    all_same = False
               
#                print('i= ', i, 'j=', j, 'allsame=', all_same )
              
            if all_same:
                updated_grid[index,j] = valid_lines_list[i,j]
        
    else:
        updated_grid[index] = valid_lines_list[0]

        
    sample_grid = updated_grid
    
    sample_grid = sample_grid.transpose()

    return sample_grid

# =========================================== 
# Main program loop
# =========================================== 

# Choose in the code here how you want to input your puzzle grid
    
# grid = input_grid(initial_grid)

# grid = sample_grid_easy

grid = sample_grid_hard

print('grid before iteration')

print(grid)

# print(could_be_this_line(sample_grid[0], valid_solutions[1]))

for iteration in range (1,100):

    startgrid = np.copy(grid)
    
    for row_index in range (0,6):
    
        newgrid = test_a_row (grid, valid_solutions, row_index)
#        print('row=', row_index)
#        print('grid after test=', newgrid)
        grid = newgrid

    for col_index in range (0,6):
        
        newgrid = test_a_col (grid, valid_solutions, col_index)
#        print('col=', col_index)
#        print('grid after test=', newgrid)
        grid = newgrid
 
    print('grid after iteration number', iteration)
    print(grid)

# if the gris hasn't changed between iterations, we assume grid is solved.   
    if np.array_equal(startgrid,grid):
        print('*** Grid is stable after', iteration, 'iterations ***')
        break
        
print('== END (stable or completed 100 iterations without stabilising) ==')


# END