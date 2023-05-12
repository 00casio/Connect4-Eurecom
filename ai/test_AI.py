#!/usr/bin/python3
# -*- coding: utf-8 -*-

from libai import Game
import time


def tests(file: str):
    with open(f"tests/{file}", "r") as f:
        lines = f.read().split("\n")[:-1]

    libai = Game()

    i = 1
    total_time = 0
    total_pos = 0
    for l in lines:
        game, expected_score = l.split(" ")[0], int(l.split(" ")[1])
        # print(expected_score)
        human = (len(game) % 2)
        for move in game:
            if human:
                libai.humanMove(int(move)-1)
            else:
                libai.forceAIMove(int(move)-1)
            human = not human
        start = time.time()
        score = libai.scoreAIpos()
        end = time.time()
        assert score == expected_score, f"{score}, {expected_score}"
        total_pos += libai.get_count()
        total_time += end-start
        print(f"{i} in {end-start:.5f} s", end="\r")
        i += 1
        libai.resetBoard()
    print(f"mean time: {total_time/len(lines):.9f}s, mean nb pos: {total_pos/len(lines):.5f}")

tests("Test_L3_R1") # End-Easy
tests("Test_L2_R1") # Middle-Easy
tests("Test_L2_R2") # Middle-Medium
tests("Test_L1_R1") # Begin-Easy
tests("Test_L1_R2") # Begin-Medium
tests("Test_L1_R3") # Begin-Hard
