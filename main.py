#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import variables as var
from interface import *
from variables import Rect, pg
from gesture import GestureController
import threading
# Run the game loop forever
def game_loop():
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


status = start_screen()
start_game()
quit_box = draw_quit_box()
gc1 = GestureController()
thread1 = threading.Thread(target=gc1.start)
thread1.start()

thread2 = threading.Thread(target=game_loop)
thread2.start()


