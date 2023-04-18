#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai

nb_parties = 1000
depth_ai1 = 4
depth_ai2 = 2
nb_win_ai1 = 0
nb_win_ai2 = 0
nb_draw = 0

for k in range(nb_parties):
    print(f"{k}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, (draw = {nb_draw})", end="\r")
    ai1 = libai.Game()
    ai2 = libai.Game()
    i = 0
    while not (ai1.ai_winning() or ai1.human_winning() or ai1.draw()):
        ai1_m = ai1.aiMove(depth_ai1)
        ai2.humanMove(ai1_m)
        ai2_m = ai2.aiMove(depth_ai2)
        ai1.humanMove(ai2_m)
        i+= 1
        # print(ai1.printBoard())
    if ai1.ai_winning():
        nb_win_ai1 += 1
    elif ai2.ai_winning():
        nb_win_ai2 += 1
    else:
        nb_draw += 1
print(nb_parties)
print("AI_1 won %i times" %nb_win_ai1)