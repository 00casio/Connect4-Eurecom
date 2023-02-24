#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from interface import *
from variables import *

status = start_screen()
start_game()

# Run the game loop forever
quit_box = draw_quit_box()
while True:
    for event in pg.event.get():
        winner = gaming(event)
        if winner != symbol_no_player or event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONUP:
            handle_quit(quit_box, pg.mouse.get_pos())
    quit_box = draw_quit_box()
    update_screen(Rect(0, 0, width_board + padding, width_screen))
    CLOCK.tick(fps)
