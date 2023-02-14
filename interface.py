#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
import sys

import numpy as np
import pygame as pg

from variables import *

# Board
board = np.array(
    [[no_player] * 7, [no_player] * 7, [no_player] * 7, [no_player] * 7, [no_player] * 7, [no_player] * 7]
)

# initializing pygame window
pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width_screen, height_screen), 0, 32)
pg.display.set_caption(screen_title)
board_surface = pg.surface.Surface((width_board, height_board)).convert_alpha()

def update_screen(rect=None, pause=0):
    screen.blit(board_surface, (padding, padding))
    if rect is not None:
        pg.display.update(rect)
    else:
        pg.display.update()
    sleep(pause)

def draw_circle(n, m):
    x = n*size_cell + size_cell//2
    y = m*size_cell + size_cell//2
    pg.draw.circle(board_surface, color_trans, (x, y), radius_disk)

def start_game():
    screen.fill(color_screen)
    pg.draw.rect(board_surface, color_board, (0, 0, width_board, height_board))
    for i in range(7):
        for j in range(6):
            draw_circle(i, j)
    update_screen()

start_game()
playing = player_1
color_playing = color_player_1

# Run the game loop forever
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            # Inverse player
            if playing == player_1:
                playing = player_2
                color_playing = color_player_2
            else:
                playing = player_1
                color_playing = color_player_1

        mouse_x, mouse_y = pg.mouse.get_pos()
        if mouse_x < pos_min_x:
            mouse_x = pos_min_x
        elif mouse_x > pos_max_x:
            mouse_x = pos_max_x
        screen.fill(color_screen)
        pg.draw.circle(screen, color_playing, (mouse_x, padding//2), radius_disk)
    update_screen()
    CLOCK.tick(fps)

"""
def draw_status():
    global draw, winner, player

    if winner is None:
        message = player.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game Draw!"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(W / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global Board, winner, draw, player

    # check for winning rows
    for row in range(0, 6):
        ligne = Board[row, :]
        for col in range(0, 4):
            if ligne[col] is not None:
                if ligne[col] == ligne[col + 1] == ligne[col + 2] == ligne[col + 3]:
                    winner = player
                    pg.draw.line(
                        screen,
                        (0, 255, 0),
                        (col * j_w + j_w / 2, row * j_h + j_h / 2),
                        ((col + 3) * j_w + j_w / 2, row * j_h + j_h / 2),
                        10,
                    )
                    break

    # check for winning columns
    for col in range(0, 7):
        column = Board[:, col]
        for row in range(0, 3):
            if column[row] is not None:
                if column[row] == column[row + 1] == column[row + 2] == column[row + 3]:
                    winner = player
                    pg.draw.line(
                        screen,
                        (0, 255, 0),
                        (col * j_w + j_w / 2, row * j_h + j_h / 2),
                        (col * j_w + j_w / 2, (row + 3) * j_h + j_h / 2),
                        10,
                    )
                    break

    # check for winning diagonals
    for row in range(3, 6):
        for col in range(0, 4):
            if Board[row, col] is not None:
                if (
                    Board[row, col]
                    == Board[row + 1, col]
                    == Board[row + 2, col]
                    == Board[row + 2, col]
                ):
                    pg.draw.line(screen, (0, 255, 0), (0, H), (W, 0), 20)
                    break

    pg.display.update()


def drawXO(row, col):
    global Board, player

    posx = j_w * (row) + 5
    posy = j_h * (col) + 5
    Board[row][col] = player

    if player == "red":
        screen.blit(r_img, (posy, posx))
        player = "blue"
    else:
        screen.blit(b_img, (posy, posx))
        player = "red"
    pg.display.update()

    # print(posx, posy)
    # print(Board)


def userClick():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column (0-6) and row (0-5) of mouse click
    col = int(x // j_w)
    row = int(y // j_h)
    # print(row, col)

    if Board[row][col] is None:
        global player
        # draw the jeton on screen
        drawXO(row, col)
        check_win()


def reset_game():
    global Board, winner, player, draw
    time.sleep(3)
    player = "red"
    draw = False
    winner = None
    Board = np.array(
        [[None] * 7, [None] * 7, [None] * 7, [None] * 7, [None] * 7, [None] * 7]
    )
    game_opening()
"""
