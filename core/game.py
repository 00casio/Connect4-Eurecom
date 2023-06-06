#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Any, Iterator, Optional, Union
from socket import gethostname

import numpy as np
import pygame as pg
from playsound import playsound

import ai.libai as libai
from core.screens import (
    GamingScreen,
    OpponentSelectionScreen,
    OptionsScreen,
    Screen,
    Screen_AI,
)
from core.structure import Board, Node
from core.utils import Box, Config, Symbol
from core.variables import Rect, Surface, Variables
from extern.communication import Communication
from extern.gesture import GestureController

pg.init()


class Player:
    """The class that keep all the options for a player"""

    def __init__(
        self,
        var: Variables,
        number: int,
        AI: bool,
        difficulty: int = -1,
        online: bool = False,
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
        self.ai_difficulty = difficulty
        self.online = online
        self.ai_cpp: Optional[libai.Game] = None
        if AI:
            self.ai_cpp = libai.Game()

    def play(self, board: Board, screen: Screen, volume: bool) -> tuple[int, int, bool]:
        """The function used when it's the player's turn"""
        assert self.online == False, "Can not play when the player is not local"
        if self.ai_cpp is not None:
            col = self.ai_cpp.aiMove(3 * self.ai_difficulty + 1)
            click = (0, 0)
        else:
            p = self.var.padding
            box_allowed = Rect(p, p, self.var.width_board, self.var.height_board)
            click = screen.click(
                box_allowed, print_disk=True, symbol_player=self.symbol
            )
            col = (click[0] - self.var.padding) // self.var.size_cell
        cancel = screen.is_canceled(click)
        if cancel:
            return (0, 0, True)

        row = board.find_free_slot(col)
        if row == -1:
            if volume:
                playsound(self.var.sound_error, block=False)
            col, row, cancel = self.play(board, screen, volume, ai_cpp)
        return (col, row, cancel)

    def resetBoard(self):
        if self.ai_cpp is not None:
            self.ai_cpp.resetBoard()

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

    def __init__(self, args: Namespace) -> None:
        """Initialize the value needed for the game"""
        self.allowed_status = {
            "gaming": -1,
            "winning": -10,
            "start": 0,
            "options": 1,
            "local": 2,
            "online": 3,
            "loc_HvH": 4,
            "loc_HvAI": 5,
            "loc_AIvAI": 6,
            "online_options": 7,
            "online_client": 8,
            "online_server": 9,
        }
        self.status = self.allowed_status["start"]
        self.winning_surface = None

        # Players
        self.var = Variables()
        self.conf = Config(self.var, args)
        self.volume = self.var.sound
        self.camera = self.var.camera
        size_screen = (self.var.width_screen, self.var.height_screen)

        # Gestures
        self.gestures = GestureController()

        # Communication
        self.communication = Communication()

        # Players
        self.player_1 = Player(self.var, 1, False, None)
        self.player_2 = Player(self.var, 2, False, None)
        self.player_null = Player(self.var, 0, False)
        self.player_playing = self.player_1

        # Pygame
        self.screen = pg.display.set_mode(size_screen, 0, 32)
        pg.display.set_caption(self.var.screen_title)

    def inverse_players(self) -> None:
        """Return the symbols of the opponent of the player currently playing"""
        if self.player_playing == self.player_1:
            self.player_playing = self.player_2
            self.opponent = self.player_1
        elif self.player_playing == self.player_2:
            self.player_playing = self.player_1
            self.opponent = self.player_2
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
        while True:
            if self.status == self.allowed_status["start"]:
                self.draw_start_screen()
            elif self.status == self.allowed_status["gaming"]:
                self.board = Board()
                self.CLOCK = pg.time.Clock()
                self.num_turn = 0
                self.start_game()
            elif self.status == self.allowed_status["winning"]:
                self.draw_winner()
            elif self.status == self.allowed_status["local"]:
                self.draw_play_local_options()
            elif self.status == self.allowed_status["online"]:
                self.draw_play_online_options()
            elif self.status == self.allowed_status["options"]:
                self.draw_options_screen()
            elif self.status == self.allowed_status["loc_HvH"]:
                self.player_1 = Player(self.var, 1, False)
                self.player_2 = Player(self.var, 2, False)
                self.status = self.allowed_status["gaming"]
            elif self.status == self.allowed_status["loc_HvAI"]:
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
                if self.screen_AI.ready_play:
                    self.status = self.allowed_status["gaming"]
                else:
                    self.status = self.allowed_status["local"]
            elif self.status == self.allowed_status["loc_AIvAI"]:
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
                if self.screen_AI.ready_play:
                    self.status = self.allowed_status["gaming"]
                else:
                    self.status = self.allowed_status["local"]
            elif self.status == self.allowed_status["online_client"]:
                code = self.select_opponent()
                if code == "103":
                    self.communication.sock.close()
                    self.communication = Communication()
                elif code == "102":
                    self.status = self.allowed_status["gaming"]
                else:
                    print(f"Ask the other group why we received {code}")
            elif self.status == self.allowed_status["online_server"]:
                self.wait_as_server()

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
        box_play_local = Box(self.var.text_options_play_local)
        box_play_online = Box(self.var.text_options_play_online)
        box_options = Box(self.var.text_options_options)
        start_screen.center_all([[box_play_local], [box_play_online], [box_options]])

        while self.status == self.allowed_status["start"]:
            mouse = start_screen.click()
            if start_screen.x_in_rect(mouse, box_play_local):
                self.status = self.allowed_status["local"]
            if start_screen.x_in_rect(mouse, box_play_online):
                self.status = self.allowed_status["online"]
            elif start_screen.x_in_rect(mouse, box_options):
                self.status = self.allowed_status["options"]

    def draw_options_screen(self) -> None:
        """Draw the options screen (language, if camera, if sound, etc.)"""
        options = OptionsScreen(
            self.var, self, self.screen, self.gestures, self.volume, self.camera
        )
        while self.status == self.allowed_status["options"]:
            click = options.click()
            if options.is_canceled(click):
                self.status = self.allowed_status["start"]
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

    def draw_play_local_options(self) -> None:
        """Show the different options when choosing to play locally"""
        screen = Screen(self.var, self.screen, self.gestures, self.volume, self.camera)
        box_HvH = Box(self.var.text_options_play_HvH)
        box_HvAI = Box(self.var.text_options_play_HvAI)
        box_AIvAI = Box(self.var.text_options_play_AIvAI)
        screen.center_all([[box_HvH], [box_HvAI], [box_AIvAI]])

        self.screen_AI = None
        while self.status == self.allowed_status["local"]:
            mouse = screen.click()
            if screen.x_in_rect(mouse, box_HvH):
                self.status = self.allowed_status["loc_HvH"]
            elif screen.x_in_rect(mouse, box_HvAI):
                self.status = self.allowed_status["loc_HvAI"]
            elif screen.x_in_rect(mouse, box_AIvAI):
                self.status = self.allowed_status["loc_AIvAI"]
            if screen.x_in_rect(mouse, screen.cancel_box):
                self.status = self.allowed_status["start"]

    def draw_play_online_options(self) -> None:
        online = Screen(self.var, self.screen, self.gestures, self.volume, self.camera)
        box_client = Box("Client")
        box_server = Box("Server")
        box_human = Box("Human")
        box_machi = Box("As AI")
        type_me = None
        player_me = None
        final_box = online.draw_agreement_box("J'accepte")
        online.center_all([[box_client, box_server], [box_human, box_machi]])

        while self.status == self.allowed_status["online"]:
            mouse = online.click()
            box = None
            out = True
            for b in online.all_boxes:
                if online.x_in_rect(mouse, b):
                    out = False
            if out:
                final_box.hide = True
                online.reset_screen(self.var.color_options_screen)
                type_me = None
                player_me = None
            
            if online.is_canceled(mouse):
                self.status = self.allowed_status["start"]

            if online.x_in_rect(mouse, box_client):
                box_server.render(self.screen)
                box = box_client
                type_me = "client"
            elif online.x_in_rect(mouse, box_server):
                box_client.render(self.screen)
                box = box_server
                type_me = "server"
            if online.x_in_rect(mouse, box_human):
                box_machi.render(self.screen)
                box = box_human
                player_me = "human"
            elif online.x_in_rect(mouse, box_machi):
                box_human.render(self.screen)
                box = box_machi
                player_me = "ai"

            if box is not None:
                online.highlight_box(
                    box,
                    self.var.color_options_highlight_box,
                    online.screen,
                    self.var.color_options_highlight_text,
                )

            if player_me is not None and type_me is not None:
                final_box.hide = False
                final_box.render(self.screen)
                pg.display.update()
            if online.x_in_rect(mouse, final_box):
                self.status = self.allowed_status["online_client"]

        if online.is_canceled(mouse):
            self.status = self.allowed_status["start"]
            return

        is_ai = player_me == "ai"
        print("We need to allow the change of the difficulty")
        if type_me == "client":
            self.player_1 = Player(self.var, 1, False, online=True)
            self.player_2 = Player(self.var, 2, is_ai, 10)
        else:
            self.player_1 = Player(self.var, 1, is_ai, 10)
            self.player_2 = Player(self.var, 2, False, online=True)
        self.communication.type = type_me

        if type_me == "client":
            self.status = self.allowed_status["online_client"]
        else:
            self.status = self.allowed_status["online_server"]

    def select_opponent(self) -> str:
        """Select the opponent between all opponents available"""
        screen_opp = OpponentSelectionScreen(
            self.var,
            self.screen,
            self.gestures,
            self.communication,
            self.volume,
            self.camera,
        )
        screen_opp.write_message(
            [
                "Please wait a few seconds",
                "We are getting a list of all potential opponents",
            ]
        )
        boxes = screen_opp.update_all_boxes()
        index = 0
        final_index = -1
        while final_index == -1:
            screen_opp.all_boxes = []
            screen_opp.screen.fill(self.var.color_options_screen)
            screen_opp.draw_quit_box()
            mouse = screen_opp.click()
            for i in range(len(boxes)):
                line = boxes[i]
                for j in range(len(line)):
                    b = line[j]
                    if screen_opp.x_in_rect(mouse, b):
                        final_index = index
                    index += 1
            if final_index == -1:
                boxes = screen_opp.update_all_boxes()
                index = 0
        mode = "100"
        if not self.player_1.ai_cpp is None and self.player_2.ai_cpp is None:
            mode = "101"
        code = self.communication.connect(final_index, mode)
        return code

    def wait_as_server(self) -> None:
        screen = OpponentSelectionScreen(
            self.var,
            self.screen,
            self.gestures,
            self.communication,
            self.volume,
            self.camera,
        )
        screen.write_message(
            ["Please wait, we are waiting for someone", "to connect to us."]
        )
        screen.draw_agreement_box(f"You are {gethostname()}", position=0.20, hide=False)
        self.communication.wait_for_connection()
        print(dir(self.communication.sock))

        screen.all_boxes = []
        screen.screen.fill(self.var.color_options_screen)
        screen.draw_cancel_box()
        screen.draw_quit_box()
        msg = Box(f"Looks like {self.communication.sock.getpeername()} want to play")
        yes = Box("Accept")
        nop = Box("Reject")
        screen.center_all([[msg], [yes, nop]], update=False)
        screen.reset_screen(self.var.color_options_screen)
        force_reload = False
        while self.status == self.allowed_status["online_server"] and not force_reload:
            mouse = screen.click()
            if screen.x_in_rect(mouse, yes):
                self.communication.send("102")
                self.status = self.allowed_status["gaming"]
            elif screen.x_in_rect(mouse, nop):
                self.communication.send("103")
                self.communication.sock.close()
                self.communication = Communication()
                self.communication.type = "server"
                force_reload = True
            elif screen.is_canceled(mouse):
                self.status = self.allowed_status["online"]

    def start_game(self) -> None:
        """Start the game"""
        self.player_playing = self.player_1
        self.opponent = self.player_2
        self.player_1.resetBoard()
        self.player_2.resetBoard()
        gaming = GamingScreen(
            self.var,
            self.screen,
            self.gestures,
            self.volume,
            self.camera,
            self.conf.language,
        )
        if self.player_1.online or self.player_2.online:
            gaming.comm = self.communication # Used when quitting the game
        gaming.draw_board()
        gaming.draw_token(
            self.var.width_screen // 2,
            self.var.padding // 2,
            self.player_playing.symbol,
            self.var.radius_disk,
            col_row=False,
            screen=gaming.screen,
        )
        pg.display.update()
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size and self.status == self.allowed_status["gaming"]
        ):
            if self.player_playing.online:
                cancel = False
                col = int(self.communication.receive())
                if col == 201:
                    cancel = True
                row = self.board.find_free_slot(col)
            else:
                col, row, cancel = self.player_playing.play(self.board, gaming, self.volume)

                # for opponent
                if self.opponent.online:
                    if cancel:
                        self.communication.send("201")
                    else:
                        self.communication.send(f"00{col}")
            if self.opponent.ai_cpp is not None:
                self.opponent.ai_cpp.humanMove(col)

            if cancel:
                self.status = self.allowed_status["local"]
                if self.opponent.online or self.player_playing.online:
                    self.status = self.allowed_status["online"]
            for event in gaming.get_event():
                if event.type == pg.MOUSEBUTTONUP:
                    gaming.handle_quit(gaming.get_mouse_pos())
                    if gaming.is_canceled(gaming.get_mouse_pos()):
                        self.status = self.allowed_status["local"]
            
            if self.status == self.allowed_status["gaming"]:
                gaming.animate_fall(col, row, self.player_playing.symbol)
                self.board[row, col] = self.player_playing.symbol.v
                self.inverse_players()
                self.num_turn += 1
        if self.status == self.allowed_status["gaming"]:
            self.winning_surface = gaming.board_surface
            self.status = self.allowed_status["winning"]

    def draw_winner(self) -> None:
        """Draw the winner on the screen, with the line that made it win"""
        winner = self.who_is_winner()
        text = f"Player {winner.symbol.v} won !"
        if self.conf.language == "fr":
            text = f"Le joueur {winner.symbol.v} a gagné !"
        elif self.conf.language == "cat":
            text = f"Nyah ! {winner.symbol.v} nyah !"
        sound = self.var.sound_winner_victory
        End = Screen(
            self.var,
            self.screen,
            self.gestures,
            volume=self.volume,
            camera=self.camera,
            cancel_box=False,
        )
        End.screen.fill(self.var.color_screen)
        End.draw_quit_box()
        if winner != self.player_1 and winner != self.player_2:
            text = self.var.text_draw[self.conf.language]
            sound = self.var.sound_winner_draw
        print(text)

        p = self.var.padding
        box_winner = Box(
            text,
            color_text=self.var.black,
            color_rect=self.var.white,
            coordinate=(self.var.width_screen // 2, p // 2),
            align=(0, 0),
        )
        box_winner.font_size = 64
        box_winner.render(self.screen)

        if self.volume:
            playsound(sound, block=False)
        self.screen.blit(self.winning_surface, (p, p))
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

        End.get_event() # Remove all clicks that happened during the game
        pg.display.update()
        End.click()
        if self.opponent.online or self.player_playing.online:
            self.communication.sock.close()
        self.status = self.allowed_status["start"]
