#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai
from time import time

nbr_test = 100
nbr_depth = 11
compiler = input("Compiler: ")
id_test = input("Id: ")
for depth in range(1, nbr_depth+1):
    t = 0
    for i in range(1, nbr_test):
        g = libai.Game()
        start = time()
        g.aiMove(depth)
        end = time()
        t += end - start
        print(f"{depth:2d}: {i}", end="\r")
    print(f"{depth:2d}: done, it took {t} seconds ({g.count()} nodes visited)")
    fp = open("result.csv", "a")
    fp.write(f"{depth:5d}, {compiler:>25s}, {nbr_test:10d}, {t/nbr_test:15f}, {id_test:>10s}\n")
    fp.close()
