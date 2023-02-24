#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Optional

from interface.tools_writing import *
import variables as var
from variables import Rect, Color, pg

def x_in_rect(rect: Rect, coor: tuple[int, int]) -> bool:
    """Return whether coor is in the rectangle 'rect'"""
    return rect.left <= coor[0] <= rect.right and rect.top <= coor[1] <= rect.bottom


def handle_click(click_coor: tuple[int, int], list_rect: list[Rect]) -> int:
    """Return the index of the box the click was in"""
    for i in range(len(list_rect)):
        if x_in_rect(list_rect[i], click_coor):
            return i
    return -1


def highlight_box(box: Rect, color_box: Color, text: str, color_text: Color) -> None:
    """Highlight the clicked box to be in a color or another"""
    pg_text = create_text_rendered(text, color_text)
    pg.draw.rect(var.screen, color_box, box)
    var.screen.blit(pg_text, (box.x + var.text_box_spacing, box.y + var.text_box_spacing))
    pg.display.update()


def draw_agreement_box(text: str, position: float = 0.75) -> Rect:
    """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
    agreement = create_text_rendered(text, var.black)
    s = agreement.get_size()
    x = (var.width_screen - s[0]) // 2 - var.text_box_spacing
    y = int(position * var.height_screen)
    box = write_text_box(agreement, var.color_screen, x, y)
    pg.display.update()
    return box


def draw_cancel_box() -> Rect:
    """Draw the box that allow the user to take a step back"""
    cancel = create_text_rendered(var.text_cancel_box, var.black)
    return write_on_line([cancel], var.white, *var.coor_cancel_box, align=-1)[0]


def draw_quit_box() -> Rect:
    """Draw the box that allow the user to take a step back"""
    quit_t = create_text_rendered(var.text_quit_box, var.black)
    return write_on_line([quit_t], var.white, *var.coor_quit_box, align=1)[0]


def handle_quit(quit_box: Rect, mouse: tuple[int, int]) -> None:
    """Function to call when wanting to see if user clicked in the quitting box"""
    if x_in_rect(quit_box, mouse):
        print("You choose to quit the game\nYou are disapointing me")
        pg.quit()
        sys.exit()


def update_screen(rect: Optional[Rect] = None, pause: float = 0.0) -> None:
    """Update the whole screen by default or only part of it"""
    var.screen.blit(var.board_surface, (var.padding, var.padding))
    if rect is not None:
        pg.display.update(rect)
    else:
        pg.display.update()
    sleep(pause)


def draw_circle(n: int, m: int, color: Color, r: int) -> None:
    """Draw a circle in the corresponding column, and row"""
    x = n * var.size_cell + var.size_cell // 2
    y = m * var.size_cell + var.size_cell // 2
    pg.draw.circle(var.board_surface, color, (x, y), r)
