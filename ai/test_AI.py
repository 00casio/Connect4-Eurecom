#!/usr/bin/python3
# -*- coding: utf-8 -*-

from libai import Game
import time

def do_game(game: str, expec_score: int, num: int, ai_game: Game) -> tuple[float, int]:
    human = len(game) % 2
    for move in game:
        if human:
            ai_game.humanMove(int(move) - 1)
        else:
            ai_game.forceAIMove(int(move) - 1)
        human = not human
    start = time.time()
    score = ai_game.scoreAIpos()
    end = time.time()
    if score != expec_score:
        print(f"{game}, found {score}, expected {expec_score}")
    # assert score == expec_score, f"test number {num} ({score} != {expec_score})"
    return (end-start, ai_game.get_count())


def tests(file: str):
    with open(f"tests/{file}", "r") as f:
        lines = f.read().split("\n")[:-1]
    i = 1
    ai_game = Game()
    total_time = 0
    total_pos = 0
    for i in range(len(lines)):
        l = lines[i]
    # for l in lines:
        # if i not in [240]:
        #     continue
        game, expected_score = l.split(" ")[0], int(l.split(" ")[1])
        t, pos = do_game(game, expected_score, i, ai_game)
        total_time += t
        total_pos += pos
        print(f"{i} in {(t):.9f}s", end="\r")
        ai_game.resetBoard()
    print(f"mean time: {total_time/len(lines):.9f}s, mean nb pos: {total_pos/len(lines):.5f}")

tests("Test_L3_R1") # End-Easy
tests("Test_L2_R1") # Middle-Easy
tests("Test_L2_R2") # Middle-Medium
tests("Test_L1_R1") # Begin-Easy
tests("Test_L1_R2") # Begin-Medium
tests("Test_L1_R3") # Begin-Hard
