#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import time
from typing import Any, Callable, Iterator, Optional, Union
from random import choice as random_choice
from os import listdir

import cv2
import numpy as np
import pygame as pg
from playsound import playsound

from core.utils import Box, Tools, Symbol
from core.variables import Color, Rect, Surface, Variables
from extern.communication import Communication
from extern.gesture import *


class Screen(Tools):
    """A screen is composed of what is shown to the user"""

    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
        cancel_box: bool = True,
        quit_box: bool = True,
        color_fill: Color = Variables().color_options_screen,
        language: str = "en"
    ) -> None:
        """Initialize the values"""
        Tools.__init__(self, var, screen, volume, camera)
        self.gestures = gesture
        self.cancel_box: Optional[Box] = None
        self.quit_box: Optional[Box] = None
        self.box_clicked = self.var.box_out
        self.screen.fill(color_fill)
        self.last_x = 0
        self.last_y = 0
        self.draw_cancel = cancel_box
        self.draw_quit = quit_box
        self.last_column_selected = 3
        self.last_box_hovered = None
        self.language = language
        if cancel_box:
            self.draw_cancel_box()
        if quit_box:
            self.draw_quit_box()

    def draw_cancel_box(self, force_reload: bool=False) -> None:
        """Draw the box that allow the user to take a step back"""
        if self.cancel_box is None or force_reload:
            self.cancel_box = Box(
                self.var.text_cancel_box,
                self.var.black,
                self.var.white,
                coordinate=self.var.coor_cancel_box,
                align=(-1, 1),
            )
        self.cancel_box.render(self.screen)
        if self.cancel_box not in self.all_boxes:
            self.all_boxes.append(self.cancel_box)

    def draw_quit_box(self, force_reload: bool=False) -> None:
        """Draw the box that allow the user to take a step back"""
        if self.quit_box is None or force_reload:
            self.quit_box = Box(
                self.var.text_quit_box,
                self.var.black,
                self.var.white,
                coordinate=self.var.coor_quit_box,
                align=(1, 1),
            )
        self.quit_box.render(self.screen)
        if self.quit_box not in self.all_boxes:
            self.all_boxes.append(self.quit_box)

    def reset_screen(self, color_screen: Color, boxes: list[Box]) -> None:
        """Reset the screen to a "blank" state"""
        self.screen.fill(color_screen)
        for b in self.all_boxes:
            b.render(self.screen)
        pg.display.update()

    def draw_circle(self, x: int, y: int, color: Color, r: int, screen: Surface) -> None:
        """ Draw a circle of the color at the coordinate """
        pg.draw.circle(screen, color, (x, y), r)

    def draw_token(self, n: int, m: int, symbol: Optional[Symbol], r: int, col_row: bool=True, screen: Surface=None) -> None:
        """Draw a circle in the corresponding column, and row
        If col_row is true, then n and m are column and row number, if they are not, then n and m are a position"""
        if screen is None:
            screen = self.board_surface
        sc = self.var.size_cell
        if col_row:
            x = n * sc + sc // 2
            y = m * sc + sc // 2
        else:
            x = n
            y = m
        if symbol is None:
            self.draw_circle(x, y, self.var.color_trans, r, screen)
        else:
            if symbol == self.var.symbol_player_1:
                r = self.var.radius_disk
                if self.language == "cat":
                    disk = pg.image.load("assets/cat/tails.png")
                    disk = pg.transform.scale(disk, (r*2, r*2))
                    screen.blit(disk, (x - r, y - r))
                else:
                    color = self.var.color_player_1
                    self.draw_circle(x, y, color, r, screen)
            elif symbol == self.var.symbol_player_2:
                color = self.var.color_player_2
                self.draw_circle(x, y, color, r, screen)
            else:
                raise ValueError("How did that happen ?")

    def hovering_box(self, box: Box, hover=True):
        if box is None:
            return
        color = box.color_rect
        if hover == True:
            color = box.color_hover
        pg.draw.rect(self.screen, color, box.box, 5)
        pg.display.update(box.box)

    def get_mouse_pos(self, force_mouse: bool = False) -> tuple[int, int]:
        """Return the mouse position"""
        # print("Change this to have the position from the camera")
        return pg.mouse.get_pos()

    def human_move(self, player: Symbol) -> None:
        """Function to use when it's the human's turn to move"""
        # self.screen.fill(self.var.color_screen)
        p = self.var.padding
        sc = self.var.size_cell
        last = self.last_column_selected

        mouse_x, mouse_y = self.get_mouse_pos()
        if mouse_x < self.var.pos_min_x:
            mouse_x = self.var.pos_min_x
        elif mouse_x > self.var.pos_max_x:
            mouse_x = self.var.pos_max_x

        if p > mouse_x or mouse_x > p + self.var.width_board:
            return

        new_col = (mouse_x - p) // sc
        self.last_column_selected = new_col
        old_rect = (p + last * sc, 0, sc, p)
        new_rect = (p + new_col * sc, 0, sc, p)
        self.draw_quit_box()
        pg.draw.rect(self.screen, self.var.color_screen, old_rect)
        pg.draw.rect(self.screen, self.var.color_highlight_column, new_rect)
        self.draw_token(p + new_col * sc + sc //2, p // 2, player, self.var.radius_disk, col_row=False, screen=self.screen)
        pg.display.update(old_rect)
        pg.display.update(new_rect)

    def update_gesture(self, image: np.ndarray[Any, np.dtype[Any]]) -> None:
        """Update the gesture class"""
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.gestures.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            self.gestures.classify_hands(results)
            self.gestures.handmajor.update_hand_result(self.gestures.hr_major)
            self.gestures.handminor.update_hand_result(self.gestures.hr_minor)

            self.gestures.handmajor.set_finger_state()
            self.gestures.handminor.set_finger_state()
            gest_name = self.gestures.handminor.get_gesture()

            if gest_name == Gest.PINCH_MINOR:
                self.gestures.handle_controls(
                    gest_name, self.gestures.handminor.hand_result
                )
            else:
                gest_name = self.gestures.handmajor.get_gesture()
                self.gestures.handle_controls(
                    gest_name, self.gestures.handmajor.hand_result
                )

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        else:
            self.prev_hand = None
        cv2.imshow("Gesture Controller", image)
        if cv2.waitKey(5) & 0xFF == 13:
            self.handle_quit(self.quit_box.center)

    def click(
        self,
        rect_play: Optional[Rect] = None,
        sound: str = Variables().sound_click_box,
        print_disk: bool = False,
        symbol_player: Symbol = Symbol(None),
        func: Callable = None,
        **args,
    ) -> tuple[int, int]:
        """Quit the function only when there is a click. Return the position of the click.
        If f is not None, then the function is called whith the argument 'event' at every iteration"""
        allow_quit = False
        while not allow_quit:
            # (suppose and) Use the camera if usable
            success = True
            if self.camera:
                success, image = self.gestures.cap.read()
                if success:
                    self.update_gesture(image)
                else:
                    print("Could not use the camera, disregarding this frame")

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    allow_quit = True
                if func is not None:
                    func(**args)

            # Actions independant of the usage of the camera
            if print_disk:
                self.human_move(symbol_player)
            # We force the usage of the mouse if there was an error
            mouse = self.get_mouse_pos()

            # Draw a rectangle in the selected box
            nearest_box = None
            for box in self.all_boxes:
                if box.hide:
                    continue
                if self.x_in_rect(mouse, box, sound=""):
                    nearest_box = box
            if self.last_box_hovered is not nearest_box:
                self.hovering_box(self.last_box_hovered, hover=False)
                self.hovering_box(nearest_box, hover=True)
                self.last_box_hovered = nearest_box

        # When a click is made we are here
        click = self.get_mouse_pos()
        if self.is_canceled(click):
            self.box_clicked = self.var.boxAI_cancel
        self.handle_quit(click)
        if rect_play is not None:
            while not self.x_in_rect(click, rect_play, ""):
                click = self.click(rect_play, sound, print_disk, symbol_player)
        return click

    def is_canceled(self, click: tuple[int, int]) -> bool:
        """Return if the cancel button was pressed"""
        if self.cancel_box is None:
            return False
        return self.x_in_rect(click, self.cancel_box)

    def handle_quit(self, click: tuple[int, int]) -> None:
        """Function to call when wanting to see if user clicked in the quitting box"""
        if self.quit_box is not None and self.x_in_rect(click, self.quit_box):
            print(self.var.message_quit)
            pg.quit()
            sys.exit()

    def x_in_rect(
        self,
        coor: tuple[int, int],
        rect: Optional[Union[Rect, Box]],
        sound: str = Variables().sound_click_box,
    ) -> bool:
        """Return whether coor is in the rectangle 'rect'"""
        if rect is None:
            return False
        if isinstance(rect, Box):
            rect = rect.box
        status = (
            rect.left <= coor[0] <= rect.right and rect.top <= coor[1] <= rect.bottom
        )
        if status and sound != "" and self.volume:
            playsound(sound, block=False)
        return status

    def handle_click(
        self, click_coor: tuple[int, int], list_rect: list[Union[Rect, Box]]
    ) -> int:
        """Return the index of the box the click was in"""
        for i in range(len(list_rect)):
            if self.x_in_rect(click_coor, list_rect[i], ""):
                return i
        return -1


class Screen_AI(Screen):
    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
        number_AI: int = 1,
    ) -> None:
        Screen.__init__(self, var, screen, gesture, volume, camera)
        self.number_AI = number_AI
        self.begin = 1

        # Creation of all boxes with message in them
        self.boxes_options = [[Box(self.var.text_difficulty_options[number_AI], color_hovering=self.var.color_options_box)]]
        boxes_ai_1 = []
        for i in range(len(self.var.boxAI_text_levels)):
            boxes_ai_1.append(
                Box(f"Level {i}", self.var.black, self.var.color_player_1, self.var.color_hover_player_1)
            )
        boxes_ai_2 = []
        for i in range(len(self.var.boxAI_text_levels)):
            boxes_ai_2.append(
                Box(f"Level {i}", self.var.black, self.var.color_player_2, self.var.color_hover_player_2)
            )
        self.boxes_options.append(boxes_ai_1)

        # self.options_levels is used to know in which the user clicked
        if self.number_AI == 2:
            self.boxes_options.append(boxes_ai_2)
            self.options_levels = [*boxes_ai_1, *boxes_ai_2]
        else:
            self.options_levels = [*boxes_ai_1]

        self.play_box = self.draw_agreement_box(self.var.text_confirmation)
        self.diff_AI_1, self.diff_AI_2 = -1, -1
        self.nbr_levels_AI_1 = len(self.boxes_options[1])
        self.center_all(self.boxes_options)
        self.screen_loop()

    def screen_loop(self) -> None:
        """Select the possibble value for the AI (if AI, AI(s) level)"""
        while self.box_clicked not in [self.var.boxAI_play, self.var.boxAI_cancel]:
            mouse_click = self.click()
            index_box = self.handle_click(mouse_click, self.options_levels)
            if index_box != -1:
                if 0 <= index_box < self.nbr_levels_AI_1:
                    # We redraw all boxes on the line (remove highlight)
                    for b in self.options_levels[: self.nbr_levels_AI_1]:
                        b.render(self.screen)
                    self.diff_AI_1 = index_box
                elif self.nbr_levels_AI_1 <= index_box < len(self.options_levels):
                    # Same here
                    for b in self.options_levels[self.nbr_levels_AI_1 :]:
                        b.render(self.screen)
                    self.diff_AI_2 = index_box % self.nbr_levels_AI_1

                if self.diff_AI_1 != -1 and (
                    self.diff_AI_2 != -1 or self.number_AI == 1
                ):
                    self.play_box.hide = False
                    self.play_box.render(self.screen)
                self.highlight_box(
                    self.options_levels[index_box],
                    self.var.color_options_highlight_box,
                    self.screen,
                    self.var.color_options_highlight_text,
                )
            elif not self.play_box.hide and self.x_in_rect(
                mouse_click, self.play_box
            ):
                self.box_clicked = self.var.boxAI_play
            else:
                self.play_box.hide = True
                self.diff_AI_1 = -1
                self.diff_AI_2 = -1
                self.reset_screen(self.var.color_options_screen, self.boxes_options)


class OpponentSelectionScreen(Screen):
    """Not completed, will allow the user to chose it's oppponent"""

    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        comm: Communication,
        volume: bool,
        camera: bool,
    ) -> None:
        Screen.__init__(self, var, screen, gesture, volume, camera)
        self.opp = None
        self.poss = []
        self.rect_boxes = []
        self.comm = comm
        self.time_update = 5
        self.last_update = 0

    def update(self) -> None:
        """Update the screen with the raspberry pi we can connect to"""
        if (time() - self.last_update) < self.time_update:
            return
        self.poss = self.comm.receive()
        i = 0
        list_poss_player = []
        while i < len(poss):
            p_1 = self.create_text_rendered(poss[i])
            p_2 = self.create_text_rendered(poss[i + 1])
            list_poss_player.append([p_1, p_2])
            i += 2
        self.rect_boxes = self.center_all(list_poss_player)

    def select(self):
        """Select a raspberry pi as the opponent"""
        while self.opp is None and self.box_clicked != self.var.boxAI_cancel:
            mouse = self.click(func=self.update)
            for i in range(len(self.rect_boxes)):
                if self.x_in_rect(mouse, self.rect_boxes[i][0]):
                    self.opp = self.poss[2 * i]
                    break
                elif self.x_in_rect(mouse, self.rect_boxes[i][1]):
                    self.opp = self.poss[2 * i + 1]
                    break
        if self.opp is not None:
            self.comm.send(self.opp)


"""
Options to do:
Language (Cymraeg, Arabic)
Logging?
"""


class OptionsScreen(Screen):
    def __init__(
        self,
        var: Variables,
        game,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
    ) -> None:
        Screen.__init__(self, var, screen, gesture, volume, camera)
        self.size = (self.var.width_screen // 10, self.var.height_screen // 10)
        self.nbr_line = 2
        self.vol, self.cam = self.draw_vol_cam()
        self.flags = list(self.draw_language())
        pg.display.update()

    def reset_options_screen(self) -> None:
        """Reset the appearance of the option screen to the default"""
        self.all_boxes = []
        self.screen.fill(self.var.color_options_screen)
        if self.draw_cancel:
            self.draw_cancel_box(force_reload=True)
        if self.draw_quit:
            self.draw_quit_box(force_reload=True)
        self.vol, self.cam = self.draw_vol_cam()
        self.flags = list(self.draw_language())
        pg.display.update()

    def dfites(
        self,
        testing: bool,
        position: tuple[int, int],
        first_image: str,
        second_image: str,
    ) -> Rect:
        """Draw First Image (if) True Else Second (image)"""
        if testing:
            box = self.draw_icon(first_image, self.size, position)
        else:
            box = self.draw_icon(second_image, self.size, position)
        return box

    def draw_vol_cam(self) -> tuple[Rect, Rect]:
        """Draw the icon for the volume and the camera"""
        cs = self.var.center_screen
        sp = self.var.options_spacing
        x_now = cs[0] - self.size[0] - sp
        y = cs[1] - self.size[1] // 2 - 3 * sp // 2
        vol = self.dfites(
            self.volume,
            (x_now, y),
            self.var.image_volume_on,
            self.var.image_volume_muted,
        )
        x_now += sp + self.size[0] + 2 * self.var.text_box_spacing
        cam = self.dfites(
            self.camera, (x_now, y), self.var.image_camera, self.var.image_nocamera
        )
        return vol, cam

    def draw_language(self) -> Iterator[Rect]:
        """Draw the languages"""
        cs = self.var.center_screen
        sp = self.var.options_spacing
        y_now = cs[1] + 3 * sp // 2
        l = [self.var.image_english, self.var.image_french, self.var.image_cat]
        x_now = cs[0] - len(l) * self.size[0] // 2 - (len(l) - 1) * sp
        for lan in l:
            yield self.draw_icon(lan, self.size, (x_now, y_now))
            x_now += sp + self.size[0] + 2 * self.var.text_box_spacing


class GamingScreen(Screen):
    """The gaming screen is used for the gaming part of the program"""

    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
        language: str,
    ) -> None:
        Screen.__init__(self, var, screen, gesture, volume, camera, language=language)
        self.color_screen = self.var.white
        self.color_board = self.var.blue
        self.width_board = self.var.width_board
        self.height_board = self.var.height_board
        self.board_surface = Surface(
            (self.width_board, self.height_board)
        ).convert_alpha()

    def blit_board(self) -> None:
        """Paste the state of the board onto the screen"""
        self.screen.blit(self.board_surface, (self.var.padding, self.var.padding))
        self.quit_box.render(self.screen)

    def draw_board(self) -> None:
        """Draw the board on the screen (needed to be sure to see the board)"""
        self.screen.fill(self.color_screen)
        pg.draw.rect(
            self.board_surface,
            self.color_board,
            (0, 0, self.width_board, self.height_board),
        )
        for i in range(7):
            for j in range(6):
                self.draw_token(i, j, None, self.var.radius_hole)
        self.blit_board()
        pg.display.update()

    def animate_fall(self, col: int, row: int, player: Symbol) -> None:
        """Animate the fall of a disk"""
        x = self.var.padding + col * self.var.size_cell + self.var.size_cell // 2
        for y in range(
            self.var.padding // 2,
            self.var.padding + row * self.var.size_cell + self.var.size_cell // 2,
            5,
        ):
            self.screen.fill(self.var.white)
            if player == self.var.symbol_player_1:
                color = self.var.color_player_1
            elif player == self.var.symbol_player_2:
                color = self.var.color_player_2
            self.draw_token(x, y, player, self.var.radius_disk, col_row=False, screen=self.screen)
            self.blit_board()
            pg.display.update()
        self.screen.fill(self.var.color_screen)
        self.draw_token(col, row, player, self.var.radius_hole)
        self.blit_board()
        pg.display.update()
        if self.volume:
            if self.language != "cat":
                sound = self.var.sound_disk_touch
            else:
                sound = ".png"
                while sound.split(".")[-1] != "mp3":
                    sound = "assets/cat/" + random_choice(listdir("assets/cat/"))
            playsound(sound, block=True)
