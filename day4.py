# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 23:57:21 2021

@author: Connor
"""
import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    # Get just the list of drawings
    drawings = np.array([int(item) for item in lines[0].split(",")])
    
    # Separate out the boards to parse 
    board_list = lines[1:]
    boards = []
    marks = []
    ii = 0
    while ii < len(board_list):
        if board_list[ii] == "\n":
            # Skip blank lines
            ii += 1
        else:
            # else update a zeros matrix with the proper board values
            new_board = np.zeros((5,5))
            for jj in range(5):
                new_board[jj,:] = np.array([int(item) for item in board_list[ii+jj].split()])
            boards.append(new_board)
            # Also store a marks mask
            marks.append(np.zeros((5,5), dtype=bool))
            ii += 5
        
    return drawings, boards, marks

def check_winner(board, mark):
    # No diagonals means this easy check works
    if np.any(np.sum(mark, axis=0)==5):
        return True
    elif np.any(np.sum(mark, axis=1)==5):
        return True
    else:
        return False

def get_winner(drawings, boards, marks):
    # For each drawing
    for drawing in drawings:
        # update the boards corresponding marks
        for board, mark in zip(boards, marks):
            mark |= board==drawing
            
            # See if any board has won yet
            if check_winner(board, mark):
                # if so, return that board, marks mask and wininng number
                return board, mark, drawing
    return None, None, None

def get_last_winner(drawings, boards, marks):
    dd = 0
    # Loop until all boards have won
    while len(boards) > 0:
        drawing = drawings[dd]
        winners = []
        # Update all boards per move
        for ii, (board, mark) in enumerate(zip(boards, marks)):
            mark |= board==drawing
            
            # See if any boards won
            if check_winner(board, mark):
                # Append those indices to a list as a surprise tool for later
                winners.append(ii)
                
        # its later; loop over this list BACKWARDS (to avoid index issues)
        for winner in winners[::-1]:
            # pop marks and boards for each winner
            last_marks = marks.pop(winner)
            last_winner = boards.pop(winner)
        dd += 1
    # If the loop ends, return the last winner, its mask, 
    # and the last winning number
    return last_winner, last_marks, drawing

if __name__ == "__main__":
    drawings, boards, marks = parse_input("input4.txt")
    
    winning_board, winning_marks, winning_num = get_winner(drawings, boards, marks)
    
    # Get the solutions to the problem
    print(np.sum(winning_board[winning_marks==False]) * winning_num)
    
    winning_board, winning_marks, winning_num = get_last_winner(drawings, boards, marks)
    print(np.sum(winning_board[winning_marks==False]) * winning_num)