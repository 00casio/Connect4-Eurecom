#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Any, Callable, Optional

import numpy as np
import pygame as pg
from playsound import playsound

from AI_test import best_col_prediction, minimax2
from gesture import *
from variables import Symbol, Variables

pg.init()

Color = pg.Color
Rect = pg.Rect
Surface = pg.Surface


class Config:
    def __init__(self, var: Variables, arguments):
        self.arg = arguments
        self.var = var
        self.var.sound = not self.arg.novolume
        self.load_language(self.arg.language)

    def load_language(self, language):
        if language not in ["en", "fr"]:
            print("This language is not translated.\nI will use English")
            language = "en"
        self.var.boxAI_text_levels = self.var.texts[language]["boxAI_text_levels"]
        self.var.text_options_play = self.var.texts[language]["options_play"]
        self.var.text_options_options = self.var.texts[language]["options_options"]
        self.var.text_options_play_HvH = self.var.texts[language]["options_play_HvH"]
        self.var.text_options_play_HvAI = self.var.texts[language]["options_play_HvAI"]
        self.var.text_options_play_AIvAI = self.var.texts[language][
            "options_play_AIvAI"
        ]
        self.var.text_options_difficulty_HvAI = self.var.texts[language][
            "options_difficulty_HvAI"
        ]
        self.var.text_options_difficulty_AIvAI = self.var.texts[language][
            "options_difficulty_AIvAI"
        ]
        self.var.text_difficulty_options = [
            "",
            self.var.text_options_difficulty_HvAI,
            self.var.text_options_difficulty_AIvAI,
        ]
        self.var.text_cancel_box = self.var.texts[language]["cancel_box"]
        self.var.text_quit_box = self.var.texts[language]["quit_box"]
        self.var.message_quit = self.var.texts[language]["message_quit"]


class Element:
    """An element is composed of a box and text"""

    def __init__(
        self,
        var: Variables,
        pos: tuple[int, int],
        text: str,
        screen: Surface,
        text_color: Color = Variables().black,
        box_color: Color = Variables().color_options_box,
        font: pg.font.Font = Variables().main_font,
        padd: tuple[int, int] = (
            Variables().text_box_spacing,
            Variables().text_box_spacing,
        ),
    ) -> None:
        self.var = var
        self.font = font
        self.pos = pos
        self.text_color = text_color
        self.color_box = box_color
        self.screen = screen
        self.padding = padd
        self.draw(text)

    def draw(self, text: str) -> None:
        self.text = self.font.render(text, True, self.text_color)
        s = self.text.get_size()
        self.box = Rect(
            self.pos[0],
            self.pos[1],
            s[0] + 2 * self.padding[0],
            s[1] + 2 * self.padding[1],
        )
        pg.draw.rect(self.screen, self.color_box, self.box)
        self.screen.blit(self.text, (self.box.x, self.box.y))
        pg.display.update(self.box)


class Tools:
    def __init__(
        self, var: Variables, screen: Surface, volume: bool, camera: bool
    ) -> None:
        self.screen = screen
        self.volume = volume
        self.camera = camera
        self.var = var

    def compute_total_size(
        self, array_text: list[list[Surface]]
    ) -> tuple[int, list[int]]:
        """Compute the height of a list of line of texts and the width of each line"""
        total_height = 0
        total_width = []
        for line_text in array_text:
            total_height += (
                max([t.get_size()[1] for t in line_text])
                + 2 * self.var.text_box_spacing
            )
            width_now = (
                sum([t.get_size()[0] for t in line_text])
                + 2 * self.var.text_box_spacing * len(line_text)
                + (len(line_text) - 1) * self.var.options_spacing
            )
            total_width.append(width_now)
        total_height += (len(array_text) - 1) * self.var.options_spacing
        return (total_height, total_width)

    def write_text_box(
        self,
        text: Surface,
        color_box: Color,
        x: int,
        y: int,
        spacing_x: int = Variables().text_box_spacing,
        spacing_y: int = Variables().text_box_spacing,
    ) -> Rect:
        """Write the text and create the box arround it"""
        size = text.get_size()
        b_rect = Rect(x, y, size[0] + 2 * spacing_x, size[1] + 2 * spacing_y)
        pg.draw.rect(self.screen, color_box, b_rect)
        self.screen.blit(text, (x + spacing_x, y + spacing_y))
        return b_rect

    def write_on_line(
        self,
        list_text: list[Surface],
        color_box: Color,
        x: int,
        y: int,
        align: int = 0,
        space_x: int = Variables().text_box_spacing,
        space_y: int = Variables().text_box_spacing,
        space_box: int = Variables().options_spacing,
    ) -> list[Rect]:
        """write 'list_text' on a single line. 'align' can take -1 for left, 0 for middle, and 1 for right"""
        boxes = []
        width_line = self.compute_total_size([list_text])[1][0]
        if align == -1:
            write_x = x
        elif align == 0:
            write_x = (x - width_line) // 2
        elif align == 1:
            write_x = x - width_line
        else:
            raise ValueError("align is not -1, 0, or 1. Correct this")
        for text in list_text:
            boxes.append(
                self.write_text_box(text, color_box, write_x, y, space_x, space_y)
            )
            write_x += text.get_size()[0] + 2 * space_x + space_box
        # pg.display.update()
        return boxes

    def center_all(
        self,
        array_text: list[list[Surface]],
        color_box: list[Color] = [Variables().color_options_box],
    ) -> list[list[Rect]]:
        """Write the texts in 'array_text' centered in the middle of the screen.
        If 'color_box' is a single element, then all boxes will have the same color"""

        color = [color_box[-1]] * (len(array_text) - len(color_box)) + color_box
        total_size = self.compute_total_size(array_text)
        rect_boxes = []
        y_now = (self.var.height_screen - total_size[0]) // 2
        for i in range(len(array_text)):
            line_text = array_text[i]
            box_rect = self.write_on_line(
                line_text, color[i], self.var.width_screen, y_now
            )
            y_now += (
                line_text[0].get_size()[1]
                + 2 * self.var.text_box_spacing
                + self.var.options_spacing
            )
            rect_boxes.append(box_rect)
        pg.display.update()
        return rect_boxes

    def create_text_rendered(
        self,
        text: str,
        color: Color = Variables().color_options_text,
        font: str = Variables().text_font,
        size: int = Variables().text_size,
    ) -> Surface:
        """Create text in the color, font, and size asked"""
        pg_font = pg.font.SysFont(font, size)
        return pg_font.render(text, True, color)

    def highlight_box(
        self, box: Rect, color_box: Color, screen: Surface, text: str, color_text: Color
    ) -> None:
        """Highlight the clicked box to be in a color or another"""
        pg_text = self.create_text_rendered(text, color_text)
        pg.draw.rect(screen, color_box, box)
        screen.blit(
            pg_text,
            (box.x + self.var.text_box_spacing, box.y + self.var.text_box_spacing),
        )
        pg.display.update()

    def draw_agreement_box(self, text: str, position: float = 0.75) -> Rect:
        """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
        agreement = self.create_text_rendered(text, self.var.black)
        s = agreement.get_size()
        x = (self.var.width_screen - s[0]) // 2 - self.var.text_box_spacing
        y = int(position * self.var.height_screen)
        box = self.write_text_box(agreement, self.var.color_screen, x, y)
        pg.display.update()
        return box

    def make_icon(self, image, size):
        img = pg.image.load(image)
        icon = pg.transform.scale(img, size)
        return icon

    def draw_icon(self, image, size, position):
        p = self.var.text_box_spacing
        icon = self.make_icon(image, size)
        box = Rect(position[0] - p, position[1] - p, size[0] + 2 * p, size[1] + 2 * p)
        pg.draw.rect(self.screen, self.var.very_light_blue, box)
        self.screen.blit(icon, position)
        return box


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
        Tools.__init__(self, var, screen, volume, camera)
        self.elements: list[Element] = []
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
        cancel = self.create_text_rendered(self.var.text_cancel_box, self.var.black)
        self.cancel_box = self.write_on_line(
            [cancel],
            self.var.white,
            self.var.coor_cancel_box[0],
            self.var.coor_cancel_box[1],
            align=-1,
        )[0]

    def draw_quit_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        quit_t = self.create_text_rendered(self.var.text_quit_box, self.var.black)
        self.quit_box = self.write_on_line(
            [quit_t],
            self.var.white,
            self.var.coor_quit_box[0],
            self.var.coor_quit_box[1],
            align=1,
        )[0]

    def reset_screen(
        self,
        color_screen: Color,
        text: list[list[Surface]],
        colors_boxes: list[Color],
    ) -> None:
        self.screen.fill(color_screen)
        self.center_all(text, colors_boxes)
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

    def update_gesture(self, image):
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
        click = self.get_mouse_pos()
        if self.is_canceled(click):
            self.box_clicked = self.var.boxAI_cancel
        self.handle_quit(click)
        if rect_play is not None:
            while not self.x_in_rect(click, rect_play, ""):
                click = self.click(rect_play, print_disk, color_disk)
        return click

    def is_canceled(self, click: tuple[int, int]) -> bool:
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
        rect: Optional[Rect],
        sound: str = Variables().sound_click_box,
    ) -> bool:
        """Return whether coor is in the rectangle 'rect'"""
        if rect is None:
            return False
        status = (
            rect.left <= coor[0] <= rect.right and rect.top <= coor[1] <= rect.bottom
        )
        if status and sound != "" and self.volume:
            playsound(sound, block=False)
        return status

    def handle_click(self, click_coor: tuple[int, int], list_rect: list[Rect]) -> int:
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

        texts_level = [
            self.create_text_rendered(f"Level {i}")
            for i in range(len(self.var.boxAI_text_levels))
        ]

        self.text_options = [
            [self.create_text_rendered(self.var.text_difficulty_options[number_AI])],
            texts_level,
        ]
        self.options_colors = [self.var.color_options_box, self.var.color_player_1]
        if self.number_AI == 2:
            self.options_colors.append(self.var.color_player_2)
        self.boxes_levels = self.center_all(self.text_options, self.options_colors)
        self.play_box: Optional[Rect] = None
        self.diff_AI_1, self.diff_AI_2 = -1, -1
        self.nbr_levels_AI_1 = len(self.boxes_levels[1])
        if self.number_AI == 2:
            self.text_options.append(texts_level)
            self.boxes_levels = self.center_all(self.text_options, self.options_colors)
            self.options_levels = [*self.boxes_levels[1], *self.boxes_levels[2]]
        else:
            self.options_levels = [*self.boxes_levels[1]]
        self.reset_screen(
            self.var.color_options_screen, self.text_options, self.options_colors
        )
        self.screen_loop()

    def screen_loop(self) -> None:
        while self.box_clicked not in [self.var.boxAI_play, self.var.boxAI_cancel]:
            mouse_click = self.click()
            index_box = self.handle_click(mouse_click, self.options_levels)
            if index_box != -1:
                if 0 <= index_box < self.nbr_levels_AI_1:
                    self.write_on_line(
                        self.text_options[1],
                        self.var.color_player_1,
                        self.var.width_screen,
                        self.boxes_levels[1][0].top,
                    )
                    self.diff_AI_1 = index_box
                elif self.nbr_levels_AI_1 <= index_box < len(self.options_levels):
                    self.write_on_line(
                        self.text_options[2],
                        self.var.color_player_2,
                        self.var.width_screen,
                        self.boxes_levels[2][0].top,
                    )
                    self.diff_AI_2 = index_box % self.nbr_levels_AI_1
                if self.diff_AI_1 != -1 and (
                    self.diff_AI_2 != -1 or self.number_AI == 1
                ):
                    self.play_box = self.draw_agreement_box("Sarah Connor ?")
                self.highlight_box(
                    self.options_levels[index_box],
                    self.var.color_options_highlight_box,
                    self.screen,
                    f"Level {index_box % self.nbr_levels_AI_1}",
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
                    self.text_options,
                    self.options_colors,
                )
                pg.display.update()


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
    ):
        Screen.__init__(self, var, screen, gesture, volume, camera)
        self.size = (self.var.width_screen // 10, self.var.height_screen // 10)
        self.nbr_line = 2
        self.vol, self.cam = self.draw_vol_cam()
        self.flags = list(self.draw_language())
        pg.display.update()

    def reset_screen(self):
        self.screen.fill(self.var.color_options_screen)
        if self.draw_cancel:
            self.draw_cancel_box()
        if self.draw_quit:
            self.draw_quit_box()
        self.vol, self.cam = self.draw_vol_cam()
        self.flags = list(self.draw_language())
        pg.display.update()
    
    def dfites(self, testing, position, first_image, second_image):
        if testing:
            box = self.draw_icon(first_image, self.size, position)
        else:
            box = self.draw_icon(second_image, self.size, position)
        return box

    def draw_vol_cam(self):
        cs = self.var.center_screen
        sp = self.var.options_spacing
        x_now = cs[0] - self.size[0] - sp
        y = cs[1] - self.size[1] // 2 - 3 * sp // 2
        vol = self.dfites(self.volume, (x_now, y), self.var.image_volume_on, self.var.image_volume_muted)
        x_now += sp + self.size[0] + 2 * self.var.text_box_spacing
        cam = self.dfites(self.camera, (x_now, y), self.var.image_camera, self.var.image_nocamera)
        return vol, cam

    def draw_language(self):
        cs = self.var.center_screen
        sp = self.var.options_spacing
        y_now = cs[1] + 3*sp//2
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
        self.screen.blit(self.board_surface, (self.var.padding, self.var.padding))
        self.draw_quit_box()

    def draw_board(self) -> None:
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


class Board(np.ndarray[Any, np.dtype[Any]]):
    def __new__(cls: np.ndarray[Any, np.dtype[Any]]) -> Any:
        self = np.array([[Variables().symbol_no_player] * 7 for i in range(6)]).view(
            cls
        )
        self.state: Optional[np.ndarray[np.uint8, np.dtype[np.uint8]]] = None
        return self

    def find_free_slot(self, i: int) -> int:
        """Return the index of the first free slot"""
        col = self[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == Variables().symbol_no_player:
                return j
        return -1

    def state_to_bits(self) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        n = "0b"
        for j in range(len(self.state[0]) - 1, -1, -1):
            n += "0"
            for i in range(len(self.state)):
                n += f"{int(self.state[i, j])}"  # <==> n += str(b)
        return n

    def state_win(self, symbol: Symbol) -> bool:
        self.state = np.zeros(self.shape, dtype=np.uint8)
        self.state[np.where(self == symbol)] = 1
        bits = int(self.state_to_bits(), 2)

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

    def horiz(self, row, col):
        for i in range(max(0, col - 3), min(7, col + 1)):
            if len(self[row, i : i + 4]) == 4:
                yield self[row, i : i + 4]

    def vert(self, row, col):
        for i in range(max(0, row - 3), min(7, row + 1)):
            if len(self[i : i + 4, col]) == 4:
                yield self[i : i + 4, col]

    def backslash(self, row, col, back=True):
        if back:
            board = self.copy()
        else:
            board = np.fliplr(self.copy())
        i, j = row, col
        while i > max(0, row - 3) and j > max(0, col - 3):
            i -= 1
            j -= 1

        while i < min(7, row + 1) and j < min(7, col + 1):
            if i >= 3 or j >= 4:
                break
            yield [board[i + k, j + k] for k in range(4)]
            i += 1
            j += 1

    def slash(self, row, col):
        yield from self.backslash(row, col[3 - (col - 3)], back=False)


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

    def play(self, board: Board, screen: Screen, volume: bool) -> tuple[int, int]:
        if self.is_ai:
            score, col = minimax2(board, 3, self.symbol.v)
            print("score is ", score)
        else:
            p = self.var.padding
            box_allowed = Rect(p, p, self.var.width_board, self.var.height_board)
            click = screen.click(box_allowed, print_disk=True, color_disk=self.color)
            col = (click[0] - self.var.padding) // self.var.size_cell
        row = board.find_free_slot(col)
        if row == -1 and volume:
            playsound(self.var.sound_error, block=False)
            col, row = self.play(board, screen, volume)
        return (col, row)

    def __eq__(self, other: object) -> bool:
        eq: bool = False
        if isinstance(other, Player):
            eq = self.symbol == other.symbol
        elif isinstance(other, Symbol):
            eq = self.symbol == other
        return eq


class Game:
    """The big class that will regulate everything"""

    def __init__(self, var: Variables, args) -> None:
        # Gestures
        self.gestures = GestureController()

        # Players
        self.var = var
        self.player_1 = Player(self.var, 1, False)
        self.player_2 = Player(self.var, 2, False)
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
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size
        ):
            if self.player_playing == self.player_1:
                play = self.player_1.play(self.board, gaming, self.volume)
            else:
                play = self.player_2.play(self.board, gaming, self.volume)
            gaming.animate_fall(play[0], play[1], self.player_playing.color)
            self.board[play[1], play[0]] = self.player_playing.symbol.v
            self.inverse_player()
            self.num_turn += 1
        self.draw_winner(gaming, play)

    def draw_winner(self, screen: GamingScreen, lastclick: tuple[int, int]) -> None:
        winner = self.who_is_winner()
        sound = self.var.sound_winner_victory
        End = Screen(self.var, self.screen, self.gestures, volume=self.volume, camera=self.camera)
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
        self.board.state_win(winner.symbol)
        bits = int(self.board.state_to_bits(), 2)

        def complete(bits, direction):
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
            options.reset_screen()
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
