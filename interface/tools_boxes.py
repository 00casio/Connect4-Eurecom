#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Optional

import variables as var
from interface.tools_writing import *
from variables import Color, Rect, pg



def highlight_box(box: Rect, color_box: Color, text: str, color_text: Color) -> None:
    """Highlight the clicked box to be in a color or another"""
    pg_text = create_text_rendered(text, color_text)
    pg.draw.rect(var.screen, color_box, box)
    var.screen.blit(
        pg_text, (box.x + var.text_box_spacing, box.y + var.text_box_spacing)
    )
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


def handle_quit(quit_box: Rect, mouse: tuple[int, int]) -> None:
    """Function to call when wanting to see if user clicked in the quitting box"""
    if x_in_rect(quit_box, mouse):
        print("You choose to quit the game\nYou are disapointing me")
        pg.quit()
        sys.exit()


def draw_circle(n: int, m: int, color: Color, r: int) -> None:
    """Draw a circle in the corresponding column, and row"""
    x = n * var.size_cell + var.size_cell // 2
    y = m * var.size_cell + var.size_cell // 2
    pg.draw.circle(var.board_surface, color, (x, y), r)
