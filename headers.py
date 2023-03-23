#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Any, Callable, Optional, Iterator

import numpy as np
import pygame as pg
from playsound import playsound

from minimax_ai import *
from gesture import *
from variables import Symbol, Variables

pg.init()

Color = pg.Color
Rect = pg.Rect
Surface = pg.Surface

class Symbol:
    """The Symbol class is used to make the difference between two players"""

    def __init__(self, value: Any) -> None:
        raise NotImplementedError

    def __eq__(self, o: object) -> Any:
        raise NotImplementedError

class Variables:
    def __init__(self) -> None:
        raise NotImplementedError
    
class Node:
    pass
class Board:
    pass

class Config:
    def __init__(self, var: Variables, arguments) -> None:
        raise NotImplementedError

    def load_language(self, language: str) -> None:
        raise NotImplementedError

class Element:
    """An element is composed of a box and text"""

    def __init__(
        self,
        var: Variables,
        pos: tuple[int, int],
        text: str,
        screen: Surface,
        text_color: Color = Variables().black,
        box_color: Color = Variables().color_options_box,
        font: pg.font.Font = Variables().main_font,
        padd: tuple[int, int] = (
            Variables().text_box_spacing,
            Variables().text_box_spacing,
        ),
    ) -> None:
        raise NotImplementedError

    def draw(self, text: str) -> None:
        raise NotImplementedError

class Tools:
    def __init__(
        self, var: Variables, screen: Surface, volume: bool, camera: bool
    ) -> None:
        raise NotImplementedError

    def compute_total_size(
        self, array_text: list[list[Surface]]
    ) -> tuple[int, list[int]]:
        """Compute the height of a list of line of texts and the width of each line"""
        raise NotImplementedError

    def write_text_box(
        self,
        text: Surface,
        color_box: Color,
        x: int,
        y: int,
        spacing_x: int = Variables().text_box_spacing,
        spacing_y: int = Variables().text_box_spacing,
    ) -> Rect:
        """Write the text and create the box arround it"""
        raise NotImplementedError

    def write_on_line(
        self,
        list_text: list[Surface],
        color_box: Color,
        x: int,
        y: int,
        align: int = 0,
        space_x: int = Variables().text_box_spacing,
        space_y: int = Variables().text_box_spacing,
        space_box: int = Variables().options_spacing,
    ) -> list[Rect]:
        raise NotImplementedError

    def center_all(
        self,
        array_text: list[list[Surface]],
        color_box: list[Color] = [Variables().color_options_box],
    ) -> list[list[Rect]]:
        """Write the texts in 'array_text' centered in the middle of the screen.
        If 'color_box' is a single element, then all boxes will have the same color"""
        raise NotImplementedError

    def create_text_rendered(
        self,
        text: str,
        color: Color = Variables().color_options_text,
        font: str = Variables().text_font,
        size: int = Variables().text_size,
    ) -> Surface:
        """Create text in the color, font, and size asked"""
        raise NotImplementedError

    def highlight_box(
        self, box: Rect, color_box: Color, screen: Surface, text: str, color_text: Color
    ) -> None:
        """Highlight the clicked box to be in a color or another"""
        raise NotImplementedError

    def draw_agreement_box(self, text: str, position: float = 0.75) -> Rect:
        """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
        raise NotImplementedError

    def make_icon(self, image: str, size: np.ndarray[Any, np.dtype[Any]]) -> Surface:
        raise NotImplementedError

    def draw_icon(self, image: str, size: np.ndarray[Any, np.dtype[Any]], position: tuple[int, int]) -> Rect:
        raise NotImplementedError
    
class Screen(Tools):
    """A screen is composed of what is shown to the user"""

    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
        cancel_box: bool = True,
        quit_box: bool = True,
        color_fill: Color = Variables().color_options_screen,
    ) -> None:
        raise NotImplementedError

    def draw_cancel_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        raise NotImplementedError

    def draw_quit_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        raise NotImplementedError

    def reset_screen(
        self,
        color_screen: Color,
        text: list[list[Surface]],
        colors_boxes: list[Color],
    ) -> None:
        raise NotImplementedError

    def get_mouse_pos(self) -> tuple[int, int]:
        """Return the mouse position"""
        raise NotImplementedError

    def human_move(self, color: Color) -> None:
        raise NotImplementedError

    def update_gesture(self, image: str) -> None:
        raise NotImplementedError
    
    def click(
        self,
        rect_play: Optional[Rect] = None,
        sound: str = Variables().sound_click_box,
        print_disk: bool = False,
        color_disk: Color = Variables().white,
    ) -> tuple[int, int]:
        """Quit the function only when there is a click. Return the position of the click.
        If f is not None, then the function is called whith the argument 'event' at every iteration"""
        raise NotImplementedError

    def is_canceled(self, click: tuple[int, int]) -> bool:
        raise NotImplementedError

    def handle_quit(self, click: tuple[int, int]) -> None:
        """Function to call when wanting to see if user clicked in the quitting box"""
        raise NotImplementedError

    def x_in_rect(
        self,
        coor: tuple[int, int],
        rect: Optional[Rect],
        sound: str = Variables().sound_click_box,
    ) -> bool:
        """Return whether coor is in the rectangle 'rect'"""
        raise NotImplementedError

    def handle_click(self, click_coor: tuple[int, int], list_rect: list[Rect]) -> int:
        """Return the index of the box the click was in"""
        raise NotImplementedError
        
class Screen_AI(Screen):
    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
        number_AI: int = 1,
    ) -> None:
        raise NotImplementedError

    def screen_loop(self) -> None:
        raise NotImplementedError

class OptionsScreen(Screen):
    def __init__(
        self,
        var: Variables,
        game,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
    ):
        raise NotImplementedError

    def reset_screen(self):
        raise NotImplementedError
    
    def dfites(self, testing: bool, position: float, first_image: str, second_image: str) -> Any:
        raise NotImplementedError

    def draw_vol_cam(self) -> tuple[Any, Any]: 
        raise NotImplementedError

    def draw_language(self):
        raise NotImplementedError


class GamingScreen(Screen):
    """The gaming screen is used for the gaming part of the program"""

    def __init__(
        self,
        var: Variables,
        screen: Surface,
        gesture: GestureController,
        volume: bool,
        camera: bool,
    ) -> None:
        raise NotImplementedError

    def draw_circle(self, n: int, m: int, color: Color, r: int) -> None:
        """Draw a circle in the corresponding column, and row"""
        raise NotImplementedError

    def blit_board(self) -> None:
        raise NotImplementedError

    def draw_board(self) -> None:
        raise NotImplementedError

    def animate_fall(self, col: int, row: int, color_player: Color) -> None:
        raise NotImplementedError

class Node:
    def __init__(self, move: int, parent, symbol: Symbol, depth: int, nbr:int = 0) -> None:
        raise NotImplementedError

    def is_terminal(self) -> bool:
       raise NotImplementedError
    
    def remove_old_root(self) -> Node:
        raise NotImplementedError

    def add_child(self, column: int) -> Node:
        raise NotImplementedError

    def get_board_state(self) -> Board:
        raise NotImplementedError

    def compute_score(self) -> None:
        raise NotImplementedError

    def copy(self) -> Node:
        raise NotImplementedError

    def create_tree(self, depth: int) -> None:
        raise NotImplementedError
    
class Board(np.ndarray[Any, np.dtype[Any]]):
    def __new__(cls: np.ndarray[Any, np.dtype[Any]]) -> Any:
        raise NotImplementedError

    def find_free_slot(self, i: int) -> int:
        """Return the index of the first free slot"""
        raise NotImplementedError

    def state_to_bits(self) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        raise NotImplementedError

    def state_win(self, symbol: Symbol) -> bool:
        raise NotImplementedError

    def horiz(self, row: int, col: int) -> Iterator:
        raise NotImplementedError

    def vert(self, row: int, col: int) -> Iterator:
        raise NotImplementedError

    def backslash(self, row: int, col: int, back = True) -> Iterator:
        raise NotImplementedError

    def slash(self, row: int, col: int) -> Iterator:
        raise NotImplementedError

    def is_valid_col(self, col: int):
        raise NotImplementedError

    def list_valid_col(self):
        raise NotImplementedError
    
class Player:
    """The class that keep all the options for a player"""

    def __init__(
        self, var: Variables, number: int, AI: bool, difficulty: int = -1
    ) -> None:
        raise NotImplementedError

    def play(self, board: Board, root: Node, screen: Screen, volume: bool) -> tuple[int, int, Node]:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError
    
class Game:
    """The big class that will regulate everything"""

    def __init__(self, var: Variables, args) -> None:
        raise NotImplementedError

    def inverse_player(self) -> None:
        """Return the symbols of the opponent of the player currently playing"""
        raise NotImplementedError

    def who_is_winner(self) -> Player:
        raise NotImplementedError

    def start(self) -> None:
        raise NotImplementedError

    def start_game(self) -> None:
        raise NotImplementedError

    def draw_winner(self, screen: GamingScreen, lastclick: tuple[int, int]) -> None:
        raise NotImplementedError

    def draw_options_screen(self) -> None:
        raise NotImplementedError

    def draw_play_options(self) -> None:
        """Show the different options when choosing to play"""
        raise NotImplementedError

    def draw_start_screen(self) -> None:
        """Show the start screen.
        For now it is only the play button but soon there will be more options"""
        raise NotImplementedError