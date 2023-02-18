#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface.AI import *
from interface.tools_boxes import *
from interface.tools_writing import *


def show_options_play():
    """Show the different options when choosing to play"""
    screen.fill(color_options_screen)
    text_HvH = create_options_text(text_options_play_HvH)
    text_HvAI = create_options_text(text_options_play_HvAI)
    text_AIvAI = create_options_text(text_options_play_AIvAI)
    boxes = center_all([text_HvH, text_HvAI, text_AIvAI])
    status = options_menu_play
    while status == options_menu_play:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(boxes[0], mouse):
                    status = options_play_HvH
                if x_in_rect(boxes[1], mouse):
                    status = options_play_HvAI
                    show_options_AI(1)
                if x_in_rect(boxes[2], mouse):
                    status = options_play_AIvAI
                    show_options_AI(2)
    return status


def start_screen():
    """Show the start screen.
    For now it is only the play button but soon there will be more options"""
    screen.fill(color_options_screen)
    text_play = create_options_text(text_options_play)
    boxes_options = center_all([text_play])
    rect_play = boxes_options[0]
    status = options_menu_start
    while status == options_menu_start:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(rect_play, mouse):
                    status = show_options_play()
    return status


def start_game():
    """Create the board to allow the game to start"""
    screen.fill(color_screen)
    pg.draw.rect(board_surface, color_board, (0, 0, width_board, height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j, color_trans, radius_hole)
    update_screen()
