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
    ai1 = libai.Game()
    ai2 = libai.Game()
    while not (ai1.ai_winning() or ai1.human_winning() or ai1.draw()):
        ai1_m = ai1.aiMove(depth_ai1)
        ai2.humanMove(ai1_m)
        if ai1.ai_winning():
            break
        ai2_m = ai2.aiMove(depth_ai2)
        ai1.humanMove(ai2_m)
    if ai1.ai_winning():
        result = ai1_winning
    elif ai1.human_winning():
        result = ai2_winning
    else:
        result = ai1_ai2_draw
    print(f"{i+1:2d} {j+1:2d} are done", end="\r")
    return result

max_level = 13
tableau = np.zeros((max_level, max_level))
x = np.linspace(1, max_level, max_level)
y = np.linspace(1, max_level, max_level)

for i in range(max_level):
    for j in range(max_level):
        tableau[j, i] = test_for_plot(i+1, j+1)

# We can change color, but we have to use the one at https://matplotlib.org/stable/_images/sphx_glr_named_colors_003.png
cmap = mpl.colors.ListedColormap(["blueviolet", "royalblue", "yellowgreen"])
plt.pcolormesh(x, y, tableau, edgecolors="w", cmap=cmap)

# Legend
plt.xlabel("Depth first player")
plt.ylabel("Depth second player")
cbar = plt.colorbar(ticks=[-0.70, 0, 0.70])
cbar.ax.set_yticklabels(["2 win", "Draw", "1 win"])

plt.savefig("result_1.png")
