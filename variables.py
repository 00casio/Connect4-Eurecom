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


class Variables:
    def __init__(self):
        # Symbols
        self.symbol_draw = Symbol("-1")
        self.symbol_no_player = Symbol("0")
        self.symbol_player_1 = Symbol("1")
        self.symbol_player_2 = Symbol("2")

        # Board
        self.board = np.array(
            [
                [symbol_no_player] * 7,
                [symbol_no_player] * 7,
                [symbol_no_player] * 7,
                [symbol_no_player] * 7,
                [symbol_no_player] * 7,
                [symbol_no_player] * 7,
            ]
        )
        self.nbr_max_turn = board.size

        # AI
        self.difficulty_AI_1: int = -1
        self.difficulty_AI_2: int = -1
        self.symbol_player_AI = symbol_no_player

        # Boxes for levels of AI
        self.box_out = 0
        self.boxAI_out = -1
        self.boxAI_play = -255
        self.boxAI_cancel = 255
        self.boxAI_text_levels = [
            "Start",
            "Start",
            "Meh, begin",
            "Get my a** kicked",
            "Welcome to Hell",
        ]

        # Colors
        self.white = Color(255, 255, 255)
        self.black = Color(0, 0, 0)
        self.red = Color(255, 0, 0)
        self.green = Color(0, 255, 0)
        self.blue = Color(38, 60, 255)
        self.dark_blue = Color(0, 0, 229)
        self.light_blue = Color(30, 160, 255)
        self.cyan = Color(45, 245, 255)
        self.color_trans = Color(0, 0, 0, 0)
        self.color_player_1 = red
        self.color_player_2 = green
        self.color_board = blue
        self.color_screen = white
        self.color_options_screen = light_blue
        self.color_options_highlight_box = cyan
        self.color_options_highlight_text = black
        self.color_options_box = blue
        self.color_options_text = white

        # Size
        self.size_cell = 100
        self.padding = int(size_cell * 1.5)
        self.width_board = 7 * size_cell
        self.height_board = 6 * size_cell
        self.radius_hole = 40
        self.radius_disk = 49
        self.width_screen = 2 * padding + width_board
        self.height_screen = 2 * padding + height_board
        self.options_spacing = padding // 4
        self.text_box_spacing = padding // 10
        self.center_screen = (
            width_screen // 2,
            height_screen // 2,
        )

        # Options
        self.options_menu_start = -1
        self.options_menu_play = 0
        self.options_play_HvH = 1
        self.options_play_HvAI = 2
        self.options_play_AIvAI = 3
        self.options_clicked_cancel = -255

        # Pygame
        self.fps = 30
        self.screen_title = "Connect 4"
        self.pos_min_x = padding + size_cell // 2
        self.pos_max_x = padding + width_board - size_cell // 2
        self.text_size = 30
        self.text_font = "monospace"
        self.text_options_play = "Play"
        self.text_options_play_HvH = "Human vs. Human"
        self.text_options_play_HvAI = "Human vs. IA"
        self.text_options_play_AIvAI = "Watch the world burn"
        self.text_options_difficulty_HvAI = "Choose your poison"
        self.text_options_difficulty_AIvAI = "How badly do you want this game to go ?"
        self.text_difficulty_options = [
            "",
            self.text_options_difficulty_HvAI,
            self.text_options_difficulty_AIvAI,
        ]

        # Fonts
        self.main_font = pg.font.SysFont(text_font, text_size)

        # Quit and cancel
        self.text_cancel_box = "Cancel"
        self.coor_cancel_box = (10, 10)
        self.text_quit_box = "Quit"
        self.coor_quit_box = (width_screen - 10, 10)

