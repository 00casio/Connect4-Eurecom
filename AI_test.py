import numpy as np
import random
import math
from interface import *
#from variables import *
from scores import *

#difficulty = "easy" #add difficulty to varibales file
#depth_easy = 1 
#depth_normal = 5 #à changer
#depth_hard = 10 #à changer
symbol_player_1 = "1"
symbol_player_2 = "2"
symbol_no_player = "0"
symbol_draw = "-1"

##Variables describing points given 

winning_move = 1500 # si on peut gagner, on le fait
three_in_lines = 9
two_in_lines = 6
counter_losing_move = 1000 # si on peut contrer une défaite imminente, on le fait
opp_three_in_lines = 12
opp_two_in_lines = 9
opp_one_in_line = 3

#dimensions board

number_col = 7
number_row = 6



def AI(board, symbol_player): #enter here if playing (turn) = AI turn
    col = best_col_prediction(board, symbol_player)
    #col = minimax_no_pruning(board, 2, True, "1")
    #print(board[:, col])
    row = find_free_row(board, col)
    #print(row)
    print("\n")
    print("we are going to play in (row, col) = ", (row, col))
    #print(is_valid_col(board, col))
    if is_valid_col(board, col): #devrait toujours être bon mais par précaution
        #print("i'm here !")
        #board = drop_disk(board, col, symbol_player)
        board = drop_disk(board, col, symbol_player)
    #symbol_playing = opponent(symbol_player) # change to other player the global variable
    return board

def opponent(symbol_player): # Gives symbol of the opponent
    if symbol_player == symbol_player_1:
        return symbol_player_2
    else:
        return symbol_player_1
    
def minimax_no_pruning(board, depth, maximizing_player, symbol_player): #returns the column where the AI will play, I tried without any success to follow and adapt the pseudo code in wikipedia
    valid_col = list_valid_col(board)
    if depth == 0 or who_is_winner(board) != symbol_no_player:
        if who_is_winner(board) == symbol_player_1:
            return (None, math.inf)
        elif who_is_winner(board) == symbol_player_2:
            return (None, - math.inf)
        elif who_is_winner(board) == symbol_draw:
            print("It is a draw, game is over")
            return (None, 0)
        else:
            return (None, score_column_prediction(board, symbol_player)) # depth = 0
        
    if maximizing_player: 
        best_score = -math.inf
        best_col = random.choice(valid_col)
        for col in valid_col:
            potential_board = board.copy()
            drop_disk(board, col, symbol_player)
            score_calculated = minimax_no_pruning(potential_board, depth-1, False)[1]
            if score_calculated > best_score:
                best_score = score_calculated
                best_col = col
        return best_col, best_score
    else:
        best_score = math.inf
        best_col = random.choice(valid_col)
        for col in valid_col:
            potential_board = board.copy()
            drop_disk(board, col, symbol_player)
            score_calculated = minimax_no_pruning(potential_board, depth-1, True)[1]
            if score_calculated < best_score:
                best_score = score_calculated
                best_col = col
        return best_col, best_score

def count_points_buffer(buffer, symbol_player): #pour des buffers de 4 éléments ayant des combinaisons verticales/horizontales/diagonales du tableau, on ajoute le nombre de point correspondant
    score = 0
    opp_player = opponent(symbol_player)
    #print(opp_player)
    if buffer.count(symbol_player) == 4:
        score += winning_move
    elif buffer.count(symbol_player) == 3 and buffer.count(symbol_no_player) == 1 :
            score += three_in_lines
    elif buffer.count(symbol_player) == 2 and buffer.count(symbol_no_player) == 2 :
             score += two_in_lines
    if buffer.count(opp_player) == 3 and buffer.count(symbol_player) == 1:
        score += counter_losing_move
    elif buffer.count(opp_player) == 2 and buffer.count(symbol_player) == 1 :
        score += opp_two_in_lines
    elif buffer.count(opp_player) == 1 and buffer.count(symbol_no_player) == 1:
        score += opp_one_in_line
    return score

def score_column_prediction(board, symbol_player): #On calcule le score total pour une situation du jeu, on l'utilisera pour trouver dans quelle colonne il vaut mieux jouer
    score = 0
    # score_horiz = 0
    # score_vert = 0
    # score_diag_slash = 0
    # score_diag_backslash = 0
    opp = opponent(symbol_player) 
    for i in range(number_row): # for horizontal lines
        row = board[i, :]
        for j in range(number_col - 3):
            buffer_row = row[j: j + 4] #buffer of 4 length to check for disks in horizontal lines
            # if count_points_buffer(list(buffer_row), symbol_player) != 0:
            #    print("buffer_row is", buffer_row)
            #    print("score added is : ", count_points_buffer(list(buffer_row), symbol_player))
            score += count_points_buffer(list(buffer_row), symbol_player)
    #score_horiz = score
    #print("horizontal score is : ", score_horiz)

    for j in range(number_col): # for vertical lines
        col = board[:, j]
        for i in range(number_row - 3):
            buffer_col = col[i: i + 4] #buffer of 4 length to check for disks in vertical lines
            # if count_points_buffer(list(buffer_col), symbol_player) != 0:
            #    print("buffer_col is", buffer_col)
            #    print("score added is : ", count_points_buffer(list(buffer_col), symbol_player))
            score += count_points_buffer(list(buffer_col), symbol_player)
    #score_vert = score - score_horiz
    #print("vertical score is : ", score_vert)

    for i in range(number_row - 3): # for slash digonal 
        for j in range(number_col - 3):
            buffer_slash = [board[i+k][j+k] for k in range(4)]
            # if count_points_buffer(list(buffer_row), symbol_player) != 0:
            #    print("buffer_slash is", buffer_slash)
            #    print("score added is : ", count_points_buffer(list(buffer_slash), symbol_player))
            score += count_points_buffer(list(buffer_slash), symbol_player)
    # score_diag_slash = score -(score_horiz + score_vert)
    # print("diag slash score is : ", score_diag_slash )

    for i in range(number_row - 3): # for backslash diagonal
        for j in range(number_col - 3):
            buffer_backslash = [board[i+3-k][j+k] for k in range(4)]
            # if count_points_buffer(list(buffer_backslash), symbol_player) != 0:
            #    print("buffer_backslash is", buffer_backslash)
            #    print("score added is : ", count_points_buffer(list(buffer_backslash), symbol_player))
            score += count_points_buffer(list(buffer_backslash), symbol_player)
    # score_diag_backslash = score - (score_horiz + score_vert + score_diag_slash)
    # print("diag_backslash score is : ", score_diag_backslash )

    return score

def drop_disk(board, col, symbol_player): #on glisse un jeton
    free_slot = find_free_row(board, col)
    board[free_slot][col] = symbol_player
    #new_free_spot = find_free_slot(col)
    #print(free_slot)
    #print(new_free_spot)
    #print("\n")
    return board

def is_valid_col(board, col): #on regarde si la colonne est pleine ou pas
    return board[0][col] == "0"

def list_valid_col(board): #liste des colonnes où l'on peut jouer
    valid_col = []
    for col in range (number_col):
        if find_free_row(board, col) != -1:
            valid_col.append(col)
    return valid_col

def find_free_row(board, colomn): #on trouve la ligne ou le jeton va aller pour une colonne donnée
    col = board[:, colomn]
    #print(col)
    inv_col = col[::-1]
    #print(inv_col)
    #print("\n")
    for k in range(len(col)):
        if inv_col[k] == "0":
            return 6-(k+1)
    return -1

def best_col_prediction(board, symbol_player): #on cherche la meilleure colonne où jouer en faisant fictivement avance le jeu en jouant dans chaque colonne
    best_score = -100000
    list_potential_col = list_valid_col(board)
    #print(list_potential_col)
    best_col = random.choice(list_potential_col)
    for col in list_potential_col:
        potential_board = board.copy()
        row = find_free_row(potential_board, col)
        #print("for col", col)
        #print("to the row", row)
        drop_disk(potential_board, col, symbol_player)
        score = score_column_prediction(potential_board, symbol_player)
        print("the current best score is", best_score)
        print("the score calculated is", score)
        #print("\n")
        if score >= best_score:
            best_score = score
            best_col = col
        if best_score == 0:
            best_col = 3
    return best_col


#Just in order to run some tests

empty_line = ["0", "0", "0", "0", "0", "0", "0"]
board1 = np.array([empty_line, empty_line, empty_line, empty_line, empty_line, empty_line])
board2 = np.array([empty_line, empty_line, ["0","0", "0" ,"0", "0" ,"0" ,"0"], ["1","0", "0" ,"0", "0" ,"0" ,"0"], ["1","0", "1" ,"0", "0" ,"0" ,"0"], ["1","0", "1" ,"0", "0" ,"2" ,"2"]])
 
def who_is_winner2(board: np.ndarray[np.float64]) -> str:
    s = board.shape
    state_symbol_player_1 = np.zeros(s)
    state_symbol_player_2 = np.zeros(s)
    state_symbol_player_1[np.where(board == symbol_player_1)] = 1
    state_symbol_player_2[np.where(board == symbol_player_2)] = 1
    if state_win(state_symbol_player_1):
        return symbol_player_1
    elif state_win(state_symbol_player_2):
        return symbol_player_2
    else:
        return symbol_no_player

def Ia_vs_Ia():
    print(board1)
    turn = 0
    for i in range(42):
        print("This is turn", turn)
        current_board = AI(board1, "1")
        turn += 1
        print(current_board)
        winner = who_is_winner2(current_board)
        if winner != symbol_no_player:
            print("And the winner is: player ", winner)
            break
        print("\n")
        print("This is turn", turn)
        current_board = AI(current_board, "2")
        turn += 1
        print(current_board)
        winner = who_is_winner2(current_board)
        if winner != symbol_no_player:
            print("And the winner is: player ", winner)
            break
        print("\n")
        
def Human_play(board):
    col = input("enter col : ")
    drop_disk(board, int(col), "1")
    print(board)
    board = AI(board, "2")
    print(board)


def play_vs_IA():
    print(board1)
    while who_is_winner2(board1) == "0":
        Human_play(board1)
    print("The winner is ", who_is_winner2(board1))

play_vs_IA() #elle est toute bête mais j'ai un peu galéré avant de la battre
#Ia_vs_Ia() # l'ia 1 bat la 2 en 32 tours sachant que je les fais jouer défensivement

