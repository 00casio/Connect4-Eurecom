#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface.AI import *
from interface.tools_boxes import *
from interface.tools_writing import *
import variables as var

pg = var.pg

def show_options_play() -> int:
    """Show the different options when choosing to play"""
    text_HvH = create_text_rendered(var.text_options_play_HvH)
    text_HvAI = create_text_rendered(var.text_options_play_HvAI)
    text_AIvAI = create_text_rendered(var.text_options_play_AIvAI)
    text_options = [[text_HvH], [text_HvAI], [text_AIvAI]]
    cancel_box, quit_box = reset_screen(
        var.color_options_screen, text_options, var.color_options_box
    )
    boxes = center_all(text_options)
    status = var.options_menu_play
    while status == var.options_menu_play:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                handle_quit(quit_box, mouse)
                if x_in_rect(boxes[0][0], mouse):
                    status = var.options_play_HvH
                elif x_in_rect(boxes[1][0], mouse):
                    status = var.options_play_HvAI
                    show_options_AI(1)
                elif x_in_rect(boxes[2][0], mouse):
                    status = var.options_play_AIvAI
                    show_options_AI(2)
                elif x_in_rect(cancel_box, mouse):
                    status = var.options_clicked_cancel
    if var.difficulty_AI_2 == -1 and status not in [
        var.options_play_HvH,
        var.options_clicked_cancel,
    ]:
        status = show_options_play()
    return status


def start_screen() -> int:
    """Show the start screen.
    For now it is only the play button but soon there will be more options"""
    screen.fill(color_options_screen)
    quit_box = draw_quit_box()
    text_play = create_text_rendered(var.text_options_play)
    boxes_options = center_all([[text_play]])
    rect_play = boxes_options[0][0]
    status = var.options_menu_start
    while status == var.options_menu_start:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                handle_quit(quit_box, mouse)
                if x_in_rect(rect_play, mouse):
                    status = show_options_play()
    if status == var.options_clicked_cancel:
        status = start_screen()
    return status


def start_game() -> None:
    """Create the board to allow the game to start"""
    screen.fill(var.color_screen)
    pg.draw.rect(var.board_surface, var.color_board, (0, 0, var.width_board, var.height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j, var.color_trans, var.radius_hole)
    update_screen()
