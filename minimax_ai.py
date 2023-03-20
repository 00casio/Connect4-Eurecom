# import numpy as np
# import random
# from variables import *
# from scores import *
from AI_test import *
import numpy as np
from typing import Optional

from variables import Variables

vzuydskqdkz = Variables()
symbol_player_1 = vzuydskqdkz.symbol_player_1
symbol_player_2 = vzuydskqdkz.symbol_player_2
symbol_no_player = vzuydskqdkz.symbol_no_player


winning_move = 9999  # si on peut gagner, on le fait
three_in_lines = 9
two_in_lines = 6
counter_losing_move = 1000  # si on peut contrer une défaite imminente, on le fait
opp_three_in_lines = 12
opp_two_in_lines = 9
opp_one_in_line = 3

# dimensions board

number_col = 7
number_row = 6


def opponent(symbol_player):  # Gives symbol of the opponent
    if symbol_player == symbol_player_1:
        return symbol_player_2
    else:
        return symbol_player_1

def count_point(line, symbol_player):
    buffer = list(line)
    score = 0
    opp_player = opponent(symbol_player)
    # print(opp_player)
    if buffer.count(symbol_player) == 4:
        score += winning_move
    if buffer.count(symbol_player) == 3 and buffer.count(symbol_no_player) == 1:
        score += three_in_lines
    if buffer.count(symbol_player) == 2 and buffer.count(symbol_no_player) == 2:
        score += two_in_lines
    if buffer.count(opp_player) == 3 and buffer.count(symbol_player) == 1:
        score += counter_losing_move
    if buffer.count(opp_player) == 2 and buffer.count(symbol_player) == 1:
        score += opp_two_in_lines
    return score

def score_board(board, symbol_player):
    s = 0
    # Horiz
    for i in range(6):
        for j in range(0, 4, 1):
            s += count_point(board[i, j:j+4], symbol_player)
    # Vert
    for i in range(3):
        for j in range(7):
            s += count_point(board[i:i+4, j], symbol_player)
    # \
    for i in range(3):
        for j in range(4):
            s += count_point([board[i + k, j + k] for k in range(4)], symbol_player)
    # /
    for i in range(3):
        for j in range(4):
            s += count_point([board[i + 3 - k, j + k] for k in range(4)], symbol_player)
    return s

def score_node(node):
    board = node.get_board_state()
    score = 0
    if board.state_win(node.symbol_player):
        score = 42 - node.nbr_move
    elif node.parent is not None and board.state_win(node.parent.symbol_player):
        score = -(42 - node.nbr_move)
    node.score = score
    return score


def minimax(node, alpha, beta, maximising):
    if node.is_terminal():
        score = score_node(node)
        if maximising:
            print("maximising", end = " ")
        else:
            print("minimizing", end = " ")
        node.score = score
        print(node.score, score)
        print(node.depth)
        return node

    if maximising:
        value = - 100
        for child in node.children:
            p = minimax(child, alpha, beta, False)
            value = max(value, p.score)
        node.score = value
        print("maximizing", value)
    else:
        value = + 100
        for child in node.children:
            p = minimax(child, alpha, beta, True)
            value = min(value, p.score)
        node.score = value
        print("minimizing", value)
    return node
