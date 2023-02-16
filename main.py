#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import pygame as pg

from interface import *
from variables import *

start_screen()
start_game()

# Run the game loop forever
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        gaming(event)
    update_screen((0, 0, padding, width_screen))
    CLOCK.tick(fps)
