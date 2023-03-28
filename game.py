#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pygame as pg
from typing import Any, Iterator, Optional
from argparse import Namespace

from gesture import *
# from headers import Rect
from minimax_ai import minimax, opponent
from screens import GamingScreen, OptionsScreen, Screen, Screen_AI
from utils import Config, Symbol
from structure import Node, Board
from variables import Variables, Rect
from playsound import playsound

pg.init()


class Player:
    """The class that keep all the options for a player"""

    def __init__(
        self, var: Variables, number: int, AI: bool, difficulty: int = -1
    ) -> None:
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
        self, board: Board, root: Node, screen: Screen, volume: bool
    ) -> tuple[int, int]:
        if self.is_ai:
            score, col = minimax(root, 0, 0, True)
        else:
            p = self.var.padding
            box_allowed = Rect(p, p, self.var.width_board, self.var.height_board)
            click = screen.click(box_allowed, print_disk=True, color_disk=self.color)
            col = (click[0] - self.var.padding) // self.var.size_cell
        for candidate in root.children:
            if candidate.column_played == col:
                break
        new_root = candidate
        # print(root.depth, new_root.nbr_move)
        # print(new_root.depth, new_root.nbr_move)
        root = new_root.remove_old_root()
        root.create_tree(4)

        row = board.find_free_slot(col)
        if row == -1 and volume:
            playsound(self.var.sound_error, block=False)
            col, row, root = self.play(board, root, screen, volume)
        return (col, row, root)

    def __eq__(self, other: object) -> bool:
        eq: bool = False
        if isinstance(other, Player):
            eq = self.symbol == other.symbol
        elif isinstance(other, Symbol):
            eq = self.symbol == other
        return eq


class Game:
    """The big class that will regulate everything"""

    def __init__(self, var: Variables, args: Namespace) -> None:
        # Gestures
        self.gestures = GestureController()

        # Players
        self.var = var
        self.root: Optional[Node] = None
        self.player_1 = Player(self.var, 1, False, None)
        self.player_2 = Player(self.var, 2, False, None)
        self.player_playing = self.player_1
        self.player_null = Player(self.var, 0, False)
        self.screen = pg.display.set_mode(
            (self.var.width_screen, self.var.height_screen), 0, 32
        )
        pg.display.set_caption(self.var.screen_title)
        self.conf = Config(self.var, args)
        self.volume = self.var.sound
        self.camera = self.var.camera

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
        if self.board.state_win(self.player_1.symbol):
            return self.player_1
        elif self.board.state_win(self.player_2.symbol):
            return self.player_2
        else:
            return self.player_null

    def start(self) -> None:
        self.draw_start_screen()
        self.board = Board()
        self.CLOCK = pg.time.Clock()
        self.num_turn = 0
        self.start_game()

    def start_game(self) -> None:
        gaming = GamingScreen(
            self.var, self.screen, self.gestures, self.volume, self.camera
        )
        gaming.draw_board()
        self.player_playing = self.player_1
        self.root = Node(-1, None, self.player_playing.symbol.v, 0)
        self.root.board = self.board.copy()
        self.root.create_tree(4)
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size
        ):
            if self.player_playing == self.player_1:
                col, row, self.root = self.player_1.play(
                    self.board, self.root, gaming, self.volume
                )
            else:
                col, row, self.root = self.player_2.play(
                    self.board, self.root, gaming, self.volume
                )
            gaming.animate_fall(col, row, self.player_playing.color)
            self.board[row, col] = self.player_playing.symbol.v
            self.inverse_player()
            self.num_turn += 1
        self.draw_winner(gaming, (col, row))

    def draw_winner(self, screen: GamingScreen, lastclick: tuple[int, int]) -> None:
        winner = self.who_is_winner()
        sound = self.var.sound_winner_victory
        End = Screen(
            self.var, self.screen, self.gestures, volume=self.volume, camera=self.camera
        )
        End.screen.fill(self.var.color_screen)
        End.draw_quit_box()
        text_winner = End.create_text_rendered(f"Player {winner.symbol.v} won !")
        if winner == self.player_1:
            print("Winner is the first player")
        elif winner == self.player_2:
            print("Winner is the second player")
        else:
            text_winner = End.create_text_rendered("No one won")
            print("That is a draw")
            sound = self.var.sound_winner_draw
        p = self.var.padding
        if self.volume:
            playsound(sound, block=False)
        self.screen.blit(screen.board_surface, (p, p))
        box_winner = End.write_on_line(
            [text_winner], winner.color, self.var.width_screen, p // 2
        )
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

        pg.display.update()
        screen.click()

    def draw_options_screen(self) -> None:
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
            options.reset_options_screen()
            click = options.click()
        self.status = self.var.options_clicked_cancel

    def draw_play_options(self) -> None:
        """Show the different options when choosing to play"""
        screen = Screen(self.var, self.screen, self.gestures, self.volume, self.camera)
        text_HvH = screen.create_text_rendered(self.var.text_options_play_HvH)
        text_HvAI = screen.create_text_rendered(self.var.text_options_play_HvAI)
        text_AIvAI = screen.create_text_rendered(self.var.text_options_play_AIvAI)
        text_options = [[text_HvH], [text_HvAI], [text_AIvAI]]
        boxes = screen.center_all(text_options)
        self.status = self.var.options_menu_play
        self.screen_AI = None
        while self.status == self.var.options_menu_play:
            mouse = screen.click()
            if screen.x_in_rect(mouse, boxes[0][0]):
                self.status = self.var.options_play_HvH
                self.player_1 = Player(self.var, 1, False)
                self.player_2 = Player(self.var, 2, False)
            elif screen.x_in_rect(mouse, boxes[1][0]):
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
            elif screen.x_in_rect(mouse, boxes[2][0]):
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

    def draw_start_screen(self) -> None:
        """Show the start screen.
        For now it is only the play button but soon there will be more options"""

        start_screen = Screen(
            self.var,
            self.screen,
            self.gestures,
            cancel_box=False,
            volume=self.volume,
            camera=self.camera,
        )
        text_play = start_screen.create_text_rendered(self.var.text_options_play)
        text_options = start_screen.create_text_rendered(self.var.text_options_options)
        boxes_options = start_screen.center_all([[text_play], [text_options]])
        rect_play = boxes_options[0][0]
        rect_opti = boxes_options[1][0]
        self.status = self.var.options_menu_start
        while self.status == self.var.options_menu_start:
            mouse = start_screen.click()
            if start_screen.x_in_rect(mouse, rect_play):
                self.draw_play_options()
            elif start_screen.x_in_rect(mouse, rect_opti):
                self.draw_options_screen()
        if self.status == self.var.options_clicked_cancel:
            self.draw_start_screen()
