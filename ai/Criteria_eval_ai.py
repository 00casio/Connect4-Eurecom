#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai

nb_parties = 100
depth_ai1 = 3
depth_ai2 = 3
nb_win_ai1 = 0
nb_win_ai2 = 0
nb_draw = 0

ai1 = libai.Game()
ai2 = libai.Game()
nb_win_ai1 = 0
nb_win_ai2 = 0
nb_draw = 0
for k in range(nb_parties):
    print(f"{k}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, (draw = {nb_draw})", end="\r")
    ai1.resetBoard()
    ai2.resetBoard()
    i = 0
    while not (ai1.ai_winning() or ai1.human_winning() or ai1.draw()):
        ai1_m = ai1.aiMove(depth_ai1)
        ai2.humanMove(ai1_m)
        if ai1.ai_winning():
            break
        ai2_m = ai2.aiMove(depth_ai2)
        ai1.humanMove(ai2_m)
        i+= 1
        # print(ai1.printBoard())
    assert ai1.ai_winning() == ai2.human_winning(), "WRONG WRONG WRONG WRONG WRONG WRONG"
    assert ai2.ai_winning() == ai1.human_winning(), "WRONG WRONG WRONG WRONG WRONG WRONG"
    if ai1.ai_winning():
        nb_win_ai1 += 1
    elif ai1.human_winning():
        nb_win_ai2 += 1
    else:
        nb_draw += 1
print(f"{nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, (draw = {nb_draw})")
percentage_win_AI_1 =  nb_parties/(nb_win_ai2 + nb_draw)

of = open("criteria_AI.txt", "a")
of.write("Criteria judged : Testing if AI at given level wins against lower level AI opponent\n")
of.write("AI_1 is depth %d while AI_2 is depth %d. AI_1 starts the game\n" % (depth_ai1, depth_ai2))
of.write(f"{nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, draw = {nb_draw}), percentage win AI_1 = {percentage_win_AI_1})\n \n")
of.close()

def tests_criteria(nb_parties, depth_ai1, depth_ai2):
    nb_win_ai1 = 0
    nb_win_ai2 = 0
    nb_draw = 0

    ai1 = libai.Game()
    ai2 = libai.Game()
    nb_win_ai1 = 0
    nb_win_ai2 = 0
    nb_draw = 0
    for k in range(nb_parties):
        print(f"{k}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, (draw = {nb_draw})", end="\r")
        ai1.resetBoard()
        ai2.resetBoard()
        i = 0
        while not (ai1.ai_winning() or ai1.human_winning() or ai1.draw()):
            ai1_m = ai1.aiMove(depth_ai1)
            ai2.humanMove(ai1_m)
            if ai1.ai_winning():
                break
            ai2_m = ai2.aiMove(depth_ai2)
            ai1.humanMove(ai2_m)
            i+= 1
            # print(ai1.printBoard())
        assert ai1.ai_winning() == ai2.human_winning(), "WRONG WRONG WRONG WRONG WRONG WRONG"
        assert ai2.ai_winning() == ai1.human_winning(), "WRONG WRONG WRONG WRONG WRONG WRONG"
        if ai1.ai_winning():
            nb_win_ai1 += 1
        elif ai1.human_winning():
            nb_win_ai2 += 1
        else:
            nb_draw += 1
    print(f"{nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, (draw = {nb_draw})")
    percentage_win_AI_1 =  nb_parties/(nb_win_ai2 + nb_draw)

    of = open("criteria_AI.txt", "a")
    of.write("Criteria judged : Testing if AI at given level wins against lower level AI opponent\n")
    of.write("AI_1 is depth %d while AI_2 is depth %d. AI_1 starts the game\n" % (depth_ai1, depth_ai2))
    of.write(f"Nb_games = {nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, draw = {nb_draw}), percentage win AI_1 = {percentage_win_AI_1})\n \n")
    of.close()