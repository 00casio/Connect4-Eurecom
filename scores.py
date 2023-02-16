#!/usr/bin/python3
# -*- coding: utf-8 -*-

from variables import no_player, player_1, player_2
from numpy import ceil, where, zeros

def state_to_bits(state):
    """Convert the state of the game for a player into the bits representation of the game"""
    n = "0b"
    for j in range(len(state[0])-1, -1, -1):
        n += "0"
        for i in range(len(state)):
            n += f"{int(state[i, j])}" # <==> n += str(b)
    return n

def state_win(state):
    print(state)
    bits = int(state_to_bits(state), 2)

    # Horizontal check
    m = bits & (bits >> 7)
    if m & (m >> 14):
        return True
    # Vertical
    m = bits & (bits >> 1)
    if m & (m >> 2):
        return True
    # Diagonal \
    m = bits & (bits >> 6)
    if m & (m >> 12):
        return True
    # Diagonal /
    m = bits & (bits >> 8)
    if m & (m >> 16):
        return True
    # Nothing found
    return False

def who_is_winner(board):
    s = board.shape
    state_player_1 = zeros(s)
    state_player_2 = zeros(s)
    state_player_1[where(board == player_1)] = 1
    state_player_2[where(board == player_2)] = 1
    if state_win(state_player_1):
        return player_1
    elif state_win(state_player_2):
        return player_2
    else:
        return no_player
