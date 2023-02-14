#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep

import numpy as np
import pygame as pg

from variables import *

# Board
board = np.array(
    [
        [no_player] * 7,
        [no_player] * 7,
        [no_player] * 7,
        [no_player] * 7,
        [no_player] * 7,
        [no_player] * 7,
    ]
)

# initializing pygame window
pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width_screen, height_screen), 0, 32)
pg.display.set_caption(screen_title)
board_surface = pg.surface.Surface((width_board, height_board)).convert_alpha()


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
    status = 0
    while status == 0:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(boxes[0], mouse[0], mouse[1]):
                    status = 1
    return status


def start_screen():
    screen.fill(color_options_screen)
    text_play = create_options_text(text_options_play)
    boxes_options = center_all([text_play])
    rect_play = boxes_options[0]
    status = 0
    while status == 0:
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


def draw_circle(n, m, color):
    x = n * size_cell + size_cell // 2
    y = m * size_cell + size_cell // 2
    pg.draw.circle(board_surface, color, (x, y), radius_disk)


def start_game():
    screen.fill(color_screen)
    pg.draw.rect(board_surface, color_board, (0, 0, width_board, height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j, color_trans)
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
    draw_circle(num_col, i, color)
    return inverse_player(playing)


def gaming(event):
    global playing, color_playing

    if event.type == pg.MOUSEBUTTONUP:
        pos_click = pg.mouse.get_pos()
        if padding < pos_click[0] < width_board + padding:
            playing, color_playing = click(
                playing, color_playing, pos_click[0] - padding
            )

    mouse_x, mouse_y = pg.mouse.get_pos()
    if mouse_x < pos_min_x:
        mouse_x = pos_min_x
    elif mouse_x > pos_max_x:
        mouse_x = pos_max_x
    screen.fill(color_screen)
    pg.draw.circle(screen, color_playing, (mouse_x, padding // 2), radius_disk)


start_screen()

start_game()
playing = player_1
color_playing = color_player_1

# Run the game loop forever
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        gaming(event)
    update_screen((0, 0, padding, width_screen))
    CLOCK.tick(fps)
