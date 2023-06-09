#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any, Iterator, Optional

import numpy as np

from core.utils import Symbol, opponent
from core.variables import Variables


class Board(np.ndarray[Any, np.dtype[Any]]):
    """The Board class contains the state of the board"""

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
        """Return if the symbol passed has won the game"""
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
        """Return if the column we want to play in is not full"""
        return self[0, col] == Variables().symbol_no_player

    def list_valid_col(self) -> list[int]:
        """liste des colonnes où l'on peut jouer"""
        possible_col = [3, 4, 2, 5, 1, 6, 0]
        valid_col = []
        for col in possible_col:
            if self.is_valid_col(col):
                valid_col.append(col)
        return valid_col
