import numpy as np


def f(i):
    if i in range(10):
        return f"0{i}"
    return f"{i}"


board = np.array([[f(j) for j in range(i, i + 7)] for i in range(1, 43, 7)])
print(board)

row = 5
col = 3
print(f"board[{row}, {col}] = {board[row, col]}")
