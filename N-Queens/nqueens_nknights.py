#!/usr/bin/env python2
# a0.py : Solve the N-Queens, N-Rooks and N-knights problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Supriya Ayalur Balasubramanian, 09-Sep-2018
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Count the total number of pieces on the diagonal.
# Here we are calculating the possible moves of a queen along the diagonals when placed in a square. 
# This count is checked for to eliminate the possible successor states.
def count_on_diagonal(board, row, col):
    dsum = 0

# Left diagonal
# Check on lower left diagonal
    r = row+1
    c = col-1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            dsum+=1
        r+=1
        c-=1

# Check on upper left diagonal
    r = row-1
    c = col-1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            dsum+=1
        r-=1
        c-=1


# Right diagonal
# Check on upper right diagonal
    r = row-1
    c = col+1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            dsum+=1
        r-=1
        c+=1

# Check on lower right diagonal
    r = row+1
    c = col+1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            dsum+=1
        r+=1
        c+=1

    if dsum > 0:
        return(dsum)

    return(dsum)
	
# Check for the availability of a knight in the board.
# Here we are calculating the possible moves of a knight when placed in a square. 
# This count is checked for to eliminate the possible successor states.
def count_of_nknights(board,row,col):
    nknights_sum=0

# Checking on lower left side 	
    r=row+2
    c=col-1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r+=2
        c-=1
    	
    r=row+1
    c=col-2
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r+=1
        c-=2
    
    		
# Checking on upper left side 
    r=row+2
    c=col+1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r+=2
        c+=1
    	
    	
    r=row+1
    c=col+2
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r+=1
        c+=2
    
    
# Checking on lower right side 
    r=row-2
    c=col-1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r-=2
        c-=1
    	
    
    r=row-1
    c=col-2
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r-=1
        c-=2
    
    
# Checking on upper right side 
    r=row-2
    c=col+1
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r-=2
        c+=1
    	
    r=row-1
    c=col+2
    while(r>=0 and c>=0 and r<N and c<N):
        if(board[r][c] == 1):
            nknights_sum+=1
        r-=1
        c+=2
    		
    	
    if nknights_sum > 0:
        return(nknights_sum)
    
    return(nknights_sum)
	
# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    board_str=''
    for row in range(0,N):
        for col in range(0,N):
            if (row,col) in coord_list:
                board_str+='X '
            elif board[row][col] == 0:
                board_str+='_ '
            else:
                if problem_type == 'nqueen': 
                    board_str+='Q '
                elif problem_type == 'nrook':
                    board_str+='R '
                elif problem_type == 'nknight':
                    board_str+='K '
        board_str+='\n'    
    return(board_str)

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# N-rooks, N-queens and N-knights successor function.
# Generates successors states even when some of the squares are blocked.
def a0successors(board):
    a0_board=[]
    if count_pieces(board)+1 <= N:
        for r in range(0,N):
            for c in range(0,N):
                if board[r][c] == 0 and count_on_col(board,c) <1 and count_on_row(board,r) <1:
                    if problem_type == 'nqueen' and count_on_diagonal(board,r,c) <=0:
                        if (r,c) not in coord_list:
                            a0_board.append(add_piece(board, r, c))
                    elif problem_type == 'nrook' and (r,c) not in coord_list:
                        a0_board.append(add_piece(board, r, c))
                if problem_type == 'nknight':
                    if count_of_nknights(board,r,c)<=0 and board[r][c] == 0 and (r,c) not in coord_list:
                        a0_board.append(add_piece(board, r, c))
    return(a0_board)
    
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N

# Solve n-rooks, n-queens and n-knights!
def solve(initial_board):
    fringe = [initial_board]                                                                                                 
    while len(fringe) > 0:
        for s in a0successors(fringe.pop()):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Command line arguments:
# This variable defines the type of problem, i.e, takes one of the parameters nrook, nqueen, nknight.
problem_type = sys.argv[1]

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[2])

# This defines the number of unavailable positions in the board.
unavail_pos = int(sys.argv[3])

# The remaining arguments define the coordinates of the unavailable positions.
# It takes all the arguments from the 4th argument and stores it in a list called unavail_coord.
# https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation
unavail_coord = sys.argv[4:]

# Creating a list of lists for the coordinates of the unavailable positions. 
# Converting the string to int using map function.
# https://stackoverflow.com/questions/4988002/shortest-way-to-slice-even-odd-lines-from-a-python-array
x_coord_list = [x-1 for x in list(map(int, unavail_coord[::2]))]
y_coord_list = [x-1 for x in list(map(int, unavail_coord[1::2]))]
# https://stackoverflow.com/questions/33887103/zip-two-lists-and-join-their-elements/33887132
coord_list=zip(x_coord_list, y_coord_list)

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")