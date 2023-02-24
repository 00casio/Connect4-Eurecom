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

#dimensions board

number_col = 7
number_row = 6


#enter here if playing (turn) = AI turn

def AI(board, symbol_player):
    col = best_col_prediction(board, symbol_player)
    print(board[:, col])
    row = find_free_row(col)
    print(row)
    print("we are going to play in row and in col : ", (row, col)) 
    print(is_valid_col(board, col))
    if is_valid_col(board, col): #devrait toujours être bon mais par précaution
        #print("i'm here !")
        #board = drop_disk(board, col, symbol_player)
        board = drop_disk2(board, row, col, symbol_player)
    #symbol_playing = opponent(symbol_player) # change to other player the global variable
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
        return symbol_player_2
    else:
        return symbol_player_1

def count_points_buffer(buffer, symbol_player):
    score = 0
    opp_player = opponent(symbol_player)
    #print(opp_player)
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
    score = 0
    opp = opponent(symbol_player) 
    for i in range(number_row): # for horizontal lines
        row = board[i, :]
        for j in range(number_col - 3):
            buffer_row = row[j: j + 4] #buffer of 4 length to check for disks in horizontal lines
            #print("buffer_row is", buffer_row)
            score += count_points_buffer(list(buffer_row), symbol_player)

    for j in range(number_col): # for vertical lines
        col = board[:, j]
        for i in range(number_row - 3):
            buffer_col = col[i: i + 4] #buffer of 4 length to check for disks in vertical lines
            #print("buffer_col is", buffer_col)
            score += count_points_buffer(list(buffer_col), symbol_player)

    for i in range(number_row - 3): # for slash digonal 
        for j in range(number_col - 3):
            buffer_slash = [board[i+k][j+k] for k in range(4)]
            #print("buffer_slash is", buffer_slash)
            score += count_points_buffer(list(buffer_slash), symbol_player)

    for i in range(number_row - 3): # for backslash diagonal
        for j in range(number_col - 3):
            buffer_backslash = [board[i+3-k][j+k] for k in range(4)]
            #print("buffer_backslash is", buffer_backslash)
            score += count_points_buffer(list(buffer_backslash), symbol_player)
    return score

def drop_disk(board, col, symbol_player):
    free_slot = find_free_row(col)
    board[free_slot][col] = symbol_player
    #new_free_spot = find_free_slot(col)
    #print(free_slot)
    #print(new_free_spot)
    #print("\n")
    return board

def drop_disk2(board, row, col, symbol_player):
    board[row][col] = symbol_player
    return board

def is_valid_col(board, col):
    return board[0][col] == "0"

def list_valid_col(board):
    valid_col = []
    for col in range (number_col):
        if find_free_row(col) != -1:
            valid_col.append(col)
    return valid_col

def find_free_row(colomn):
    col = board[:, colomn]
    #print(col)
    inv_col = col[::-1]
    #print(inv_col)
    #print("\n")
    for k in range(len(col)):
        if inv_col[k] == "0":
            return 6-(k+1)
    return -1

def best_col_prediction(board, symbol_player):
    best_score = -100000
    list_potential_col = list_valid_col(board)
    #print(list_potential_col)
    best_col = random.choice(list_potential_col)
    for col in list_potential_col:
        potential_board = board.copy()
        row = find_free_row(col)
        #print("for col", col)
        #print("to the row", row)
        #print("\n")
        drop_disk2(potential_board, row, col, symbol_player)
        score = score_column_prediction(potential_board, symbol_player)
        #print("the current best score is", best_score)
        #print("the score calculated is", score)
        if score >= best_score:
            best_score = score
            best_col = col
    return best_col

#Just in order to run some tests

empty_line = ["0", "0", "0", "0", "0", "0", "0"]
board1 = np.array([empty_line, empty_line, empty_line, empty_line, empty_line, ["0","1" ,"0", "0", "0", "0", "0"]])
board2 = np.array([empty_line, empty_line, ["0","0", "0" ,"0", "0" ,"0" ,"0"], ["1","0", "0" ,"0", "0" ,"0" ,"0"], ["1","0", "1" ,"0", "0" ,"0" ,"0"], ["1","0", "1" ,"0", "0" ,"2" ,"2"]])
 
current_board = AI(board1, "1")
print(current_board)
print("\n")
current_board2 = AI(current_board, "2")
print(current_board2)
print("\n")
#current_board = AI(current_board, "1")
#print(current_board)
#print("\n")
#current_board = AI(current_board, "2")
#print(current_board)
#print("\n")
#current_board = AI(current_board, "1")
#print(current_board)
#print("\n")
#current_board = AI(current_board, "2")
#print(current_board)
#print("\n")
