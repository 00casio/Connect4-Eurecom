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
