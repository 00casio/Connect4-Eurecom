#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai
import random
import time

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
            # ai2_m = random.choice([0, 1, 2, 3, 4, 5, 6])
            ai1.humanMove(ai2_m)
            i+= 1       
        if ai1.ai_winning():
            nb_win_ai1 += 1
        elif ai1.human_winning():
            nb_win_ai2 += 1
        else:
            nb_draw += 1
    print(f"{nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, draw = {nb_draw}")
    percentage_win_AI_1 = (100*nb_win_ai1)/nb_parties
    print("percentage winning AI 1 : ", percentage_win_AI_1)

    of = open("criteria_AI.txt", "a")

    #of.write("Criteria judged : Testing if AI at given level wins against lower level AI opponent\n")
    of.write("Criteria judged : Testing if, when AI 1 plays first, it wins against same level AI opponent \n")
    #of.write("Criteria judged : Testing if AI wins at any depth against a random player \n")

    #of.write(f"AI_1 is depth {depth_ai1} and is playing against random player")
    of.write(f"AI_1 is depth {depth_ai1} while AI_2 is depth {depth_ai2}. AI_1 starts the game\n")
    of.write(f"Nb_games = {nb_parties}: AI_1 = {nb_win_ai1}, AI_2 = {nb_win_ai2}, draw = {nb_draw}, percentage win AI_1 = {percentage_win_AI_1:.2f}\n \n")
    of.close()

tests_criteria(1000, 1, 1)
tests_criteria(1000, 3, 3)
tests_criteria(1000, 5, 5)
#tests_criteria(100, 6, 6) # beggining of weird stats, AI 2 wins most of the time
tests_criteria(100, 7, 7) # AI 2 is always winning here, this is stange
#tests_criteria(50, 8, 8)
tests_criteria(50, 9, 9) # my computer is too slow for this one, but seems like the same as the previous one

# tests_criteria(1000, 1, 1)
# tests_criteria(1000, 3, 1)
# tests_criteria(1000, 5, 1)
# tests_criteria(500, 7, 1)
# tests_criteria(50, 9, 1)


# tests_criteria(1000, 5, 3)
# tests_criteria(500, 7, 3)
# #tests_criteria(50, 9, 3)
# tests_criteria(500, 7, 5)
# tests_criteria(100, 9, 7)
