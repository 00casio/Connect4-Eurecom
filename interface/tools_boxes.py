#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

from interface.tools_writing import *


def x_in_rect(rect, coor):
    """Return whether coor is in the rectangle 'rect'"""
    return (
        rect[0] <= coor[0] <= rect[0] + rect[2]
        and rect[1] <= coor[1] <= rect[1] + rect[3]
    )


def handle_click(click_coor, list_rect):
    """Return the index of the box the click was in"""
    for i in range(len(list_rect)):
        if x_in_rect(list_rect[i], click_coor):
            return i
    return -1


def highlight_box(box, color_box, text, color_text):
    """Highlight the clicked box to be in a color or another"""
    pg_text = create_options_text(text, color_text)
    pg.draw.rect(screen, color_box, box)
    x, y, a, b = box
    screen.blit(pg_text, (x + text_box_spacing, y + text_box_spacing))
    pg.display.update()


def draw_agreement_box(text, position=0.75):
    """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
    agreement = create_options_text(text, black)
    s = agreement.get_size()
    x = (width_screen - s[0]) // 2 - text_box_spacing
    y = int(position * height_screen)
    box = (x, y, s[0] + 2 * text_box_spacing, s[1] + 2 * text_box_spacing)
    pg.draw.rect(screen, color_screen, box)
    screen.blit(agreement, (x + text_box_spacing, y + text_box_spacing))
    pg.display.update()
    return box


def update_screen(rect=None, pause=0):
    screen.blit(board_surface, (padding, padding))
    if rect is not None:
        pg.display.update(rect)
    else:
        pg.display.update()
    sleep(pause)


def draw_circle(n, m, color, r):
    x = n * size_cell + size_cell // 2
    y = m * size_cell + size_cell // 2
    pg.draw.circle(board_surface, color, (x, y), r)
