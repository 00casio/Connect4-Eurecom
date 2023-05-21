#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Any, Sequence, Union, Optional

import pygame as pg

from core.variables import Color, Rect, Surface, Variables


def opponent(symbol_player: Any) -> Any:
    """ Gives symbol of the opponent """
    if symbol_player == Variables().symbol_player_1:
        return Variables().symbol_player_2
    else:
        return Variables().symbol_player_1


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
            raise NotImplementedError


class Config:
    """ The config class cotains all possible variables for the game """
    def __init__(self, var: Variables, arguments: Namespace) -> None:
        self.arg = arguments
        self.var = var
        self.var.sound = not self.arg.novolume
        self.var.camera = not self.arg.nocamera
        self.var.libai = not self.arg.no_libai
        self.load_language(self.arg.language)

    def load_language(self, language: str) -> None:
        """ Load the correct language in the variables """
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


class Box:
    def __init__(self, text: str, color_text: Color=Variables().color_options_text, color_rect: Color=Variables().color_options_box, coordinate: tuple[int,int]=(-1, -1), align: tuple[int, int]= (0,0)) -> None:
        """ Initialize all the variables fot this class.
        'align' desribes how the text and box are written according to the coordinate.
        For example, with align=(-1,0), the coordinates refer to the middle-left point of the box, and align=(1, -1) is the bottom-right corner"""

        self.text = text
        self.color_text = color_text
        self.color_rect = color_rect
        self.coor = coordinate
        self.align = align
        self.box: Optional[Rect] = None
        self.font_size = Variables().text_size
        self.font_name = Variables().text_font
        tbs = Variables().text_box_spacing
        self.spacings = [tbs, tbs, tbs, tbs]
        self.font_r = pg.font.SysFont(self.font_name, self.font_size)
        self.text_r = self.font_r.render(self.text, True, self.color_text)
 
    def render(self, screen: Surface) -> None:
        self.font_r = pg.font.SysFont(self.font_name, self.font_size)
        self.text_r = self.font_r.render(self.text, True, self.color_text)
        s = self.text_r.get_size()
        spa = self.spacings
        x = self.coor[0]
        if self.align[0] > -1: # AKA == 0 or == 1
            x -= spa[0] + s[0]//2
        if self.align[0] > 0: # AKA == 1
            x -= s[0]//2 + spa[2] + s[0]%2 # Correction if s[0] is odd
        y = self.coor[1]
        if self.align[1] < 1:
            y -= spa[1] + s[1]//2
        if self.align[1] < 0:
            y -= s[1]//2 + spa[3] + s[1]%2 # Correction if s[0] is odd

        self.box = Rect(x, y, spa[0] + spa[2] + s[0], spa[1] + spa[3] + s[1])
        pg.draw.rect(screen, self.color_rect, self.box)
        screen.blit(self.text_r, (x + spa[0], y + spa[1]))

    def change_sfs(self, new_size: Optional[int] =None, new_font: Optional[int]=None, spacings: list[int]= []) -> None:
        if new_size is not None:
            self.font_size = new_size
        if new_font is not None:
            self.font_name = new_font
        if len(spacings) == 0:
            self.spacings = [tbs, tbs, tbs, tbs]
        elif len(spacings) == 1:
            self.spacings = [spacings[0] for _ in range(4)]
        elif len(spacings) == 2:
            self.spacings = [spacings[i%2] for i in range(4)]
        elif len(spacings) == 4:
            self.spacings = spacings


class Tools:
    """ A class aggregating many tools """
    def __init__(
        self, var: Variables, screen: Surface, volume: bool, camera: bool
    ) -> None:
        """ Initialize the values """
        self.screen = screen
        self.volume = volume
        self.camera = camera
        self.var = var

    def recompute_total_size(self, list_boxes: list[list[Box]]) -> list[tuple[int, int]]:
        total_sizes = []
        for line in list_boxes:
            line_h = 0
            line_w = 0
            for box in line:
                s = box.text_r.get_size()
                spa = box.spacings
                line_w += s[0] + spa[0] + spa[2]
                line_h = max(s[1] + spa[1] + spa[3], line_h)
            total_sizes.append((line_w + self.var.options_spacing * (len(line) - 1), line_h))
        return total_sizes

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

    def recenter_all(self, list_lines_boxes: list[list[Box]]) -> None:
        n = len(list_lines_boxes)
        lines_size = self.recompute_total_size(list_lines_boxes)
        c = self.var.center_screen
        os = self.var.options_spacing

        y = c[1] - sum([lines_size[i][1] for i in range(n)]) // 2 - os * (n - 1) // 2
        for i in range(n):
            line = list_lines_boxes[i]
            x = c[0] - (lines_size[i][0]) // 2
            for box in line:
                box.coor = (x, y)
                box.align = (-1, 1)
                box.render(self.screen)
                x += box.spacings[0] + box.spacings[2] + box.text_r.get_size()[0] + os
            y += lines_size[i][1] + os
        pg.display.update()

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
        text: Union[str, Sequence[str]],
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

    def make_icon(self, image: str, size: tuple[int, int]) -> Surface:
        """ Scale the image to the wanted size """
        img = pg.image.load(image)
        icon = pg.transform.scale(img, size)
        return icon

    def draw_icon(
        self, image_path: str, size: tuple[int, int], position: tuple[int, int]
    ) -> Rect:
        """ Draw the image at image_path with the size and position wanted """
        p = self.var.text_box_spacing
        icon = self.make_icon(image_path, size)
        box = Rect(position[0] - p, position[1] - p, size[0] + 2 * p, size[1] + 2 * p)
        pg.draw.rect(self.screen, self.var.very_light_blue, box)
        self.screen.blit(icon, position)
        return box
