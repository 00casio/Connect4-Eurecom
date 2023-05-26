#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Any, Iterator, Optional

import numpy as np
import pygame as pg
from playsound import playsound

import ai.libai as libai
from ai.minimax_ai import minimax, opponent
from core.screens import GamingScreen, OptionsScreen, Screen, Screen_AI
from core.structure import Board, Node
from core.utils import Box, Config, Symbol
from core.variables import Rect, Variables, Surface
from extern.gesture import *

pg.init()


class Player:
    """The class that keep all the options for a player"""

    def __init__(
        self, var: Variables, number: int, AI: bool, difficulty: int = -1
    ) -> None:
        """Initialize the values for the Players"""
        self.var = var
        if number == 0:
            self.symbol = Symbol(self.var.symbol_no_player)
            self.color = self.var.color_trans
        elif number == 1:
            self.symbol = Symbol(self.var.symbol_player_1)
            self.color = self.var.color_player_1
        elif number == 2:
            self.symbol = Symbol(self.var.symbol_player_2)
            self.color = self.var.color_player_2
        else:
            raise ValueError("There can not be more than 2 players")
        self.is_ai = AI
        self.ai_difficulty = difficulty

    def play(
        self, board: Board, root: Node, screen: Screen, volume: bool, ai_cpp
    ) -> tuple[int, int]:
        """The function used when it's the player's turn"""
        if self.is_ai:
            if ai_cpp is None:
                score, col = minimax(root, 0, 0, True)
            else:
                col = ai_cpp.aiMove(3 * self.ai_difficulty + 1)
        else:
            p = self.var.padding
            box_allowed = Rect(p, p, self.var.width_board, self.var.height_board)
            click = screen.click(box_allowed, print_disk=True, symbol_player=self.symbol)
            col = (click[0] - self.var.padding) // self.var.size_cell
        if ai_cpp is None:
            for candidate in root.children:
                if candidate.column_played == col:
                    break
            new_root = candidate
            # print(root.depth, new_root.nbr_move)
            # print(new_root.depth, new_root.nbr_move)
            root = new_root.remove_old_root()
            root.create_tree(4)

        row = board.find_free_slot(col)
        if row == -1:
            if volume:
                playsound(self.var.sound_error, block=False)
            col, row, root = self.play(board, root, screen, volume, ai_cpp)
        return (col, row, root)

    def __eq__(self, other: object) -> bool:
        """Allow to compare a player and another object"""
        eq: bool = False
        if isinstance(other, Player):
            eq = self.symbol == other.symbol
        elif isinstance(other, Symbol):
            eq = self.symbol == other
        return eq


class Game:
    """The big class that will regulate everything"""

    def __init__(
        self, args: Namespace, ai_cpp_1: libai.Game, ai_cpp_2: libai.Game
    ) -> None:
        """Initialize the value needed for the game"""

        # Players
        self.var = Variables()
        self.conf = Config(self.var, args)
        self.volume = self.var.sound
        self.camera = self.var.camera
        self.libai = self.var.libai
        size_screen = (self.var.width_screen, self.var.height_screen)

        # Gestures
        self.gestures = GestureController(size_screen)

        # TODO: communication

        # AI
        self.root: Optional[Node] = None
        self.ai_cpp_1 = ai_cpp_1
        self.ai_cpp_2 = ai_cpp_2

        # Players
        self.player_1 = Player(self.var, 1, False, None)
        self.player_2 = Player(self.var, 2, False, None)
        self.player_null = Player(self.var, 0, False)
        self.player_playing = self.player_1

        # Pygame
        self.screen = pg.display.set_mode(size_screen, 0, 32)
        pg.display.set_caption(self.var.screen_title)

    def inverse_player(self) -> None:
        """Return the symbols of the opponent of the player currently playing"""
        if self.player_playing == self.player_1:
            self.player_playing = self.player_2
        elif self.player_playing == self.player_2:
            self.player_playing = self.player_1
        else:
            raise ValueError(
                "How is that possible ? Read carefully the error and send me everything"
            )

    def who_is_winner(self) -> Player:
        """Return the symbol of the player currently playing"""
        if self.board.state_win(self.player_1.symbol):
            return self.player_1
        elif self.board.state_win(self.player_2.symbol):
            return self.player_2
        else:
            return self.player_null

    def start(self, skip_start_screen=False) -> None:
        """The start function to use when wanting to start the program"""
        if not skip_start_screen:
            self.draw_start_screen()
        else:
            self.draw_play_options()
        self.board = Board()
        self.CLOCK = pg.time.Clock()
        self.num_turn = 0
        self.start_game()

    def draw_start_screen(self) -> None:
        """Show the starting screen, choose between the different possinilities"""

        start_screen = Screen(
            self.var,
            self.screen,
            self.gestures,
            cancel_box=False,
            volume=self.volume,
            camera=self.camera,
        )
        box_play = Box(self.var.text_options_play)
        box_options = Box(self.var.text_options_options)
        start_screen.center_all([[box_play], [box_options]])

        self.status = self.var.options_menu_start
        while self.status == self.var.options_menu_start:
            mouse = start_screen.click()
            if start_screen.x_in_rect(mouse, box_play.box):
                self.draw_play_options()
            elif start_screen.x_in_rect(mouse, box_options.box):
                self.draw_options_screen()
        if self.status == self.var.options_clicked_cancel:
            self.draw_start_screen()

    def draw_options_screen(self) -> None:
        """Draw the options screen (language, if camera, if sound, etc.)"""
        options = OptionsScreen(
            self.var, self, self.screen, self.gestures, self.volume, self.camera
        )
        click = options.click()
        while options.box_clicked != self.var.boxAI_cancel:
            if options.x_in_rect(click, options.vol):
                self.volume = not self.volume
                options.volume = self.volume
            elif options.x_in_rect(click, options.cam):
                self.camera = not self.camera
                options.camera = self.camera
            elif options.x_in_rect(click, options.flags[0]):
                self.conf.load_language("en")
            elif options.x_in_rect(click, options.flags[1]):
                self.conf.load_language("fr")
            elif options.x_in_rect(click, options.flags[2]):
                self.conf.load_language("cat")
            options.reset_options_screen()
            click = options.click()
        self.status = self.var.options_clicked_cancel

    def draw_play_options(self) -> None:
        """Show the different options when choosing to play"""
        self.ai_cpp_1.resetBoard()
        self.ai_cpp_2.resetBoard()
        screen = Screen(self.var, self.screen, self.gestures, self.volume, self.camera)
        box_HvH = Box(self.var.text_options_play_HvH)
        box_HvAI = Box(self.var.text_options_play_HvAI)
        box_AIvAI = Box(self.var.text_options_play_AIvAI)
        screen.center_all([[box_HvH], [box_HvAI], [box_AIvAI]])

        self.status = self.var.options_menu_play
        self.screen_AI = None
        while self.status == self.var.options_menu_play:
            mouse = screen.click()
            if screen.x_in_rect(mouse, box_HvH):
                self.status = self.var.options_play_HvH
                self.player_1 = Player(self.var, 1, False)
                self.player_2 = Player(self.var, 2, False)
            elif screen.x_in_rect(mouse, box_HvAI):
                self.status = self.var.options_play_HvAI
                self.screen_AI = Screen_AI(
                    self.var,
                    self.screen,
                    self.gestures,
                    volume=self.volume,
                    camera=self.camera,
                    number_AI=1,
                )
                self.player_1 = Player(self.var, 1, False)
                self.player_2 = Player(self.var, 2, True, self.screen_AI.diff_AI_1)
            elif screen.x_in_rect(mouse, box_AIvAI):
                self.status = self.var.options_play_AIvAI
                self.screen_AI = Screen_AI(
                    self.var,
                    self.screen,
                    self.gestures,
                    volume=self.volume,
                    camera=self.camera,
                    number_AI=2,
                )
                self.player_1 = Player(self.var, 1, True, self.screen_AI.diff_AI_1)
                self.player_2 = Player(self.var, 2, True, self.screen_AI.diff_AI_2)
            if screen.x_in_rect(mouse, screen.cancel_box):
                self.status = self.var.options_clicked_cancel
        if (self.player_1.is_ai and self.player_1.ai_difficulty == -1) or (
            self.player_2.is_ai and self.player_2.ai_difficulty == -1
        ):
            if self.status not in [
                self.var.options_play_HvH,
                self.var.options_clicked_cancel,
            ]:
                self.draw_play_options()

    def select_opponent(self):
        """
        TODO:
            Choose if the opponent is local or remote
            Put the communication part in here
            Pick who is player 1 and player 2
        """
        pass

    def start_game(self) -> None:
        """Start the game"""
        self.player_playing = self.player_1
        gaming = GamingScreen(
            self.var, self.screen, self.gestures, self.volume, self.camera
        )
        gaming.draw_board()
        gaming.draw_token(self.var.width_screen // 2, self.var.padding // 2, self.player_playing.symbol, self.var.radius_disk, col_row=False, screen=gaming.screen)
        pg.display.update()
        if not self.libai:
            self.root = Node(-1, None, self.player_playing.symbol.v, 0)
            self.root.board = self.board.copy()
            self.root.create_tree(4)
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size
        ):
            if self.player_playing == self.player_1:
                col, row, self.root = self.player_1.play(
                    self.board, self.root, gaming, self.volume, self.ai_cpp_1
                )
                if self.libai:
                    self.ai_cpp_2.humanMove(col)
            else:
                col, row, self.root = self.player_2.play(
                    self.board, self.root, gaming, self.volume, self.ai_cpp_2
                )
                if self.libai:
                    self.ai_cpp_1.humanMove(col)
            gaming.animate_fall(col, row, self.player_playing.symbol)
            self.board[row, col] = self.player_playing.symbol.v
            self.inverse_player()
            self.num_turn += 1
        self.draw_winner(gaming.board_surface, (col, row))

    def draw_winner(self, board_surface: Surface, lastclick: tuple[int, int]) -> None:
        """Draw the winner on the screen, with the line that made it win"""
        winner = self.who_is_winner()
        text = f"Player {winner.symbol.v} won !"
        if self.conf.language == "fr":
            text = f"Le joueur {winner.symbol.v} a gagné !"
        elif self.conf.language == "cat":
            text = f"Nyah ! {winner.symbol.v} nyah !"
        sound = self.var.sound_winner_victory
        End = Screen(
            self.var, self.screen, self.gestures, volume=self.volume, camera=self.camera, cancel_box=False
        )
        End.screen.fill(self.var.color_screen)
        End.draw_quit_box()
        if winner != self.player_1 and winner != self.player_2:
            text = self.var.text_draw[self.conf.language]
            sound = self.var.sound_winner_draw
        print(text)

        p = self.var.padding
        box_winner = Box(text, color_text=self.var.black, color_rect=self.var.white, coordinate=(self.var.width_screen//2, p//2), align=(0, 0))
        box_winner.font_size = 64
        box_winner.render(self.screen)

        if self.volume:
            playsound(sound, block=False)
        self.screen.blit(board_surface, (p, p))
        bits = int(self.board.state_to_bits(), 2)

        def complete(bits: int, direction: int) -> None:
            d = {0: 7, 1: 1, 2: 6, 3: 8}
            m = bits & (bits >> d[direction])
            m2 = m & (m >> 2 * d[direction])
            if m2:
                bs = bin(m2)[2:]
                i = 48 - ("0" * (49 - len(bs)) + bs).find("1")
                p = self.var.padding
                c = self.var.size_cell
                x_s = p + (i // 7) * c + c // 2
                y_s = self.var.height_board - (i % 7 - 1) * c
                x_e = x_s
                y_e = y_s
                if direction in [0, 2, 3]:
                    x_e += 3 * c
                if direction in [1, 3]:
                    y_e -= 3 * c
                if direction == 2:
                    y_e += 3 * c
                pg.draw.line(self.screen, self.var.black, (x_s, y_s), (x_e, y_e), 15)

        complete(bits, 0)  # Horizontal check
        complete(bits, 1)  # Vert
        complete(bits, 2)  # \
        complete(bits, 3)  # /

        pg.event.get()

        pg.display.update()
        End.click()
        self.start(skip_start_screen=True)
