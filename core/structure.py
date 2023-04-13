#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any, Iterator, Optional

import numpy as np

from core.utils import Symbol, opponent
from core.variables import Variables


class Board(np.ndarray[Any, np.dtype[Any]]):
    def __new__(cls: np.ndarray[Any, np.dtype[Any]]) -> Any:
        self = np.array([[Variables().symbol_no_player] * 7 for i in range(6)]).view(
            cls
        )
        self.state = None
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

    def is_valid_col(
        self, col: int
    ) -> bool:  # on regarde si la colonne est pleine ou pas
        return self[0, col] == Variables().symbol_no_player

    def list_valid_col(self) -> list[int]:  # liste des colonnes où l'on peut jouer
        possible_col = [3, 4, 2, 5, 1, 6, 0]
        valid_col = []
        for col in possible_col:
            if self.is_valid_col(col):
                valid_col.append(col)
        return valid_col


class Node_H:
    def __init__(self):
        self.column_played = -1
        self.parent = None
        self.symbol_player = Symbol(Variables().symbol_no_player)
        self.board = None
        self.score = None
        self.children = []
        self.depth = -1
        self.nbr_move = 0

    def is_terminal(self) -> bool:
        raise NotImplementedError()

    def create_tree(self, depth: int) -> None:
        raise NotImplementedError()


class Node(Node_H):
    def __init__(
        self,
        move: int,
        parent: Optional[Node_H],
        symbol: Symbol,
        depth: int,
        nbr: int = 0,
    ) -> None:
        super().__init__()
        self.column_played = move
        self.parent = parent
        self.symbol_player = symbol
        self.depth = depth
        self.nbr_move = nbr

    def is_terminal(self) -> bool:
        return self.children == []

    def remove_old_root(self) -> Node_H:
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

    def add_child(self, column: int) -> Node_H:
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

    def copy(self) -> Node_H:
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
