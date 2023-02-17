#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface.AI import *
from interface.screens import *
from interface.tools_boxes import *
from interface.tools_writing import *
from scores import who_is_winner


def inverse_player(symbol_playing):
    """ Return the symbols of the opponent of the player currently playing """
    if symbol_playing == symbol_player_1:
        symbol_playing = symbol_player_2
        color_playing = color_player_2
    else:
        symbol_playing = symbol_player_1
        color_playing = color_player_1
    return symbol_playing, color_playing


def find_free_slot(i):
    """ Return the index of the first free slot """
    col = board[:, i]
    for j in range(len(col) - 1, -1, -1):
        if col[j] == symbol_no_player:
            return j
    return -1


def click(symbol_player, color, pos_click_x):
    """ What happens when a player click in a row or an AI play """
    global board

    num_col = pos_click_x // size_cell
    i = find_free_slot(num_col)
    if i == -1:
        return symbol_player, color
    board[i, num_col] = symbol_player
    x = padding + num_col * size_cell + size_cell // 2
    for y in range(padding // 2, padding + i * size_cell + padding // 2, 5):
        screen.fill(white)
        pg.draw.circle(screen, color, (x, y), radius_disk)
        update_screen()
    draw_circle(num_col, i, color, radius_hole)
    return inverse_player(symbol_player)


def gaming(event):
    """ The function that should handle all events in a turn """
    global symbol_playing, color_playing, num_turn

    winner = symbol_no_player
    if event.type == pg.MOUSEBUTTONUP:
        pos_click = pg.mouse.get_pos()
        if padding < pos_click[0] < width_board + padding:
            symbol_playing, color_playing = click(
                symbol_playing, color_playing, pos_click[0] - padding
            )
            num_turn += 1
            winner = who_is_winner(board)
            if winner == symbol_player_1:
                print("Winner is player 1")
            elif winner == symbol_player_2:
                print("Player 2 won this match")
            elif num_turn == nbr_max_turn:
                winner = symbol_draw
                print("It's a draw")

    if winner == symbol_no_player:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x < pos_min_x:
            mouse_x = pos_min_x
        elif mouse_x > pos_max_x:
            mouse_x = pos_max_x
        screen.fill(color_screen)
        pg.draw.circle(screen, color_playing, (mouse_x, padding // 2), radius_disk)
    return winner
