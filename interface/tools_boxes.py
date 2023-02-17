#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

from interface.tools_writing import *


def x_in_rect(rect, coor):
    return (
        rect[0] <= coor[0] <= rect[0] + rect[2]
        and rect[1] <= coor[1] <= rect[1] + rect[3]
    )


def handle_click(click_coor, list_rect):
    for i in range(len(list_rect)):
        if x_in_rect(list_rect[i], click_coor):
            return i
    return -1


def highlight_box(box, text, color):
    pg.draw.rect(screen, color, box)
    x, y, a, b = box
    screen.blit(text, (x + text_box_spacing, y + text_box_spacing))
    pg.display.update()


def draw_agreement_box(text):
    agreement = create_options_text(text, black)
    s = agreement.get_size()
    x = (width_screen - s[0]) // 2 - text_box_spacing
    y = int(0.75 * height_screen)
    box = (x, y, s[0] + 2 * text_box_spacing, s[1] + 2 * text_box_spacing)
    pg.draw.rect(screen, color_screen, box)
    screen.blit(agreement, (x + text_box_spacing, y + text_box_spacing))
    pg.display.update()
    return box


def highlight_clicked_box(box_clicked, index_box, color_box, color_text):
    text = create_options_text(f"Level {index_box}", color_text)
    highlight_box(box_clicked, text, color_box)


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
