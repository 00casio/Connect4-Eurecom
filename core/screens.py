#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import time
from typing import Any, Callable, Iterator, Optional, Union

import cv2
import numpy as np
import pygame as pg
from playsound import playsound

from core.utils import Tools, Box
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
    ) -> None:
        """ Initialize the values """
        Tools.__init__(self, var, screen, volume, camera)
        self.gestures = gesture
        self.cancel_box: Optional[Rect] = None
        self.box_clicked = self.var.box_out
        self.screen.fill(color_fill)
        self.draw_cancel = cancel_box
        self.draw_quit = quit_box
        if cancel_box:
            self.draw_cancel_box()
        if quit_box:
            self.draw_quit_box()

    def draw_cancel_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        self.cancel_box = Box(self.var.text_cancel_box, self.var.black, self.var.white, coordinate=self.var.coor_cancel_box, align=(-1, 1))
        self.cancel_box.render(self.screen)

    def draw_quit_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        self.quit_box = Box(self.var.text_quit_box, self.var.black, self.var.white, coordinate=self.var.coor_quit_box, align=(1, 1))
        self.quit_box.render(self.screen)

    def reset_screen(
        self,
        color_screen: Color,
        boxes: list[Box]
    ) -> None:
        """ Reset the screen to a "blank" state """
        self.screen.fill(color_screen)
        for line in boxes:
            for b in line:
                b.render(self.screen)
        if self.draw_cancel:
            self.draw_cancel_box()
        if self.draw_quit:
            self.draw_quit_box()
        pg.display.update()

    def get_mouse_pos(self) -> tuple[int, int]:
        """Return the mouse position"""
        # print("Change this to have the position from the camera")
        return pg.mouse.get_pos()

    def human_move(self, color: Color) -> None:
        """ Function to use when it's the human's turn to move """
        self.screen.fill(self.var.color_screen)
        mouse_x, mouse_y = self.get_mouse_pos()
        if mouse_x < self.var.pos_min_x:
            mouse_x = self.var.pos_min_x
        elif mouse_x > self.var.pos_max_x:
            mouse_x = self.var.pos_max_x

        p = self.var.padding
        if p < mouse_x < p + self.var.width_board:
            col = (mouse_x - p) // self.var.size_cell
            rect_col = Rect(p + col * self.var.size_cell, 0, self.var.size_cell, p)
            pg.draw.rect(self.screen, self.var.color_highlight_column, rect_col)
        self.draw_quit_box()
        pg.draw.circle(self.screen, color, (mouse_x, p // 2), self.var.radius_disk)
        pg.display.update((mouse_x - p // 2, 0, p, p))

    def update_gesture(self, image: np.ndarray[Any, np.dtype[Any]]) -> None:
        """ Update the gesture class """
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.gestures.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            GestureController.classify_hands(results)
            self.gestures.handmajor.update_hand_result(self.gestures.hr_major)
            self.gestures.handminor.update_hand_result(self.gestures.hr_minor)

            self.gestures.handmajor.set_finger_state()
            self.gestures.handminor.set_finger_state()
            gest_name = self.gestures.handminor.get_gesture()

            if gest_name == Gest.PINCH_MINOR:
                Controller.handle_controls(
                    gest_name, self.gestures.handminor.hand_result
                )
            else:
                gest_name = self.gestures.handmajor.get_gesture()
                Controller.handle_controls(
                    gest_name, self.gestures.handmajor.hand_result
                )

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        else:
            Controller.prev_hand = None
        cv2.imshow("Gesture Controller", image)
        if cv2.waitKey(5) & 0xFF == 13:
            self.handle_quit(self.quit_box.center)

    def click(
        self,
        rect_play: Optional[Rect] = None,
        sound: str = Variables().sound_click_box,
        print_disk: bool = False,
        color_disk: Color = Variables().white,
        func: Callable = None,
        **args,
    ) -> tuple[int, int]:
        """Quit the function only when there is a click. Return the position of the click.
        If f is not None, then the function is called whith the argument 'event' at every iteration"""
        allow_quit = False
        while not allow_quit:
            if self.camera:
                success, image = GestureController.cap.read()
                if success:
                    self.update_gesture(image)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    allow_quit = True
                if print_disk:
                    self.human_move(color_disk)
                if func is not None:
                    func(**args)
        click = self.get_mouse_pos()
        if self.is_canceled(click):
            self.box_clicked = self.var.boxAI_cancel
        self.handle_quit(click)
        if rect_play is not None:
            while not self.x_in_rect(click, rect_play, ""):
                click = self.click(rect_play, sound, print_disk, color_disk)
        return click

    def is_canceled(self, click: tuple[int, int]) -> bool:
        """ Return if the cancel button was pressed """
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

    def handle_click(self, click_coor: tuple[int, int], list_rect: list[Union[Rect, Box]]) -> int:
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
        self.boxes_options = [[Box(self.var.text_difficulty_options[number_AI])]]
        boxes_ai_1 = []
        for i in range(len(self.var.boxAI_text_levels)):
            boxes_ai_1.append(Box(f"Level {i}", self.var.black, self.var.color_player_1))
        boxes_ai_2 = []
        for i in range(len(self.var.boxAI_text_levels)):
            boxes_ai_2.append(Box(f"Level {i}", self.var.black, self.var.color_player_2))
        self.boxes_options.append(boxes_ai_1)

        # self.options_levels is used to know in which the user clicked
        if self.number_AI == 2:
            self.boxes_options.append(boxes_ai_2)
            self.options_levels = [*boxes_ai_1, *boxes_ai_2]
        else:
            self.options_levels = [*boxes_ai_1]

        self.play_box: Optional[Rect] = None
        self.diff_AI_1, self.diff_AI_2 = -1, -1
        self.nbr_levels_AI_1 = len(self.boxes_options[1])
        self.center_all(self.boxes_options)
        self.screen_loop()

    def screen_loop(self) -> None:
        """ Select the possibble value for the AI (if AI, AI(s) level) """
        while self.box_clicked not in [self.var.boxAI_play, self.var.boxAI_cancel]:
            mouse_click = self.click()
            index_box = self.handle_click(mouse_click, self.options_levels)
            if index_box != -1:
                if 0 <= index_box < self.nbr_levels_AI_1:
                    # We redraw all boxes on the line (remove highlight)
                    for b in self.options_levels[:self.nbr_levels_AI_1]:
                        b.render(self.screen)
                    self.diff_AI_1 = index_box
                elif self.nbr_levels_AI_1 <= index_box < len(self.options_levels):
                    # Same here
                    for b in self.options_levels[self.nbr_levels_AI_1:]:
                        b.render(self.screen)
                    self.diff_AI_2 = index_box % self.nbr_levels_AI_1

                if self.diff_AI_1 != -1 and (
                    self.diff_AI_2 != -1 or self.number_AI == 1
                ):
                    self.play_box = self.draw_agreement_box("Sarah Connor ?")
                self.highlight_box(
                    self.options_levels[index_box],
                    self.var.color_options_highlight_box,
                    self.screen,
                    self.var.color_options_highlight_text,
                )
            elif self.play_box is not None and self.x_in_rect(
                mouse_click, self.play_box
            ):
                self.box_clicked = self.var.boxAI_play
            else:
                self.play_box = None
                self.diff_AI_1 = -1
                self.diff_AI_2 = -1
                self.reset_screen(
                    self.var.color_options_screen,
                    self.boxes_options
                )


class OpponentSelectionScreen(Screen):
    """ Not completed, will allow the user to chose it's oppponent """
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
        """ Update the screen with the raspberry pi we can connect to """
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
        """ Select a raspberry pi as the opponent """
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
        """ Reset the appearance of the option screen to the default """
        self.screen.fill(self.var.color_options_screen)
        if self.draw_cancel:
            self.draw_cancel_box()
        if self.draw_quit:
            self.draw_quit_box()
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
        """ Draw First Image (if) True Else Second (image) """
        if testing:
            box = self.draw_icon(first_image, self.size, position)
        else:
            box = self.draw_icon(second_image, self.size, position)
        return box

    def draw_vol_cam(self) -> tuple[Rect, Rect]:
        """ Draw the icon for the volume and the camera """
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
        """ Draw the languages """
        cs = self.var.center_screen
        sp = self.var.options_spacing
        y_now = cs[1] + 3 * sp // 2
        l = [self.var.image_english, self.var.image_french]
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
    ) -> None:
        Screen.__init__(self, var, screen, gesture, volume, camera)
        self.color_screen = self.var.white
        self.color_board = self.var.blue
        self.width_board = self.var.width_board
        self.height_board = self.var.height_board
        self.board_surface = Surface(
            (self.width_board, self.height_board)
        ).convert_alpha()

    def draw_circle(self, n: int, m: int, color: Color, r: int) -> None:
        """Draw a circle in the corresponding column, and row"""
        x = n * self.var.size_cell + self.var.size_cell // 2
        y = m * self.var.size_cell + self.var.size_cell // 2
        pg.draw.circle(self.board_surface, color, (x, y), r)

    def blit_board(self) -> None:
        """ Paste the state of the board onto the screen """
        self.screen.blit(self.board_surface, (self.var.padding, self.var.padding))
        self.draw_quit_box()

    def draw_board(self) -> None:
        """ Draw the board on the screen (needed to be sure to see the board) """
        self.screen.fill(self.color_screen)
        pg.draw.rect(
            self.board_surface,
            self.color_board,
            (0, 0, self.width_board, self.height_board),
        )
        for i in range(7):
            for j in range(6):
                self.draw_circle(i, j, self.var.color_trans, self.var.radius_hole)
        self.blit_board()
        pg.display.update()

    def animate_fall(self, col: int, row: int, color_player: Color) -> None:
        """ Animate the fall of a disk """
        x = self.var.padding + col * self.var.size_cell + self.var.size_cell // 2
        for y in range(
            self.var.padding // 2,
            self.var.padding + row * self.var.size_cell + self.var.size_cell // 2,
            5,
        ):
            self.screen.fill(self.var.white)
            pg.draw.circle(self.screen, color_player, (x, y), self.var.radius_disk)
            self.blit_board()
            pg.display.update()
        self.draw_circle(col, row, color_player, self.var.radius_hole)
        if self.volume:
            playsound(self.var.sound_disk_touch, block=True)
