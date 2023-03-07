import inspect
import random
import inspect
import numpy as np

from variables import Variables

vzuydskqdkz = Variables()  # don't want to overlap two variables

# difficulty = "easy" #add difficulty to varibales file
# depth_easy = 1
# depth_normal = 5 #à changer
# depth_hard = 10 #à changer
symbol_player_1 = vzuydskqdkz.symbol_player_1
symbol_player_2 = vzuydskqdkz.symbol_player_2
symbol_no_player = vzuydskqdkz.symbol_no_player

##Variables describing points given

winning_move = 1500  # si on peut gagner, on le fait
three_in_lines = 9
two_in_lines = 6
counter_losing_move = 1000  # si on peut contrer une défaite imminente, on le fait
opp_three_in_lines = 12
opp_two_in_lines = 9
opp_one_in_line = 3

# dimensions board

number_col = 7
number_row = 6


def AI(board, symbol_player):  # enter here if playing (turn) = AI turn
    print(board)
    col = best_col_prediction(board, symbol_player)
    #minimax = minimax_no_pruning(board, 2, symbol_player)
    #col = minimax[0]
    #score = minimax[1]
    #print("The best score is", score)
    #print("the best col is", col)
    # print(board[:, col])
    #print(col)
    #print(score)
    row = board.find_free_slot(col)
    # print(row)
    print("\n")
    print("we are going to play in (row, col) = ", (row, col))
    # print(is_valid_col(board, col))
    if is_valid_col(board, col):  # devrait toujours être bon mais par précaution
        # print("i'm here !")
        # board = drop_disk(board, col, symbol_player)
        board = drop_disk(board, col, symbol_player)
    # symbol_playing = opponent(symbol_player) # change to other player the global variable
    return board


def opponent(symbol_player):  # Gives symbol of the opponent
    if symbol_player == symbol_player_1:
        return symbol_player_2
    else:
        return symbol_player_1


# def minimax_no_pruning(
#     board, depth, symbol_player
# ):  # returns the column where the AI will play, I tried without any success to follow and adapt the pseudo code in wikipedia
#     valid_col = list_valid_col(board)
#     if depth == 0 or who_is_winner2(board) != symbol_no_player:
#         if who_is_winner2(board) == symbol_player_1:
#             # print("test 1")
#             return (None, math.inf)
#         elif who_is_winner2(board) == symbol_player_2:
#             # print("test 2")
#             return (None, -math.inf)
#         elif who_is_winner2(board) == symbol_draw:
#             print("It is a draw, game is over")
#             return (None, 0)
#         else:
#             # print("test 3")
#             # print("the score is", score_column_prediction(board, symbol_player))
#             return (None, score_column_prediction(board, symbol_player))  # depth = 0

#     if symbol_player == "2":  # on cherche à maximiser le score du joueur 2 ici
#         best_score = -math.inf
#         best_col = random.choice(valid_col)
#         for col in valid_col:
#             potential_board = board.copy()
#             drop_disk(potential_board, col, symbol_player)
#             print(" IA turn, Here is for col", col)
#             print(potential_board)
#             print("\n")
#             score_calculated = minimax_no_pruning(
#                 potential_board, depth - 1, symbol_player
#             )[1]
#             if score_calculated >= best_score:
#                 best_score = score_calculated
#                 best_col = col
#         if best_score == 0:
#             return 3, best_score
#         print("best score, best col : ", best_score, best_col)
#         return best_col, best_score
#     else:
#         best_score = math.inf
#         best_col = random.choice(valid_col)
#         for col in valid_col:
#             potential_board = board.copy()
#             drop_disk(board, col, opponent(symbol_player))
#             print(" hypothesis player turn, Here is for col", col)
#             print(potential_board)
#             print("\n")
#             score_calculated = minimax_no_pruning(
#                 potential_board, depth - 1, opponent(symbol_player)
#             )[1]
#             if score_calculated <= best_score:
#                 best_score = score_calculated
#                 best_col = col
#         return best_col, best_score


def count_points_buffer(
    buffer, symbol_player
):  # pour des buffers de 4 éléments ayant des combinaisons verticales/horizontales/diagonales du tableau, on ajoute le nombre de point correspondant
    # print(buffer)
    score = 0
    opp_player = opponent(symbol_player)
    # print(opp_player)
    if buffer.count(symbol_player) == 4:
        score += winning_move
    elif buffer.count(symbol_player) == 3 and buffer.count(symbol_no_player) == 1:
        score += three_in_lines
    elif buffer.count(symbol_player) == 2 and buffer.count(symbol_no_player) == 2:
        score += two_in_lines
    if buffer.count(opp_player) == 3 and buffer.count(symbol_player) == 1:
        score += counter_losing_move
    elif buffer.count(opp_player) == 2 and buffer.count(symbol_player) == 1:
        score += opp_two_in_lines
    return score


# min()


def score_column_prediction(
    board, row, col, symbol_player
):  # On calcule le score total pour une situation du jeu, on l'utilisera pour trouver dans quelle colonne il vaut mieux jouer
    score = 0
    # score_horiz = 0
    # score_vert = 0
    # score_diag_slash = 0
    # score_diag_backslash = 0
    buffer_gen_horiz = board.horiz(row, col)
    for buffer_horiz in buffer_gen_horiz: # buffer of 4 length to check for disks in horizontal lines
        # if count_points_buffer(list(buffer_horiz), symbol_player) != 0:
        #     print("buffer_horiz is", buffer_horiz)
        #     print("score added is : ", count_points_buffer(list(buffer_horiz), symbol_player))
        score += count_points_buffer(list(buffer_horiz), symbol_player)
    # score_horiz = score
    # print("horizontal score is : ", score_horiz)

    buffer_gen_col = board.vert(row, col)  # buffer of 4 length to check for disks in vertical lines
    for buffer_vert in buffer_gen_col:   
        # print("buffer_col is", buffer_col)
        # print(count_points_buffer(list(buffer_col), symbol_player))
        # if count_points_buffer(list(buffer_vert), symbol_player) != 0:
        #   print("buffer_col is", buffer_vert)
        #   print("score added is : ", count_points_buffer(list(buffer_vert), symbol_player))
        score += count_points_buffer(list(buffer_vert), symbol_player)
    # score_vert = score - score_horiz
    # print("vertical score is : ", score_vert)

    buffer_gen_backslash = board.backslash(row, col) # for backslash diagonal
    for buffer_backslash in buffer_gen_backslash:
            # if count_points_buffer(list(buffer_backslash), symbol_player) != 0:
            #    print("buffer_backslash is", buffer_backslash)
            #    print("score added is : ", count_points_buffer(list(buffer_backslash), symbol_player))
            score += count_points_buffer(list(buffer_backslash), symbol_player)
    # score_diag_backslash = score -(score_horiz + score_vert)
    # print("diag backslash score is : ", score_diag_backslash )

    buffer_gen_slash = board.slash(row, col) # for slash diagonal
    for buffer_slash in buffer_gen_backslash:
            # if count_points_buffer(list(buffer_slash), symbol_player) != 0:
            #    print("buffer_slash is", buffer_slash)
            #    print("score added is : ", count_points_buffer(list(buffer_slash), symbol_player))
            score += count_points_buffer(list(buffer_slash), symbol_player)
    # score_diag_slash = score - (score_horiz + score_vert + score_diag_slash)
    # print("diag slash score is : ", score_diag_slash)

    return score


def drop_disk(board, col, symbol_player):  # on glisse un jeton
    free_slot = board.find_free_slot(col)
    board[free_slot][col] = symbol_player
    return board


def is_valid_col(board, col):  # on regarde si la colonne est pleine ou pas
    return board[0][col] == symbol_no_player


def list_valid_col(board):  # liste des colonnes où l'on peut jouer
    valid_col = []
    for col in range(number_col):
        if is_valid_col(board, col):
            valid_col.append(col)
    return valid_col

def best_col_prediction(
    board, symbol_player
):  # on cherche la meilleure colonne où jouer en faisant fictivement avance le jeu en jouant dans chaque colonne
    #print(board)
    best_score = -100000
    list_potential_col = list_valid_col(board)
    # print(list_potential_col)
    best_col = random.choice(list_potential_col)
    for col in list_potential_col:
        potential_board = board.copy()
        row = potential_board.find_free_slot(col)
        # print("for col", col)
        # print("to the row", row)
        drop_disk(potential_board, col, symbol_player)
        score = score_column_prediction(potential_board, row, col, symbol_player)
        # print("the current best score is", best_score)
        # print("the score calculated is", score)
        # print("\n")
        if score >= best_score:
            best_score = score
            best_col = col
        if best_score == 0:
            if 3 in list_potential_col:
                best_col = 3
            else:
                best_col = random.choice(list_potential_col)
    return best_col

