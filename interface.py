#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

import pygame as pg

from variables import *
from scores import who_is_winner


def center_all(list_text):
    total_size = 0
    for text in list_text:
        total_size += 2 * text_box_spacing + text.get_size()[1]
    total_size += (len(list_text) - 1) * options_spacing
    rect_boxes = []
    y_start = (height_screen - total_size) // 2
    y_now = y_start
    for text in list_text:
        size = text.get_size()
        x_now = (width_screen - size[0]) // 2 - text_box_spacing
        box_rect = (
            x_now,
            y_now,
            size[0] + 2 * text_box_spacing,
            size[1] + 2 * text_box_spacing,
        )
        pg.draw.rect(screen, color_options_box, box_rect)
        screen.blit(text, (x_now + text_box_spacing, y_now + text_box_spacing))
        y_now += 2 * text_box_spacing + size[1] + options_spacing
        rect_boxes.append(box_rect)
    pg.display.update()
    return rect_boxes


def x_in_rect(rect, x, y):
    return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]


def create_options_text(text):
    font = pg.font.SysFont(text_font, text_size)
    return font.render(text, 1, color_options_text)


def show_options_play():
    screen.fill(color_options_screen)
    text_HvH = create_options_text(text_options_play_HvH)
    text_HvIA = create_options_text(text_options_play_HvIA)
    text_IAvIA = create_options_text(text_options_play_IAvIA)
    boxes = center_all([text_HvH, text_HvIA, text_IAvIA])
    status = options_menu_play
    while status == options_menu_play:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(boxes[0], mouse[0], mouse[1]):
                    status = options_play_HvH
    return status


def start_screen():
    screen.fill(color_options_screen)
    text_play = create_options_text(text_options_play)
    boxes_options = center_all([text_play])
    rect_play = boxes_options[0]
    status = options_menu_start
    while status == options_menu_start:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(rect_play, mouse[0], mouse[1]):
                    status = show_options_play()
    return status


def update_screen(rect=None, pause=0):
    screen.blit(board_surface, (padding, padding))
    if rect is not None:
        pg.display.update(rect)
    else:
        pg.display.update()
    sleep(pause)


def draw_circle(n, m, color, r):
    x = n * size_cell + size_cell // 2
    y = m * size_cell + size_cell // 2
    pg.draw.circle(board_surface, color, (x, y), r)


def start_game():
    screen.fill(color_screen)
    pg.draw.rect(board_surface, color_board, (0, 0, width_board, height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j, color_trans, radius_hole)
    update_screen()


def inverse_player(playing):
    if playing == player_1:
        playing = player_2
        color_playing = color_player_2
    else:
        playing = player_1
        color_playing = color_player_1
    return playing, color_playing


def find_low_bound(i):
    col = board[:, i]
    for j in range(len(col) - 1, -1, -1):
        if col[j] == no_player:
            return j
    return -1


def click(player, color, pos_click_x):
    global board

    num_col = pos_click_x // size_cell
    i = find_low_bound(num_col)
    if i == -1:
        return player, color
    board[i, num_col] = player
    x = padding + num_col * size_cell + size_cell // 2
    for y in range(padding // 2, padding + i * size_cell + padding // 2, 5):
        screen.fill(white)
        pg.draw.circle(screen, color, (x, y), radius_disk)
        update_screen()
    draw_circle(num_col, i, color, radius_hole)
    return inverse_player(playing)


def gaming(event):
    global playing, color_playing, num_turn

    winner = no_player
    if event.type == pg.MOUSEBUTTONUP:
        pos_click = pg.mouse.get_pos()
        if padding < pos_click[0] < width_board + padding:
            playing, color_playing = click(
                playing, color_playing, pos_click[0] - padding
            )
            num_turn += 1
            winner = who_is_winner(board)
            if winner == player_1:
                print("Winner is player 1")
            elif winner == player_2:
                print("Player 2 won this match")
            elif num_turn == nbr_max_turn:
                winner = draw
                print("It's a draw")
    
    if winner == no_player:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x < pos_min_x:
            mouse_x = pos_min_x
        elif mouse_x > pos_max_x:
            mouse_x = pos_max_x
        screen.fill(color_screen)
        pg.draw.circle(screen, color_playing, (mouse_x, padding // 2), radius_disk)
    return winner
