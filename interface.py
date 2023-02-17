#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

import pygame as pg

from scores import who_is_winner
from variables import *


def compute_total_size(list_text):
    total_size = 0
    for text in list_text:
        total_size += 2 * text_box_spacing
        if type(text) == list:
            total_size += max([t.get_size()[1] for t in text])
        else:
            total_size += text.get_size()[1]
    return total_size + (len(list_text) - 1) * options_spacing


def write_same_line(list_text, y, color_box):
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
    if type(text) == list:
        new_y, box_rect = write_same_line(text, y_now, color_box)
    else:
        new_y, box_rect = write_same_line([text], y_now, color_box)
        box_rect = box_rect[0]
    return new_y, box_rect


def center_all(list_text, color_box=color_options_box):
    if type(color_box) == list:
        assert len(list_text) == len(
            color_box
        ), f"list_text and color_box are not the same size ({len(list_text)} and {len(color_box)})"
    total_size = compute_total_size(list_text)
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


def x_in_rect(rect, coor):
    return (
        rect[0] <= coor[0] <= rect[0] + rect[2]
        and rect[1] <= coor[1] <= rect[1] + rect[3]
    )


def create_options_text(text, color=color_options_text):
    font = pg.font.SysFont(text_font, text_size)
    return font.render(text, 1, color)


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


def options_1AI(text_options):
    boxes_levels = center_all(text_options)
    box_clicked = boxAI_out
    play_box = None
    while box_clicked != boxAI_play:
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONUP:
                continue
            screen.fill(color_options_screen)
            center_all(text_options)
            mouse_click = pg.mouse.get_pos()
            index_box = handle_click(mouse_click, boxes_levels[1])
            if index_box != boxAI_out:
                highlight_clicked_box(
                    boxes_levels[1][index_box],
                    index_box,
                    color_options_highlight_box,
                    color_options_highlight_text,
                )
                play_box = draw_agreement_box(boxAI_text_levels[index_box])
                difficulty_AI = index_box
            elif play_box is not None and x_in_rect(play_box, mouse_click):
                box_clicked = boxAI_play
            else:
                play_box = None
                pg.display.update()
    return symbol_player_2, difficulty_AI


def options_2AI(text_options):
    colors = [color_options_box, color_player_1, color_player_2]
    boxes_levels = center_all(text_options, colors)
    box_clicked = boxAI_out
    play_box = None
    diff_AI_1, diff_AI_2 = None, None
    options_levels = [*boxes_levels[1], *boxes_levels[2]]
    nbr_levels_AI_1 = len(boxes_levels[1])
    while box_clicked != boxAI_play:
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONUP:
                continue
            mouse_click = pg.mouse.get_pos()
            index_box = handle_click(mouse_click, options_levels)
            if index_box != boxAI_out:
                if 0 <= index_box < nbr_levels_AI_1:
                    write_same_line(
                        text_options[1], boxes_levels[1][0][1], color_player_1
                    )
                    diff_AI_1 = index_box
                elif nbr_levels_AI_1 <= index_box < len(options_levels):
                    write_same_line(
                        text_options[2], boxes_levels[2][0][1], color_player_2
                    )
                    diff_AI_2 = index_box % nbr_levels_AI_1
                if diff_AI_1 is not None and diff_AI_2 is not None:
                    play_box = draw_agreement_box("Sarah Connor ?")
                highlight_clicked_box(
                    options_levels[index_box],
                    index_box % nbr_levels_AI_1,
                    color_options_highlight_box,
                    color_options_highlight_text,
                )
            elif play_box is not None and x_in_rect(play_box, mouse_click):
                box_clicked = boxAI_play
            else:
                play_box = None
                diff_AI_1 = None
                diff_AI_2 = None
                screen.fill(color_options_screen)
                center_all(text_options, colors)
            pg.display.update()
    return diff_AI_1, diff_AI_2


def show_options_AI(number):
    global player_AI, difficulty_AI_1, difficulty_AI_2

    screen.fill(color_options_screen)
    texts_level = []
    for i in range(len(boxAI_text_levels)):
        texts_level.append(create_options_text(f"Level {i}"))
    text_difficulty_options = [
        "",
        text_options_difficulty_HvAI,
        text_options_difficulty_AIvAI,
    ]
    text_diff = create_options_text(text_difficulty_options[number])
    text_options = [text_diff, texts_level]

    if number == 1:
        player_AI, difficulty_AI_1 = options_1AI(text_options)
    elif number == 2:
        text_options.append(texts_level)
        difficulty_AI_1, difficulty_AI_2 = options_2AI(text_options)


def show_options_play():
    screen.fill(color_options_screen)
    text_HvH = create_options_text(text_options_play_HvH)
    text_HvAI = create_options_text(text_options_play_HvAI)
    text_AIvAI = create_options_text(text_options_play_AIvAI)
    boxes = center_all([text_HvH, text_HvAI, text_AIvAI])
    status = options_menu_play
    while status == options_menu_play:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(boxes[0], mouse):
                    status = options_play_HvH
                if x_in_rect(boxes[1], mouse):
                    status = options_play_HvAI
                    show_options_AI(1)
                if x_in_rect(boxes[2], mouse):
                    status = options_play_AIvAI
                    show_options_AI(2)
    return status


def start_screen():
    screen.fill(color_options_screen)
    text_play = create_options_text(text_options_play)
    boxes_options = center_all([text_play])
    rect_play = boxes_options[0]
    status = options_menu_start
    while status == options_menu_start:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                if x_in_rect(rect_play, mouse):
                    status = show_options_play()
    return status


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


def start_game():
    screen.fill(color_screen)
    pg.draw.rect(board_surface, color_board, (0, 0, width_board, height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j, color_trans, radius_hole)
    update_screen()


def inverse_player(symbol_playing):
    if symbol_playing == symbol_player_1:
        symbol_playing = symbol_player_2
        color_playing = color_player_2
    else:
        symbol_playing = symbol_player_1
        color_playing = color_player_1
    return symbol_playing, color_playing


def find_low_bound(i):
    col = board[:, i]
    for j in range(len(col) - 1, -1, -1):
        if col[j] == symbol_no_player:
            return j
    return -1


def click(player, color, pos_click_x):
    global board

    num_col = pos_click_x // size_cell
    i = find_low_bound(num_col)
    if i == -1:
        return player, color
    board[i, num_col] = player
    x = padding + num_col * size_cell + size_cell // 2
    for y in range(padding // 2, padding + i * size_cell + padding // 2, 5):
        screen.fill(white)
        pg.draw.circle(screen, color, (x, y), radius_disk)
        update_screen()
    draw_circle(num_col, i, color, radius_hole)
    return inverse_player(symbol_playing)


def gaming(event):
    global symbol_playing, color_playing, num_turn

    winner = symbol_no_player
    if event.type == pg.MOUSEBUTTONUP:
        pos_click = pg.mouse.get_pos()
        if padding < pos_click[0] < width_board + padding:
            symbol_playing, color_playing = click(
                symbol_playing, color_playing, pos_click[0] - padding
            )
            num_turn += 1
            winner = who_is_winner(board)
            if winner == symbol_player_1:
                print("Winner is player 1")
            elif winner == symbol_player_2:
                print("Player 2 won this match")
            elif num_turn == nbr_max_turn:
                winner = symbol_draw
                print("It's a draw")

    if winner == symbol_no_player:
        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x < pos_min_x:
            mouse_x = pos_min_x
        elif mouse_x > pos_max_x:
            mouse_x = pos_max_x
        screen.fill(color_screen)
        pg.draw.circle(screen, color_playing, (mouse_x, padding // 2), radius_disk)
    return winner
