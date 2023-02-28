#!/usr/bin/python3
# -*- coding: utf-8 -*-

import variables as var
from interface.AI import *
from interface.screens import *
from interface.tools_boxes import *
from interface.tools_writing import *
from scores import who_is_winner
from variables import Color, Event, Symbol, pg


def click(
    symbol_player: Symbol, color: Color, pos_click_x: int
) -> tuple[Symbol, Color]:
    """What happens when a player click in a row or an AI play"""

    num_col = pos_click_x // var.size_cell
    i = find_free_slot(num_col)
    if i == -1:
        return (symbol_player, color)
    var.board[i, num_col] = symbol_player
    x = var.padding + num_col * var.size_cell + var.size_cell // 2
    for y in range(
        var.padding // 2, var.padding + i * var.size_cell + var.size_cell // 2, 5
    ):
        var.screen.fill(var.white)
        pg.draw.circle(var.screen, color, (x, y), var.radius_disk)
        update_screen()
    draw_circle(num_col, i, color, var.radius_hole)
    return inverse_player(symbol_player)


def gaming(event: Event) -> Symbol:
    """The function that should handle all events in a turn"""

    winner = var.symbol_no_player
    if event.type == pg.MOUSEBUTTONUP:
        pos_click = pg.mouse.get_pos()
        if var.padding < pos_click[0] < var.width_board + var.padding:
            var.symbol_playing, var.color_playing = click(
                var.symbol_playing, var.color_playing, pos_click[0] - var.padding
            )
            var.num_turn += 1
            winner = who_is_winner(var.board)
            if winner == var.symbol_player_1:
                print("Winner is player 1")
            elif winner == var.symbol_player_2:
                print("Player 2 won this match")
            elif var.num_turn == var.nbr_max_turn:
                winner = var.symbol_draw
                print("It's a draw")

    if winner == var.symbol_no_player:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x < var.pos_min_x:
            mouse_x = var.pos_min_x
        elif mouse_x > var.pos_max_x:
            mouse_x = var.pos_max_x
        var.screen.fill(var.color_screen)
        pg.draw.circle(
            var.screen, var.color_playing, (mouse_x, var.padding // 2), var.radius_disk
        )
    return winner
