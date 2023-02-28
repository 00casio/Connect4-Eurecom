#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from variables import Variables
import numpy as np
from typing import Any
from AI_test import best_col_prediction

var = Variables()

class Symbol:
    """ The Symbol class is used to make the difference between two players """
    def __init__(self, value: Any) -> None:
        self.v = value

    def __eq__(self, o: object) -> Any:
        if not isinstance(o, Symbol):
            return NotImplemented
        return o.v == self.v

class Element:
    """ An element is composed of a box and text """
    def __init__(self, box, text, color_box, color_text):
        raise NotImplementedError("Not finished")
        self.box = box
        self.text = text
        self.color_box = color_box
        self.color_text = color_text
    
    def change_text_color(self, new_color):
        raise NotImplementedError("Not for now")
    def change_box_color(self):
        raise NotImplementedError("Not for now")

class Screen:
    """ A screen is composed of what is shown to the user """
    def __init__(self, name: str, width: int, height: int):
        self.name = name
        self.width = width
        self.height = height
        self.elements = []
        self.screen = None

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
    """ The gaming screen is used for the gaming part of the program """
    def __init__(self, name: str, width: int, height: int) -> None:
        Screen.__init__(self, name, width, height)
        self.color_screen = var.white
        self.color_board = var.light_blue
        self.width_board = var.width_board
        self.height_board = var.height_board
        self.board_surface = pg.surface.Surface((self.width_board, self.height_board)).convert_alpha()

    def draw_board():
        self.screen.fill(self.color_screen)
        pg.draw.rect(self.board_surface, self.color_board, (0, 0, self.width_board, self.height_board))
        for i in range(7):
            for j in range(6):
                draw_circle(i, j, var.color_trans, var.radius_hole)
        update_screen()

    def find_free_slot(self, board, i: int) -> int:
        """Return the index of the first free slot"""
        col = board[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == var.symbol_no_player:
                return j
        return -1

    def animate_fall(self, col: int, row: int, color_player: pg.Color) -> None:
        for y in range(var.padding+num_col*var.size_cell+ var.size_cell//2, 5):
            self.screen.fill(var.white)
            pg.draw.circle(self.screen, color_player, (x, y), var.radius_disk)
            update_screen()
        pg.draw.circle(self.board_surface, color, (x, y), var.radius_hole)

    def player_move(self, board, col: int) -> None:
        row = find_free_slot(board)
        self.animate_fall()
        raise NotImplementedError("Not finished")

class Player:
    """ The class that keep all the options for a player """
    def __init__(self, symbol: Any, color: pg.Color, AI: bool):
        self.symbol = Symbol(symbol)
        self.color = color
        self.is_ai = AI

    def play(self, board, screen):
        if self.is_ai:
            col = best_col_prediction(board, self.symbol)
        else:
            click = screen.get_mouse_pos()
            col = (click[0] - padding) // var.size_cell
        return col
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False
        return self.symbol == other.symbol

class Game:
    """ The big class that will regulate everything """
    def __init__(self):
        self.player_1: Player = None
        self.player_2: Player = None
        self.player_playing: Player = None
        self.player_null = Player(var.symbol_no_player, var.color_trans, False)
        self.board = np.array([[symbol_no_player] * 7 for i in range(6)])

    def inverse_player(self):
        """Return the symbols of the opponent of the player currently playing"""
        if self.player_playing == self.player_1:
            self.player_playing = self.player_2
        elif self.player_playing == self.player_2:
            self.player_playing = self.player_1
        else:
            raise ValueError("How is that possible ? Read carefully the log and send me everything")

    def state_to_bits(self, state: np.ndarray[np.dtype[np.float64], np.float64]) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        n = "0b"
        for j in range(len(state[0]) - 1, -1, -1):
            n += "0"
            for i in range(len(state)):
                n += f"{int(state[i, j])}"  # <==> n += str(b)
        return n

    def state_win(self, state: np.ndarray[np.float64]) -> bool:
        bits = int(state_to_bits(state), 2)

        # Horizontal check
        m = bits & (bits >> 7)
        if m & (m >> 14):
            return True
        # Vertical
        m = bits & (bits >> 1)
        if m & (m >> 2):
            return True
        # Diagonal \
        m = bits & (bits >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = bits & (bits >> 8)
        if m & (m >> 16):
            return True
        # Nothing found
        return False

    def who_is_winner(self):
        s = self.board.shape
        state_symbol_player_1 = np.zeros(s)
        state_symbol_player_2 = np.zeros(s)
        state_symbol_player_1[np.where(self.board == self.player_1.symbol)] = 1
        state_symbol_player_2[np.where(self.board == self.player_2.symbol)] = 1
        if self.state_win(state_symbol_player_1):
            return self.player_1.symbol
        elif self.state_win(state_symbol_player_2):
            return self.player_2.symbol
        else:
            return self.player_null.symbol

    def draw_winner(self):
        raise NotImplementedError("Not for now")
    def start_game(self):
        raise NotImplementedError("Not for now")
    def options_screen(self):
        raise NotImplementedError("Not for now")
    def play_screen(self):
        raise NotImplementedError("Not for now")
