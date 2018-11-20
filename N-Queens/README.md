# N-rooks, N-queens and N-knights

Imagine that you have an empty chessboard of size N { i.e., an N _ N grid of squares. Our goal is to _nd a way of placing N queens on the board such that no two queens share the same row, column, or diagonal { in other words, so that no queen could \take" any other queen. This is called the N-queens problem. For example, when N = 1, there's a very easy solution (the queen goes on the only square!). For N = 2, there's no solution at all, nor is there a solution for N = 3. But there are solutions for larger boards, including the standard chessboard with N = 8. Create a new program, nqueen_nrook_nknight.py, with several features, including the ability to solve the N-rooks, N-queens and N-knoght problems, and the ability to solve these problems when some of the squares of the board are not available (meaning that you cannot place a piece on them). Your program must accept at least 3 arguments. The first one is either nrook or nqueen, which signifies the problem type. The second is the number of rooks or queens (i.e., N). The third argument represents the number of unavailable positions. The remaining arguments encode which positions are unavailable, using row- column coordinates and assuming a coordinate system where (1,1) is at the top-left of the board. Taking the 7-rooks problem with position (1, 1) unavailable as an example, we might run:

$.nqueen_nrook_nknight.py nrook 7 1 1 1 which means that one square is unavailable, and it is at row 1 and column 1. One possible result could be:

$ ./nqueen_nrook_nknight.py nrook 7 1 1 1

X R _ _ _ _ _

R _ _ _ _ _ _

_ _ R _ _ _ _

_ _ _ R _ _ _

_ _ _ _ R _ _

_ _ _ _ _ R _

_ _ _ _ _ _ R

where R indicates the position of a rook, underscore marks an empty square, and X shows the unavailable position. Or for the 8-queens problem with (1, 2) and (1,8) unavailable, one possible result could be:

$ ./nqueen_nrook_nknight.py nqueen 8 2 1 2 1 8

_ X _ _ Q _ _ X

_ _ _ _ _ _ Q _

_ Q _ _ _ _ _ _

_ _ _ _ _ Q _ _

_ _ Q _ _ _ _ _

Q _ _ _ _ _ _ _

_ _ _ Q _ _ _ _

_ _ _ _ _ _ _ Q

where the Q's indicate the positions of queens on the board. As a special case, there can be 0 unavailable squares, in which case only exactly three arguments are given to nqueen_nrook_nknight.py. Please print only the solution in exactly the above format and nothing else. The output format is important because we will use an auto-grading script to test and grade your code.

Additionally, Implement the N-knights problem, which should be invoked using nknight as the first parameter to nqueen_nrook_nknight.py. The goal of this puzzle is to place N knights on the board such that none of them can take any of the others, where again some squares are unavailable.
