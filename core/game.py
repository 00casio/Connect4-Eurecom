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
from core.structure import Board
from core.utils import Box, Config, Symbol
from core.variables import Rect, Surface, Config
from extern.communication import Communication
from extern.gesture import GestureController

pg.init()


class Player:
    """The class that keep all the options for a player"""

    def __init__(
        self,
        conf: Config,
        number: int,
        AI: bool,
        level: int = 0,
        online: bool = False,
    ) -> None:
        """Initialize the values for the Players"""
        self.conf = conf
        # Associate the appropriate symbol and color for the player
        if number == 0:
            self.symbol = Symbol(self.conf.symbol_no_player)
            self.color = self.conf.color_trans
        elif number == 1:
            self.symbol = Symbol(self.conf.symbol_player_1)
            self.color = self.conf.color_player_1
        elif number == 2:
            self.symbol = Symbol(self.conf.symbol_player_2)
            self.color = self.conf.color_player_2
        else:
            raise ValueError("There can not be more than 2 players")
        if level is None:
            level = 0
        self.ai_depth = 3 * level + 1
        self.online = online
        self.ai_cpp: Optional[libai.Game] = None
        if AI:
            self.ai_cpp = libai.Game()

    def play(self, board: Board, screen: Screen, volume: bool) -> tuple[int, int, bool]:
        """The function used when it's the player's turn"""
        assert self.online == False, "Can not play when the player is not local"
        if self.ai_cpp is not None:
            # if the player is an AI, search the move
            col = self.ai_cpp.aiMove(self.ai_depth)
            click = (-1, -1) # Here to avoid error
        else:
            p = self.conf.padding
            box_allowed = Rect(p, p, self.conf.width_board, self.conf.height_board) # Where the user is allowed to click
            click = screen.click(
                box_allowed, print_disk=True, symbol_player=self.symbol
            )
            col = (click[0] - self.conf.padding) // self.conf.size_cell # Compute the col clicked
        cancel = screen.is_canceled(click)
        if cancel:
            return (-1, -1, True)

        row = board.find_free_slot(col)
        if row == -1:
            # If we clicked on a full column, we need to ask again for a cick
            if volume:
                playsound(self.conf.sound_error, block=False)
            col, row, cancel = self.play(board, screen, volume)
        return (col, row, cancel)

    def resetBoard(self) -> None:
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
        self.conf = Config(args)
        self.volume = self.conf.sound
        self.camera = self.conf.camera
        size_screen = (self.conf.width_screen, self.conf.height_screen)

        # Gestures
        self.gestures = GestureController()

        # Communication
        self.communication = Communication()

        # Players
        self.player_1 = Player(self.conf, 1, False, None)
        self.player_2 = Player(self.conf, 2, False, None)
        self.player_null = Player(self.conf, 0, False)
        self.player_playing = self.player_1

        # Pygame
        self.screen = pg.display.set_mode(size_screen, 0, 32)
        pg.display.set_caption(self.conf.screen_title)

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
                "How is that possible ? Read carefully the stack trace and send me everything"
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
        while True: # We never quit this loop
            # self.status give us what screen we should use
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
                self.player_1 = Player(self.conf, 1, False)
                self.player_2 = Player(self.conf, 2, False)
                self.status = self.allowed_status["gaming"]
            elif self.status == self.allowed_status["loc_HvAI"]:
                self.screen_AI = Screen_AI(
                    self.conf,
                    self.screen,
                    self.gestures,
                    volume=self.volume,
                    camera=self.camera,
                    number_AI=1,
                )
                self.player_1 = Player(self.conf, 1, False)
                self.player_2 = Player(self.conf, 2, True, self.screen_AI.diff_AI_1)
                if self.screen_AI.ready_play:
                    self.status = self.allowed_status["gaming"]
                else:
                    self.status = self.allowed_status["local"]
            elif self.status == self.allowed_status["loc_AIvAI"]:
                self.screen_AI = Screen_AI(
                    self.conf,
                    self.screen,
                    self.gestures,
                    volume=self.volume,
                    camera=self.camera,
                    number_AI=2,
                )
                self.player_1 = Player(self.conf, 1, True, self.screen_AI.diff_AI_1)
                self.player_2 = Player(self.conf, 2, True, self.screen_AI.diff_AI_2)
                if self.screen_AI.ready_play:
                    self.status = self.allowed_status["gaming"]
                else:
                    self.status = self.allowed_status["local"]
            elif self.status == self.allowed_status["online_client"]:
                code = self.select_opponent()
                if code == "103": # Connection refused
                    self.communication.sock.close()
                    self.communication = Communication()
                elif code == "102": # Connection accepted
                    self.status = self.allowed_status["gaming"]
                else:
                    print(f"Ask the other group why we received {code}")
            elif self.status == self.allowed_status["online_server"]:
                self.wait_as_server()

    def draw_start_screen(self) -> None:
        """Show the starting screen, choose between the different possinilities"""

        start_screen = Screen(
            self.conf,
            self.screen,
            self.gestures,
            cancel_box=False,
            volume=self.volume,
            camera=self.camera,
        )
        box_play_local = Box(self.conf.text_options_play_local, language=self.conf.language)
        box_play_online = Box(self.conf.text_options_play_online, language=self.conf.language)
        box_options = Box(self.conf.text_options_options, language=self.conf.language)
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
            self.conf, self, self.screen, self.gestures, self.volume, self.camera
        )
        while self.status == self.allowed_status["options"]:
            click = options.click()
            if options.is_canceled(click):
                self.status = self.allowed_status["start"]
            if options.x_in_rect(click, options.vol):
                self.volume = not self.volume # Inverse the volume option
                options.volume = self.volume
            elif options.x_in_rect(click, options.cam):
                self.camera = not self.camera # Inverse the camera option
                options.camera = self.camera
            # Change the language depending on where the click is
            elif options.x_in_rect(click, options.flags[0]):
                self.conf.change_language("en")
            elif options.x_in_rect(click, options.flags[1]):
                self.conf.change_language("fr")
            elif options.x_in_rect(click, options.flags[2]):
                self.conf.change_language("cat")
            elif options.x_in_rect(click, options.flags[3]):
                self.conf.change_language("wls")
            options.reset_options_screen()

    def draw_play_local_options(self) -> None:
        """Show the different options when choosing to play locally"""
        screen = Screen(self.conf, self.screen, self.gestures, self.volume, self.camera)
        box_HvH = Box(self.conf.text_options_play_HvH, language=self.conf.language)
        box_HvAI = Box(self.conf.text_options_play_HvAI, language=self.conf.language)
        box_AIvAI = Box(self.conf.text_options_play_AIvAI, language=self.conf.language)
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
        online = Screen(self.conf, self.screen, self.gestures, self.volume, self.camera)
        box_client = Box("Client", language=self.conf.language)
        box_server = Box("Server", language=self.conf.language)
        box_human = Box("Human", language=self.conf.language)
        box_machi = Box("As AI", language=self.conf.language)
        type_me = None
        player_me = None
        final_box = online.draw_agreement_box(self.conf.text_online_agreement_box)
        online.center_all([[box_client, box_server], [box_human, box_machi]])

        while self.status == self.allowed_status["online"]:
            mouse = online.click()
            box = None
            other_box = None
            # If the click is not in a box, we need to reset the screen
            out = True
            for b in online.all_boxes:
                if online.x_in_rect(mouse, b):
                    out = False
            if out:
                final_box.hide = True
                online.reset_screen(self.conf.color_options_screen)
                type_me = None
                player_me = None

            if online.is_canceled(mouse):
                self.status = self.allowed_status["start"]

            if online.x_in_rect(mouse, box_client):
                other_box = box_server
                box = box_client
                type_me = "client"
            elif online.x_in_rect(mouse, box_server):
                other_box = box_client
                box = box_server
                type_me = "server"
            if online.x_in_rect(mouse, box_human):
                other_box = box_machi
                box = box_human
                player_me = "human"
            elif online.x_in_rect(mouse, box_machi):
                other_box = box_human
                box = box_machi
                player_me = "ai"

            if box is not None:
                other_box.render(self.screen) # Reset the other box
                online.highlight_box( # Highlight the selected box
                    box,
                    self.conf.color_options_highlight_box,
                    online.screen,
                    self.conf.color_options_highlight_text,
                )

            if player_me is not None and type_me is not None:
                # If we selected both our mode and our type, print the confirmation box
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
        # Create the two player
        if type_me == "client":
            self.player_1 = Player(self.conf, 1, False, online=True)
            self.player_2 = Player(self.conf, 2, is_ai, 1)
            self.player_2.ai_depth = 16
        else:
            self.player_1 = Player(self.conf, 1, is_ai, 1)
            self.player_2.ai_depth = 16
            self.player_2 = Player(self.conf, 2, False, online=True)
        self.communication.type = type_me

        # Change the status depending on the type selected
        if type_me == "client":
            self.status = self.allowed_status["online_client"]
        else:
            self.status = self.allowed_status["online_server"]

    def select_opponent(self) -> str:
        """Select the opponent between all opponents available"""
        screen_opp = OpponentSelectionScreen(
            self.conf,
            self.screen,
            self.gestures,
            self.communication,
            self.volume,
            self.camera,
        )
        boxes = screen_opp.update_all_boxes()
        index = 0
        final_index = -1
        while final_index == -1:
            screen_opp.all_boxes = []
            screen_opp.screen.fill(self.conf.color_options_screen)
            screen_opp.draw_quit_box()
            mouse = screen_opp.click()
            # Go throught all boxes for the connections
            for i in range(len(boxes)):
                line = boxes[i]
                for j in range(len(line)):
                    b = line[j]
                    # to know if we clicked in it
                    if screen_opp.x_in_rect(mouse, b):
                        final_index = index
                    index += 1
            if final_index == -1: # If we clicked in no box,
                boxes = screen_opp.update_all_boxes() # update the boxes
                index = 0
        # By default we play as human, but if we selected ai, then we change the mode
        mode = "100"
        if not self.player_1.ai_cpp is None and self.player_2.ai_cpp is None:
            mode = "101"
        code = self.communication.connect(final_index, mode)
        return code

    def wait_as_server(self) -> None:
        screen = OpponentSelectionScreen(
            self.conf,
            self.screen,
            self.gestures,
            self.communication,
            self.volume,
            self.camera,
        )
        screen.write_message(
            ["Please wait, we are waiting for someone", "to connect to us."]
        )
        screen.draw_agreement_box(f"You are {gethostname()}", position=0.25, hide=False)
        code = "000"
        while code not in ["100", "101"]:
            # Wait for someone to really try to connect to us
            code = self.communication.wait_for_connection()

        # Reset the boxes present on the screen
        screen.all_boxes = []
        screen.screen.fill(self.conf.color_options_screen)
        screen.draw_cancel_box()
        screen.draw_quit_box()
        msg = Box(f"Looks like {self.communication.get_name_client()} want to play", language=self.conf.language)
        yes = Box("Accept", language=self.conf.language)
        nop = Box("Reject", language=self.conf.language)
        screen.center_all([[msg], [yes, nop]], update=False)
        screen.reset_screen(self.conf.color_options_screen)
        # Act according to the box selected
        force_reload = False
        while self.status == self.allowed_status["online_server"] and not force_reload:
            mouse = screen.click()
            if screen.x_in_rect(mouse, yes):
                self.communication.send("102")
                self.status = self.allowed_status["gaming"]
            elif screen.x_in_rect(mouse, nop):
                self.communication.send("103")
                self.communication.sock.close()
                self.communication = Communication("server")
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
            self.conf,
            self.screen,
            self.gestures,
            self.volume,
            self.camera,
            self.conf.language,
        )
        if self.player_1.online or self.player_2.online:
            gaming.comm = self.communication # Used when quitting the game
        gaming.draw_board()
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size and self.status == self.allowed_status["gaming"]
        ): # Until we have a draw, a winner, or a cancel, play
            if self.player_playing.online:
                cancel = False
                col = int(self.communication.receive())
                if col == 201: # If the code was the one to abort the game
                    cancel = True
                    row = -1
                else:
                    row = self.board.find_free_slot(col)
            else:
                # If the player is local, wait for a valid click
                col, row, cancel = self.player_playing.play(self.board, gaming, self.volume)

                # for opponent
                if self.opponent.online:
                    msg = "201" if cancel else f"00{col}"
                    self.communication.send(msg)
            if self.opponent.ai_cpp is not None:
                # If the opponent is an ai, then make the same move
                self.opponent.ai_cpp.humanMove(col)

            if cancel:
                # If the game was canceled, go to the appropriate screen
                self.status = self.allowed_status["local"]
                if self.opponent.online or self.player_playing.online:
                    self.communication.sock.close()
                    self.communication = Communication()
                    self.status = self.allowed_status["online"]
            for event in gaming.get_event():
                # This is for when we clicked when the other player (ai or online) played
                if event.type == pg.MOUSEBUTTONUP:
                    gaming.handle_quit(gaming.get_mouse_pos())
                    if gaming.is_canceled(gaming.get_mouse_pos()):
                        self.status = self.allowed_status["local"]

            if self.status == self.allowed_status["gaming"]:
                self.board[row, col] = self.player_playing.symbol.v
                # Maybe multithread this animation ?
                gaming.animate_fall(col, row, self.player_playing.symbol)
                self.inverse_players()
                self.num_turn += 1
        # if status was gaming and we are out of the loop, then the game was not aborted
        if self.status == self.allowed_status["gaming"]:
            self.winning_surface = gaming.board_surface
            self.status = self.allowed_status["winning"]

    def draw_winner(self) -> None:
        """Draw the winner on the screen, with the line that made it win"""

        # Change the message and sound according to the options
        winner = self.who_is_winner()
        sound = self.conf.sound_winner_victory
        text = f"Player {winner.symbol.v} won !"
        if self.conf.language == "fr":
            text = f"Le joueur {winner.symbol.v} a gagné !"
        elif self.conf.language == "cat":
            text = f"Nyah ! {winner.symbol.v} nyah !"
        elif self.conf.language == "wls":
            text = f"Chwaraewr {winner.symbol.v} yn ennill"
        elif self.conf.language == "fra":
            sound = self.conf.sound_franz_win
        if winner != self.player_1 and winner != self.player_2:
            text = self.conf.text_draw[self.conf.language]
            sound = self.conf.sound_winner_draw
        if (winner == self.player_1 and self.player_1.online) or (winner == self.player_2 and self.player_2.online):
            sound = self.conf.sound_winner_defeat
            if self.conf.language == "fra":
                sound = self.conf.sound_franz_lose
            text = "You lose"
        print(text)

        End = Screen(
            self.conf,
            self.screen,
            self.gestures,
            volume=self.volume,
            camera=self.camera,
        )
        End.screen.fill(self.conf.color_screen)
        End.cancel_box.text = self.conf.text_retry
        End.cancel_box.render(End.screen)
        End.draw_quit_box()

        p = self.conf.padding
        box_winner = Box(
            text,
            color_text=self.conf.black,
            color_rect=self.conf.white,
            coordinate=(self.conf.width_screen // 2, p // 2),
            align=(0, 0),
            language=self.conf.language
        )
        box_winner.font_size = 64
        box_winner.render(self.screen)

        if self.volume:
            playsound(sound, block=False)
        self.screen.blit(self.winning_surface, (p, p))
        bits = int(self.board.state_to_bits(), 2)

        def complete(bits: int, direction: int) -> None:
            """ Fucntion to check in a direction if there was a winner and draw a line where the winner won """
            d = {0: 7, 1: 1, 2: 6, 3: 8}
            m = bits & (bits >> d[direction])
            m2 = m & (m >> 2 * d[direction])
            if m2:
                bs = bin(m2)[2:]
                i = 48 - ("0" * (49 - len(bs)) + bs).find("1")
                p = self.conf.padding
                c = self.conf.size_cell
                x_s = p + (i // 7) * c + c // 2
                y_s = self.conf.height_board - (i % 7 - 1) * c
                x_e = x_s
                y_e = y_s
                if direction in [0, 2, 3]:
                    x_e += 3 * c
                if direction in [1, 3]:
                    y_e -= 3 * c
                if direction == 2:
                    y_e += 3 * c
                pg.draw.line(self.screen, self.conf.black, (x_s, y_s), (x_e, y_e), 15)

        complete(bits, 0)  # Horizontal check
        complete(bits, 1)  # Vert
        complete(bits, 2)  # \
        complete(bits, 3)  # /

        End.get_event() # Remove all clicks that happened during the game
        pg.display.update()
        mouse = End.click()
        if End.is_canceled(mouse):
            self.status = self.allowed_status["gaming"]
        else:
            if self.opponent.online or self.player_playing.online:
                self.communication.sock.close()
            self.status = self.allowed_status["start"] # Go back to the main menu after a game ended
