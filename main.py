#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from interface import *
import variables as var

pg = var.pg

status = start_screen()
start_game()

quit_box = draw_quit_box()
# Run the game loop forever
while True:
    for event in pg.event.get():
        winner = gaming(event)
        if winner != var.symbol_no_player or event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONUP:
            handle_quit(quit_box, pg.mouse.get_pos())
    quit_box = draw_quit_box()
    update_screen(Rect(0, 0, var.width_board + var.padding, var.width_screen))
    var.CLOCK.tick(var.fps)
