import numpy as np
import random
from interface import *
from variables import *
 

difficulty = "easy" #add difficulty to varibales file
depth_easy = 1 
depth_normal = 5 #à changer
depth_hard = 10 #à changer
symbol_player_1 = "1"
symbol_player_2 = "2"

##Variables describing points given for minimax algorithm

winning_move = 1000
three_in_lines = 6
two_in_lines = 3
center = 2
losing_move = -1000
opp_three_in_lines = -9
opp_two_in_lines = -6
opp_one_in_line = -3

number_col = 7
number_row = 6



#enter here if playing (turn) = AI number
def AI(board, symbol_player):
    symbol_player = playing
    col = best_col_prediction(board)
    if is_valid_col(col): #devrait toujours être bon 
        drop_disk(board, col, playing)
    playing = opponent(playing) # change to other player
    return board

#def minimax(board, depth = 1): #returns the column where the AI will play
#    if difficulty == "normal":
#        depth = depth_normal
#    elif difficulty == "hard":
#        depth = depth_hard
#    ##construct the score 
#    pass #not finished

def opponent(symbol_player):
    if symbol_player == symbol_player_1:
        return symbol_player_1
    else:
        return symbol_player_2

def count_points_buffer(buffer, symbol_player):
    score = 0
    opp_player = opponent(symbol_player)
    if buffer.count(symbol_player) == 4:
        score += winning_move
    elif buffer.count(symbol_player) == 3 and buffer.count(symbol_no_player) == 1 :
            score += three_in_lines
    elif buffer.count(symbol_player) == 2 and buffer.count(symbol_no_player) == 2 :
             score += two_in_lines
    if buffer.count(opp_player) == 4:
        score += losing_move
    elif buffer.count(opp_player) == 3 and buffer.count(symbol_no_player) == 1:
        score += opp_three_in_lines
    elif buffer.count(opp_player) == 2 and buffer.count(symbol_no_player) == 2 :
        score += opp_two_in_lines
    return score


def score_column_prediction(board, symbol_player): #symbol_player is the number of current player
    opp = opponent(symbol_player) 
    for i in range(number_row): # for horizontal lines
        row = board[i, :]
        for j in range(number_col - 3):
            buffer_row = row[j: j + 4] #buffer of 4 length to check for disks in horizontal lines
            score += count_points_buffer(buffer_row, symbol_player)

    for j in range(number_col): # for vertical lines
        col = board[:, j]
        for i in range(number_row - 3):
            buffer_col = col[i, i + 4] #buffer of 4 length to check for disks in vertical lines
            score += count_points_buffer(buffer_col, symbol_player)

    for i in range(number_row - 3): # for slash digonal 
        for j in range(number_col - 3):
            buffer_slash = board[i+3][j+3]
            score += count_points_buffer(buffer_slash, symbol_player)

    for i in range(number_row - 3): # for backslash diagonal
        for j in range(number_col - 3, number_col):
            buffer_backslash = board[i][j]
            score += count_points_buffer(buffer_backslash, symbol_player)
    return score

def drop_disk(board, col, symbol_player):
    free_slot = find_free_slot(col)
    board[free_slot][col] = symbol_player

def is_valid_col(board, col):
    return board[0][col] == 0

def list_valid_col(board):
    valid_col = []
    for col in range (number_col):
        if find_free_slot(col) != -1:
            valid_col.append(col)
    return valid_col

def best_col_prediction(board, symbol_player):
    best_score = -100000
    best_col = random.choice(list_valid_col(board))
    for col in list_valid_col:
        potential_board = board.copy()
        drop_disk(potential_board, col, symbol_player)
        score = score_column_prediction(potential_board, symbol_player)
        if score >= best_score:
            best_score = score
            best_col = col
    return best_col
