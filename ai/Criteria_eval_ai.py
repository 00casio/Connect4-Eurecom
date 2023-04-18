#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai

nb_parties = 100
depth_ai1 = 3
depth_ai2 = 5
nb_win_ai1 = 0

for k in range(nb_parties):
    ai1 = libai.Game()
    ai2 = libai.Game()
    while not ai1.ai_winning() or not ai1.human_winning() or ai1.draw() != -1:
        ai1_m = ai1.aiMove(depth_ai1)
        ai2.humanMove(ai1_m)
        ai2_m = ai2.aiMove(depth_ai2)
        ai1.humanMove(ai2_m)
    if ai1.ai_winning():
        nb_win_ai1+=1
print(nb_win_ai1)
