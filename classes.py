#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
import variables as var
from typing import Any
from AI_test import best_col_prediction

class Symbol:
    def __init__(self, value: Any) -> None:
        self.v = value

    def __eq__(self, o: object) -> Any:
        if not isinstance(o, Symbol):
            return NotImplemented
        return o.v == self.v

class Element:
    def __init__(self, box, text, color_box, color_text):
        self.box = box
        self.text = text
        self.color_box = color_box
        self.color_text = color_text
    
    def change_text_color(self, new_color):
        raise NotImplementedError("Not for now")
    def change_box_color(self):
        raise NotImplementedError("Not for now")

class Screen:
    def __init__(self, name: str):
        self.name = name
        self.elements = []

    def add_box_text(self, position, text, color_box, color_text):
        raise NotImplementedError("Not for now")
        self.elements.append(Element(box, text, color_box, color_text))

    def get_mouse_pos(self):
        raise NotImplementedError("Not for now")
        """ Return the mouse position if conditions are met """
        return pg.mouse.get_pos()
    
    def draw_all_centered(self, list_text):
        raise NotImplementedError("Not for now")

class GamingScreen(Screen):
    def __init__(self, name: str) -> None:
        Screen.__init__(self, name)
        self.init_board()

    def init_board(self):
        self.board = []
        raise NotImplementedError("Not for now")

    def find_free_slot(self, i: int) -> int:
        """Return the index of the first free slot"""
        col = self.board[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == var.symbol_no_player:
                return j
        return -1

    def animate_fall(self, col: int, row: int) -> None:
        raise NotImplementedError("Not for now")

    def player_move(self, col: int) -> None:
        row = find_free_slot(self.board)
        self.animate_fall()
        raise NotImplementedError("Not finished")

class Player:
    def __init__(self, symbol: Any, AI: bool, screen: GamingScreen):
        self.symbol = Symbol(symbol)
        self.is_ai = AI
        self.screen = screen

    def play(board):
        if self.is_ai:
            col = best_col_prediction(board, self.symbol)
        else:
            click = self.screen.get_mouse_pos()
            col = (click[0] - padding) // var.size_cell
        return col

class Game:
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.player_playing = None

    def inverse_player(self):
        raise NotImplementedError("Not for now")

    def who_is_winner(self):
        raise NotImplementedError("Not for now")
    def draw_winner(self):
        raise NotImplementedError("Not for now")
    def start_game(self):
        raise NotImplementedError("Not for now")
    def options_screen(self):
        raise NotImplementedError("Not for now")
    def play_screen(self):
        raise NotImplementedError("Not for now")
