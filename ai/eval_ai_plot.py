#!/usr/bin/python3
# -*- coding: utf-8 -*-

import libai
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

ai1_winning = 1
ai2_winning = -1
ai1_ai2_draw = 0


def test_for_plot(depth_ai1, depth_ai2):
    i = depth_ai1
    j = depth_ai2
    ai1 = libai.Game()
    ai2 = libai.Game()
    print(f"Doing {i:02d} vs {j:02d}", end="\r")
    k = 1
    while not (ai1.ai_winning() or ai1.human_winning() or ai1.draw()):
        ai1_m = ai1.aiMove(i)
        ai2.humanMove(ai1_m)
        k += 1
        print(f"Doing {i:02d} vs {j:02d}, move nbr {k:02d}", end="\r")
        if ai1.ai_winning():
            break
        ai2_m = ai2.aiMove(j)
        ai1.humanMove(ai2_m)
        k += 1
        print(f"Doing {i:02d} vs {j:02d}, move nbr {k:02d}", end="\r")
    if ai1.ai_winning():
        result = ai1_winning
    elif ai1.human_winning():
        result = ai2_winning
    else:
        result = ai1_ai2_draw
    print(f"{i:02d} {j:02d} are done", " "* 20, end="\r")
    return result


def plot_result(x, y, tableau):
    # We can change color, but we have to use the one at https://matplotlib.org/stable/_images/sphx_glr_named_colors_003.png
    cmap = mpl.colors.ListedColormap(["blueviolet", "royalblue", "yellowgreen"])
    plt.pcolormesh(x, y, tableau, edgecolors="w", cmap=cmap)

    # Legend
    plt.xlabel("Depth first player")
    plt.ylabel("Depth second player")
    cbar = plt.colorbar(ticks=[-0.70, 0, 0.70])
    cbar.ax.set_yticklabels(["2 win", "Draw", "1 win"])

    plt.savefig("test_1.png")
    plt.close()


max_level = 17
tableau = np.zeros((max_level, max_level))
x = np.linspace(1, max_level, max_level)
y = np.linspace(1, max_level, max_level)

# for i in range(max_level):
#     for j in range(max_level):
#         tableau[j, i] = test_for_plot(i + 1, j + 1)
#         plot_result(x, y, tableau)
