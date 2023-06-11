#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time

import libai
import matplotlib.pyplot as plt

write = False
plot = False

nbr_test = 100
max_depth = 18
compiler = input("Compiler: ")
id_test = input("Id: ")
for depth in range(1, max_depth + 1):
    total_t = []
    if 0 <= depth < 13:
        nbr_test = 100
    if depth == 13:
        nbr_test = 50
    if depth >= 14:
        nbr_test = 10
    if depth >= 16:
        nbr_test = 2
    for i in range(1, nbr_test+1):
        g = libai.Game()
        start = time()
        trash = g.aiMove(depth)
        end = time()
        total_t.append(end - start)
        if depth >= 7 or i % 25 == 0:
            print(f"{depth:3d}: {i}", end="\r")
    t = sum(total_t)
    print(
        f"{depth:3d}: done, it took {t/nbr_test:21.12f} seconds ({g.get_count():10d} nodes visited)"
    )
    if write:
        with open("benchmark_result.csv", "a") as fp:
            fp.write(
                f"{depth:5d}, {compiler:>25s}, {nbr_test:10d}, {t/nbr_test:15.10f}, {id_test:>10s}\n"
            )
    if plot:
        plt.hist(total_t, bins=100)
        plt.savefig(f"bench_hists/{id_test}_{depth}.png")
        plt.close()
