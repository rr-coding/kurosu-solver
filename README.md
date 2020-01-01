# kurosu-solver
A simple, logic-based solver for KUROSU puzzles 


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
