#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

from typing import Any, Iterator
from variables import Variables
from utils import Symbol, opponent
from structure import Node, Board

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


def count(buffer: list[Any], symbol: Any, number: int) -> bool:
    return buffer.count(symbol) == number


def count_point(line: np.ndarray[Any, np.dtype[Any]] | list[Any], symbol_player: Any) -> int:
    buffer = list(line)
    score = 0
    opp_player = opponent(symbol_player)
    g = buffer.count(symbol_player)
    b = buffer.count(opp_player)
    z = buffer.count(symbol_no_player)

    # if (g == 4):
    #     score += 500001 #// preference to go for winning move vs. block
    # elif (g == 3 and z == 1):
    #     score += 5000
    # elif (g == 2 and z == 2):
    #     score += 500
    # elif (b == 2 and z == 2):
    #     score -= 501# // preference to block
    # elif (b == 3 and z == 1):
    #     score -= 5001 # // preference to block
    # elif (b == 4):
    #     score -= 500000
    # if count(buffer, symbol_player, 4):
    #     score += 100
    # if count(buffer, symbol_player, 3) and count(buffer, symbol_no_player, 1):
    #     score += 5
    # if count(buffer, symbol_no_player, 2) and count(buffer, symbol_player, 2):
    #     score += 2
    # if count(buffer, opp_player, 3) and count(buffer, symbol_no_player, 1):
    #     score -= 4
    if count(buffer, symbol_player, 4):
        return winning_move
    elif count(buffer, opp_player, 4):
        return -winning_move
    elif count(buffer, symbol_player, 3) and count(buffer, symbol_no_player, 1):
        score += three_in_lines
    elif count(buffer, opp_player, 3):
        if count(buffer, symbol_no_player, 1):
            score -= three_in_lines
    elif count(buffer, symbol_no_player, 2):
        if count(buffer, symbol_player, 2):
            score += two_in_lines
        elif count(buffer, opp_player, 2):
            score -= two_in_lines
    return score


def score_board(board: Board, symbol_player: Any) -> int:
    s = 0
    # Horiz
    for i in range(6):
        for j in range(0, 4, 1):
            s += count_point(board[i, j : j + 4], symbol_player)
    # Vert
    for i in range(3):
        for j in range(7):
            s += count_point(board[i : i + 4, j], symbol_player)
    # \
    for i in range(3):
        for j in range(4):
            s += count_point([board[i + k, j + k] for k in range(4)], symbol_player)
    # /
    for i in range(3):
        for j in range(4):
            s += count_point([board[i + 3 - k, j + k] for k in range(4)], symbol_player)
    return s


def score_node(node: Node) -> int:
    board = node.get_board_state()
    score = 0
    if board.state_win(node.symbol_player):
        score = 42 - node.nbr_move
    elif node.parent is not None and board.state_win(node.parent.symbol_player):
        score = -(42 - node.nbr_move)
    node.score = score
    return score


def minimax(node: Node, alpha: int, beta: int, maximising: bool) -> tuple[int, int]:
    if node.is_terminal():
        score = score_board(node.get_board_state(), node.symbol_player)
        # if maximising:
        #     print("maximising", end = " ")
        # else:
        #     print("minimizing", end = " ")
        n = node.copy()
        n.score = score
        # print(node.score, score)
        return n.score, n.column_played

    chosen = node.copy()
    chosen.column_played = -1
    if maximising:
        value = -10000000
        for child in node.children:
            score = minimax(child, alpha, beta, False)[0]
            if score > value:
                value = score
        # print("maximizing", value)
    else:
        value = +10000000
        for child in node.children:
            score = minimax(child, alpha, beta, True)[0]
            if score < value:
                value = score
        # print("minimizing", value)
    return score, chosen.column_played  # faux, plus de node
