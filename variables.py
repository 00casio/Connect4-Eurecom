#!/usr/bin/python3
# -*- coding: utf-8 -*-

import typing as typ

import numpy as np
import pygame

pg = pygame
pg.init()

# Types hints
Any = typ.Any
Surface = pg.Surface
Rect = pg.Rect
Color = pg.Color
Event = pg.event.Event
Font = pg.font.Font


# Classes


class Symbol:
    def __init__(self, value: Any) -> None:
        self.v = value

    def __eq__(self, o: object) -> Any:
        if not isinstance(o, Symbol):
            return NotImplemented
        return o.v == self.v


# Symbols
symbol_draw = Symbol("-1")
symbol_no_player = Symbol("0")
symbol_player_1 = Symbol("1")
symbol_player_2 = Symbol("2")

# Board
board = np.array(
    [
        [symbol_no_player] * 7,
        [symbol_no_player] * 7,
        [symbol_no_player] * 7,
        [symbol_no_player] * 7,
        [symbol_no_player] * 7,
        [symbol_no_player] * 7,
    ]
)
nbr_max_turn = board.size

# AI
difficulty_AI_1: int = 0
difficulty_AI_2: int = 0
symbol_player_AI = symbol_no_player

# Boxes for levels of AI
boxAI_out = -1
boxAI_play = -255
boxAI_text_levels = [
    "Start",
    "Start",
    "Meh, begin",
    "Get my a** kicked",
    "Welcome to Hell",
]

# Colors
white = Color(255, 255, 255)
black = Color(0, 0, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(38, 60, 255)
dark_blue = Color(0, 0, 229)
light_blue = Color(30, 160, 255)
cyan = Color(45, 245, 255)
color_trans = Color(0, 0, 0, 0)
color_player_1 = red
color_player_2 = green
color_board = blue
color_screen = white
color_options_screen = light_blue
color_options_highlight_box = cyan
color_options_highlight_text = black
color_options_box = blue
color_options_text = white

# Size
size_cell = 100
padding = int(size_cell * 1.5)
width_board = 7 * size_cell
height_board = 6 * size_cell
radius_hole = 40
radius_disk = 49
width_screen = 2 * padding + width_board
height_screen = 2 * padding + height_board
options_spacing = padding // 4
text_box_spacing = padding // 10
center_screen = (width_screen // 2, height_screen // 2, )

# Options
options_menu_start = -1
options_menu_play = 0
options_play_HvH = 1
options_play_HvAI = 2
options_play_AIvAI = 3

# Pygame
fps = 30
screen_title = "Connect 4"
pos_min_x = padding + size_cell // 2
pos_max_x = padding + width_board - size_cell // 2
text_size = 30
text_font = "monospace"
text_options_play = "Play"
text_options_play_HvH = "Human vs. Human"
text_options_play_HvAI = "Human vs. IA"
text_options_play_AIvAI = "Watch the world burn"
text_options_difficulty_HvAI = "Choose your poison"
text_options_difficulty_AIvAI = "How badly do you want this game to go ?"

# Fonts
main_font = pg.font.SysFont(text_font, text_size)


# Starting everything
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width_screen, height_screen), 0, 32)
pg.display.set_caption(screen_title)
board_surface = pg.surface.Surface((width_board, height_board)).convert_alpha()
symbol_playing = symbol_player_1
color_playing = color_player_1
num_turn = 0
