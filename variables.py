#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pygame as pg

pg.init()

# Symbols
no_player = "0"
player_1 = "1"
player_2 = "2"

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

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (38, 60, 255)
dark_blue = (0, 0, 229)
light_blue = (30, 160, 255)
color_trans = (0, 0, 0, 0)
color_player_1 = red
color_player_2 = green
color_board = blue
color_screen = white
color_options_screen = light_blue
color_options_box = blue
color_options_text = white

# Size
size_cell = 100
padding = size_cell
width_board = 7 * size_cell
height_board = 6 * size_cell
radius_hole = 40
radius_disk = 49
width_screen = 2 * padding + width_board
height_screen = 2 * padding + height_board
options_spacing = padding // 4
text_box_spacing = padding // 10

# Options
options_menu_start = -1
options_menu_play = 0
options_play_HvH = 1
options_play_HvIA = 2
options_play_IAvIA = 3

# Pygame
fps = 30
screen_title = "Connect 4"
pos_min_x = padding + size_cell // 2
pos_max_x = padding + width_board - size_cell // 2
text_size = 30
text_font = "monospace"
text_options_play = "Play"
text_options_play_HvH = "Human vs. Human"
text_options_play_HvIA = "Human vs. IA"
text_options_play_IAvIA = "Watch the world burn"

# Starting everything
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width_screen, height_screen), 0, 32)
pg.display.set_caption(screen_title)
board_surface = pg.surface.Surface((width_board, height_board)).convert_alpha()
playing = player_1
color_playing = color_player_1
