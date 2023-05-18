#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time

import libai

nbr_test = 100
max_depth = 14
compiler = input("Compiler: ")
id_test = input("Id: ")
for depth in range(1, max_depth + 1):
    t = 0
    for i in range(1, nbr_test):
        g = libai.Game()
        start = time()
        trash = g.aiMove(depth)
        end = time()
        t += end - start
        print(f"{depth:3d}: {i}", end="\r")
    print(f"{depth:3d}: done, it took {t:21.12f} seconds ({g.get_count():10d} nodes visited)")
    fp = open("result.csv", "a")
    fp.write(
        f"{depth:5d}, {compiler:>25s}, {nbr_test:10d}, {t/nbr_test:15.10f}, {id_test:>10s}\n"
    )
    fp.close()
