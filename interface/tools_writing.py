#!/usr/bin/python3
# -*- coding: utf-8 -*-

from variables import *


def compute_total_size(array_text: list[list[Surface]]) -> tuple[float, list[float]]:
    """Compute the height of a list of line of texts and the width of each line"""
    total_height = 0
    total_width = []
    for line_text in array_text:
        total_height += max([t.get_size()[1] for t in line_text]) + 2 * text_box_spacing
        width_now = (
            sum([t.get_size()[0] for t in line_text])
            + 2 * text_box_spacing * len(line_text)
            + (len(line_text) - 1) * options_spacing
        )
        total_width.append(width_now)
    total_height += (len(array_text) - 1) * options_spacing
    return (total_height, total_width)


def write_text_box(
    text: Surface,
    color_box: Color,
    x: int,
    y: int,
    spacing_x: int = text_box_spacing,
    spacing_y: int = text_box_spacing,
) -> Rect:
    """Write the text and create the box arround it"""
    size = text.get_size()
    b_rect = Rect(x, y, size[0] + 2 * spacing_x, size[1] + 2 * spacing_y)
    pg.draw.rect(screen, color_box, b_rect)
    screen.blit(text, (x + spacing_x, y + spacing_y))
    return b_rect


def write_on_line(
    list_text: list[Surface],
    color_box: Color,
    x: int,
    y: int,
    align: int = 0,
    space_x: int = text_box_spacing,
    space_y: int = text_box_spacing,
    space_box: int = options_spacing
) -> list[Rect]:
    """write 'list_text' on a single line. 'align' can take -1 for left, 0 for middle, and 1 for right"""
    boxes = []
    width_line = compute_total_size([list_text])[1][0]
    if align == -1:
        write_x = x
    elif align == 0:
        write_x = (x - width_line) // 2
    elif align == 1:
        write_x = x - width_line
    else:
        raise ValueError("align is not -1, 0, or 1. Correct this")
    for text in list_text:
        boxes.append(write_text_box(text, color_box, write_x, y, space_x, space_y))
        write_x += text.get_size()[0] + 2 * space_x + space_box
    pg.display.update()
    return boxes


def write_on_column(
    list_text: list[Surface],
    color_box: Color,
    x: int,
    y: int,
    align: int = 0,
    space_x: int = text_box_spacing,
    space_y: int = text_box_spacing,
    space_box: int = options_spacing
) -> list[Rect]:
    boxes = []
    height_line = compute_total_size([list_text])[0]
    if align == -1:
        write_y = y
    elif align == 0:
        write_y = (y - height_line) // 2
    elif align == 1:
        write_y = y - height_line
    else:
        raise ValueError("align is not -1, 0, or 1. Correct this")
    for text in list_text:
        boxes.append(write_text_box(text, color_box, x, write_y))
        write_y += text.get_size()[1] + 2 * space_y + space_box
    pg.display.update()
    return boxes


def center_all(
    array_text: list[list[Surface]], color_box: Color | list[Color] = color_options_box
) -> list[list[Rect]]:
    """Write the texts in 'array_text' centered in the middle of the screen.
    If 'color_box' is a single element, then all boxes will have the same color"""
    if type(color_box) == list:
        assert len(array_text) == len(
            color_box
        ), f"array_text and color_box are not the same size ({len(array_text)} and {len(color_box)})"
    total_size = compute_total_size(array_text)
    rect_boxes = []
    y_now = (height_screen - total_size[0]) // 2
    for i in range(len(array_text)):
        line_text = array_text[i]
        if type(color_box) == list:
            color = color_box[i]
        else:
            color = color_box
        box_rect = write_on_line(line_text, color, width_screen, y_now)
        y_now += line_text[0].get_size()[1] + 2 * text_box_spacing + options_spacing
        rect_boxes.append(box_rect)
    pg.display.update()
    return rect_boxes


def create_text_rendered(
    text: str,
    color: Color = color_options_text,
    font: str = text_font,
    size: int = text_size,
) -> Surface:
    """Create text in the color, font, and size asked"""
    font = pg.font.SysFont(font, size)
    return font.render(text, 1, color)
