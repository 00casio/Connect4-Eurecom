#!/usr/bin/python3
# -*- coding: utf-8 -*-

from variables import *


def compute_total_height(list_text):
    """ Calculate the total height of a list of text """
    total_size = 0
    for text in list_text:
        total_size += 2 * text_box_spacing
        if type(text) == list:
            total_size += max([t.get_size()[1] for t in text])
        else:
            total_size += text.get_size()[1]
    return total_size + (len(list_text) - 1) * options_spacing


def write_same_line(list_text, y, color_box):
    """ Write on the same line centered in the middle all elements in 'list_text' in the color 'color_box'.
    'color_box' can be list, but it must be the same size as 'list_text' """
    box_rect = []
    n = list_text
    x_tot = 0
    for text in list_text:
        x_tot += 2 * text_box_spacing + options_spacing + text.get_size()[0]
    x_tot -= options_spacing
    x_now = (width_screen - x_tot) // 2 - text_box_spacing

    for text in list_text:
        size = text.get_size()
        b_rect = (
            x_now,
            y,
            size[0] + 2 * text_box_spacing,
            size[1] + 2 * text_box_spacing,
        )
        pg.draw.rect(screen, color_box, b_rect)
        screen.blit(text, (x_now + text_box_spacing, y + text_box_spacing))
        box_rect.append(b_rect)
        x_now += 2 * text_box_spacing + size[0] + options_spacing

    new_y = (
        y
        + max([t.get_size()[1] for t in list_text])
        + 2 * text_box_spacing
        + options_spacing
    )
    return new_y, box_rect


def write_to_screen(text, y_now, color_box):
    """ Write 'text' on the screen in the color 'color_box' """
    if type(text) == list:
        new_y, box_rect = write_same_line(text, y_now, color_box)
    else:
        new_y, box_rect = write_same_line([text], y_now, color_box)
        box_rect = box_rect[0]
    return new_y, box_rect


def center_all(list_text, color_box=color_options_box):
    """ Write the texts in 'list_text' centered in the middle of the screen """
    if type(color_box) == list:
        assert len(list_text) == len(
            color_box
        ), f"list_text and color_box are not the same size ({len(list_text)} and {len(color_box)})"
    total_size = compute_total_height(list_text)
    rect_boxes = []
    y_now = (height_screen - total_size) // 2
    for i in range(len(list_text)):
        text = list_text[i]
        if type(color_box) == list:
            color = color_box[i]
        else:
            color = color_box
        y_now, box_rect = write_to_screen(text, y_now, color)
        rect_boxes.append(box_rect)
    pg.display.update()
    return rect_boxes


def create_options_text(text, color=color_options_text, font=text_font, size=text_size):
    """ Create text in the color, font, and size asked """
    font = pg.font.SysFont(font, size)
    return font.render(text, 1, color)
