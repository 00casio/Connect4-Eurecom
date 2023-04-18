#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai

nb_parties = 100
depth_ai1 = 4
depth_ai2 = 3
nb_win_ai1 = 0


for k in range(nb_parties):
    print(k, end="\r")
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
        nb_win_ai1+=1
    print("%i %i" %(k, i))
print(nb_parties)
print("AI_1 won %i times" %nb_win_ai1)