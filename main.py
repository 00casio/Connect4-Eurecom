#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from interface import *
from variables import *

status = start_screen()
start_game()

# Run the game loop forever
while True:
    for event in pg.event.get():
        winner = gaming(event)
        if winner != symbol_no_player:
            pg.quit()
            sys.exit()
    update_screen((0, 0, padding, width_screen))
    CLOCK.tick(fps)
