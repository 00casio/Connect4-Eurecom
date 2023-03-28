#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any, Iterator, Optional
from utils import Symbol, opponent
import numpy as np
from headers import Node
from variables import Variables


class Board(np.ndarray[Any, np.dtype[Any]]):
    def __new__(cls: np.ndarray[Any, np.dtype[Any]]) -> Any:
        self = np.array([[Variables().symbol_no_player] * 7 for i in range(6)]).view(
            cls
        )
        self.state: Optional[np.ndarray[np.uint8, np.dtype[np.uint8]]] = None
        return self

    def find_free_slot(self, i: int) -> int:
        """Return the index of the first free slot"""
        col = self[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == Variables().symbol_no_player:
                return j
        return -1

    def state_to_bits(self) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        n = "0b"
        for j in range(len(self.state[0]) - 1, -1, -1):
            n += "0"
            for i in range(len(self.state)):
                n += f"{int(self.state[i, j])}"  # <==> n += str(b)
        return n

    def state_win(self, symbol: Symbol) -> bool:
        self.state = np.zeros(self.shape, dtype=np.uint8)
        self.state[np.where(self == symbol)] = 1
        bits = int(self.state_to_bits(), 2)

        # Horizontal check
        m = bits & (bits >> 7)
        if m & (m >> 14):
            return True
        # Vertical
        m = bits & (bits >> 1)
        if m & (m >> 2):
            return True
        # Diagonal \
        m = bits & (bits >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = bits & (bits >> 8)
        if m & (m >> 16):
            return True
        # Nothing found
        return False

    def horiz(self, row: int, col: int) -> Iterator[list[Any]]:
        for i in range(max(0, col - 3), min(7, col + 1)):
            if len(self[row, i : i + 4]) == 4:
                yield self[row, i : i + 4]

    def vert(self, row: int, col: int) -> Iterator[list[Any]]:
        for i in range(max(0, row - 3), min(7, row + 1)):
            if len(self[i : i + 4, col]) == 4:
                yield self[i : i + 4, col]

    def backslash(self, row: int, col: int, back=True) -> Iterator[list[Any]]:
        if back:
            board = self.copy()
        else:
            board = np.fliplr(self.copy())
        i, j = row, col
        while i > max(0, row - 3) and j > max(0, col - 3):
            i -= 1
            j -= 1

        while i < min(7, row + 1) and j < min(7, col + 1):
            if i >= 3 or j >= 4:
                break
            yield [board[i + k, j + k] for k in range(4)]
            i += 1
            j += 1

    def slash(self, row: int, col: int) -> Iterator:
        yield from self.backslash(row, col[3 - (col - 3)], back=False)

    def is_valid_col(self, col: int) -> bool:  # on regarde si la colonne est pleine ou pas
        return self[0, col] == Variables().symbol_no_player

    def list_valid_col(self) -> list[int]:  # liste des colonnes où l'on peut jouer
        possible_col = [3, 4, 2, 5, 1, 6, 0]
        valid_col = []
        for col in possible_col:
            if self.is_valid_col(col):
                valid_col.append(col)
        return valid_col


class Node:
    def __init__(
        self, move: int, parent: Optional[Node], symbol: Symbol, depth: int, nbr: int = 0
    ) -> None:
        self.column_played = move
        self.parent = parent
        self.symbol_player = symbol
        self.board: Board = None
        self.score: int = None
        self.children: list[Node] = []
        self.depth = depth
        self.nbr_move = nbr

    def is_terminal(self) -> bool:
        return self.children == []

    def remove_old_root(self) -> None:
        self.depth -= 1
        if self.depth == 0:
            self.board = self.parent.get_board_state()
            self.board[
                self.board.find_free_slot(self.column_played), self.column_played
            ] = self.symbol_player
            self.parent = None
        for child in self.children:
            child.remove_old_root()
        return self

    def add_child(self, column: int) -> Node:
        child = Node(
            column,
            self,
            opponent(self.symbol_player),
            self.depth + 1,
            self.nbr_move + 1,
        )
        self.children.append(child)
        return child

    def get_board_state(self) -> Board:
        board = self.board
        if self.parent is not None:
            board = self.parent.get_board_state().copy()
            board[
                board.find_free_slot(self.column_played), self.column_played
            ] = self.symbol_player
        return board

    def compute_score(self) -> None:
        board = self.get_board_state()
        self.score = score_board(board, self.symbol_player)

    def copy(self) -> Node:
        node = Node(
            self.column_played,
            self.parent,
            self.symbol_player,
            self.depth,
            self.nbr_move,
        )
        node.board = self.board
        node.children = self.children
        node.score = self.score
        return node

    def create_tree(self, depth: int) -> None:
        if depth == 0:
            return
        board = self.get_board_state()
        for col in board.list_valid_col():
            # if col in [c.column_played for c in self.children]:
            #     child = self.children[col]
            # else:
            child = self.add_child(col)
            child.create_tree(depth - 1)
