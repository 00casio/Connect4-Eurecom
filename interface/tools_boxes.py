#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Optional

from interface.tools_writing import *


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
    pg.draw.rect(screen, color_box, box)
    screen.blit(pg_text, (box.x + text_box_spacing, box.y + text_box_spacing))
    pg.display.update()


def draw_agreement_box(text: str, position: float = 0.75) -> Rect:
    """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
    agreement = create_text_rendered(text, black)
    s = agreement.get_size()
    x = (width_screen - s[0]) // 2 - text_box_spacing
    y = int(position * height_screen)
    box = write_text_box(agreement, color_screen, x, y)
    pg.display.update()
    return box


def draw_cancel_box() -> Rect:
    """Draw the box that allow the user to take a step back"""
    cancel = create_text_rendered(text_cancel_box, black)
    return write_on_line([cancel], white, *coor_cancel_box, align=-1)[0]


def draw_quit_box() -> Rect:
    """Draw the box that allow the user to take a step back"""
    quit_t = create_text_rendered(text_quit_box, black)
    return write_on_line([quit_t], white, *coor_quit_box, align=1)[0]


def handle_quit(quit_box: Rect, mouse: tuple[int, int]) -> None:
    """Function to call when wanting to see if user clicked in the quitting box"""
    if x_in_rect(quit_box, mouse):
        print("You choose to quit the game\nYou are disapointing me")
        pg.quit()
        sys.exit()


def update_screen(rect: Optional[Rect] = None, pause: float = 0.0) -> None:
    """Update the whole screen by default or only part of it"""
    screen.blit(board_surface, (padding, padding))
    if rect is not None:
        pg.display.update(rect)
    else:
        pg.display.update()
    sleep(pause)


def draw_circle(n: int, m: int, color: Color, r: int) -> None:
    """Draw a circle in the corresponding column, and row"""
    x = n * size_cell + size_cell // 2
    y = m * size_cell + size_cell // 2
    pg.draw.circle(board_surface, color, (x, y), r)
