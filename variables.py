#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Symbols
no_player = "0"
player_1 = "1"
player_2 = "2"

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_trans = (0, 0, 0, 0)
color_player_1 = red
color_player_2 = green
color_board = blue
color_screen = white

# Size
size_cell = 100
padding = size_cell
width_board = 7*size_cell
height_board = 6*size_cell
radius_disk = 40
width_screen = 2*padding + width_board
height_screen = 2*padding + height_board

# Pygame
fps = 30
screen_title = "Connect 4"
