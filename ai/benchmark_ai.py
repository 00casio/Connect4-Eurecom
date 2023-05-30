#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time

import libai
import matplotlib.pyplot as plt

write = False
plot = True

nbr_test = 10000
max_depth = 13
compiler = input("Compiler: ")
id_test = input("Id: ")
for depth in range(1, max_depth + 1):
    total_t = []
    for i in range(1, nbr_test):
        g = libai.Game()
        start = time()
        trash = g.aiMove(depth)
        end = time()
        total_t.append(end - start)
        if depth >= 7 or i % 25 == 0:
            print(f"{depth:3d}: {i}", end="\r")
    t = sum(total_t)
    print(
        f"{depth:3d}: done, it took {t:21.12f} seconds ({g.get_count():10d} nodes visited)"
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
