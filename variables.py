#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any

import pygame as pg

pg.init()

Color = pg.Color


class Symbol:
    """The Symbol class is used to make the difference between two players"""

    def __init__(self, value: Any) -> None:
        self.v = value

    def __eq__(self, o: object) -> Any:
        if isinstance(o, Symbol):
            return o.v == self.v
        elif isinstance(o, type(self.v)):
            return o == self.v
        else:
            return NotImplemented


class Variables:
    def __init__(self) -> None:
        # Symbols
        self.symbol_no_player = "0"
        self.symbol_player_1 = "1"
        self.symbol_player_2 = "2"

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
        self.grey = Color(200, 200, 200)
        self.color_trans = Color(0, 0, 0, 0)
        self.color_player_1 = self.red
        self.color_player_2 = self.green
        self.color_board = self.blue
        self.color_screen = self.white
        self.color_highlight_column = self.grey
        self.color_options_screen = self.light_blue
        self.color_options_highlight_box = self.cyan
        self.color_options_highlight_text = self.black
        self.color_options_box = self.blue
        self.color_options_text = self.white

        # Size
        self.size_cell = 100
        self.padding = int(self.size_cell * 1.5)
        self.width_board = 7 * self.size_cell
        self.height_board = 6 * self.size_cell
        self.radius_hole = 40
        self.radius_disk = 49
        self.width_screen = 2 * self.padding + self.width_board
        self.height_screen = 2 * self.padding + self.height_board
        self.options_spacing = self.padding // 4
        self.text_box_spacing = self.padding // 10
        self.center_screen = (
            self.width_screen // 2,
            self.height_screen // 2,
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
        self.pos_min_x = self.padding + self.size_cell // 2
        self.pos_max_x = self.padding + self.width_board - self.size_cell // 2
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

        # Sounds
        self.sound_click_box = "sounds/box.mp3"
        self.sound_error = "sounds/error.mp3"
        self.sound_disk_touch = "sounds/tuck.mp3"
        self.sound_winner_draw = "sounds/draw.mp3"
        self.sound_winner_victory = "sounds/victory.mp3"

        # Fonts
        self.main_font = pg.font.SysFont(self.text_font, self.text_size)

        # Quit and cancel
        self.text_cancel_box = "Cancel"
        self.coor_cancel_box = (10, 10)
        self.text_quit_box = "Quit"
        self.coor_quit_box = (self.width_screen - 10, 10)
        self.message_quit = "You chose to quit the game\nYou are disapointing me"
