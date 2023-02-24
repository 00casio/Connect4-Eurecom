#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface.tools_boxes import *
from interface.tools_writing import *
import variables as var
from variables import Color, Rect, Surface, Symbol, pg


def reset_screen(
    color_screen: Color, text: list[list[Surface]], colors_boxes: Color | list[Color]
) -> tuple[Rect, Rect]:
    var.screen.fill(color_screen)
    center_all(text, colors_boxes)
    a, b = draw_cancel_box(), draw_quit_box()
    pg.display.update()
    return (a, b)


def options_1AI(text_options: list[list[Surface]]) -> tuple[Symbol, int]:
    """Show the options for when there is only 1 AI in the game"""
    boxes_levels = center_all(text_options)
    cancel_box, quit_box = reset_screen(
        var.color_options_screen, text_options, var.color_options_box
    )
    box_clicked = var.boxAI_out
    play_box = None
    difficulty_AI = -1
    while box_clicked not in [var.boxAI_play, var.boxAI_cancel]:
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONUP:
                continue
            cancel_box, quit_box = reset_screen(
                var.color_options_screen, text_options, var.color_options_box
            )
            mouse_click = pg.mouse.get_pos()
            if x_in_rect(cancel_box, mouse_click):
                box_clicked = var.boxAI_cancel
            handle_quit(quit_box, mouse_click)
            index_box = handle_click(mouse_click, boxes_levels[1])
            if index_box != var.boxAI_out:
                highlight_box(
                    boxes_levels[1][index_box],
                    var.color_options_highlight_box,
                    f"Level {index_box}",
                    var.color_options_highlight_text,
                )
                play_box = draw_agreement_box(var.boxAI_text_levels[index_box])
                difficulty_AI = index_box
            elif play_box is not None and x_in_rect(play_box, mouse_click):
                box_clicked = var.boxAI_play
            else:
                play_box = None
                pg.display.update()
    return (var.symbol_player_2, difficulty_AI)


def options_2AI(text_options: list[list[Surface]]) -> tuple[int, int]:
    """Show the options for when there are 2 AIs in the game"""
    colors = [var.color_options_box, var.color_player_1, var.color_player_2]
    boxes_levels = center_all(text_options, colors)
    box_clicked = var.boxAI_out
    play_box = None
    diff_AI_1, diff_AI_2 = -1, -1
    options_levels = [*boxes_levels[1], *boxes_levels[2]]
    nbr_levels_AI_1 = len(boxes_levels[1])
    cancel_box, quit_box = reset_screen(var.color_options_screen, text_options, colors)
    while box_clicked not in [var.boxAI_play, var.boxAI_cancel]:
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONUP:
                continue
            mouse_click = pg.mouse.get_pos()
            if x_in_rect(cancel_box, mouse_click):
                box_clicked = var.boxAI_cancel
            handle_quit(quit_box, mouse_click)
            index_box = handle_click(mouse_click, options_levels)
            if index_box != var.boxAI_out:
                if 0 <= index_box < nbr_levels_AI_1:
                    write_on_line(
                        text_options[1],
                        var.color_player_1,
                        var.width_screen,
                        boxes_levels[1][0].top,
                    )
                    diff_AI_1 = index_box
                elif nbr_levels_AI_1 <= index_box < len(options_levels):
                    write_on_line(
                        text_options[2],
                        var.color_player_2,
                        var.width_screen,
                        boxes_levels[2][0].top,
                    )
                    diff_AI_2 = index_box % nbr_levels_AI_1
                if diff_AI_1 != -1 and diff_AI_2 != -1:
                    play_box = draw_agreement_box("Sarah Connor ?")
                highlight_box(
                    options_levels[index_box],
                    var.color_options_highlight_box,
                    f"Level {index_box % nbr_levels_AI_1}",
                    var.color_options_highlight_text,
                )
            elif play_box is not None and x_in_rect(play_box, mouse_click):
                box_clicked = var.boxAI_play
            else:
                play_box = None
                diff_AI_1 = -1
                diff_AI_2 = -1
                cancel_box, quit_box = reset_screen(
                    var.color_options_screen, text_options, colors
                )
            pg.display.update()
    return (diff_AI_1, diff_AI_2)


def show_options_AI(number: int) -> None:
    """Show the options for the AIs according to the number given"""

    assert 0 < number < 3, f"number can not be something other than 1 or 2"

    var.screen.fill(var.color_options_screen)
    texts_level = []
    for i in range(len(var.boxAI_text_levels)):
        texts_level.append(create_text_rendered(f"Level {i}"))
    text_difficulty_options = [
        "",
        var.text_options_difficulty_HvAI,
        var.text_options_difficulty_AIvAI,
    ]
    text_diff = create_text_rendered(text_difficulty_options[number])
    text_options = [[text_diff], texts_level]

    if number == 1:
        var.symbol_player_AI, var.difficulty_AI_2 = options_1AI(text_options)
    elif number == 2:
        text_options.append(texts_level)
        var.difficulty_AI_1, var.difficulty_AI_2 = options_2AI(text_options)
