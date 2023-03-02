#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from typing import Any, Callable, Optional

import numpy as np
import pygame as pg

from AI_test import best_col_prediction
from variables import Symbol, Variables

var = Variables()
pg.init()

Color = pg.Color
Rect = pg.Rect
Surface = pg.Surface


class Element:
    """An element is composed of a box and text"""

    def __init__(
        self,
        pos: tuple[int, int],
        text: str,
        screen: Surface,
        text_color: Color = var.black,
        box_color: Color = var.color_options_box,
        font: pg.font.Font = var.main_font,
        padd: tuple[int, int] = (var.text_box_spacing, var.text_box_spacing),
    ) -> None:
        self.font = font
        self.pos = pos
        self.text_color = text_color
        self.color_box = box_color
        self.screen = screen
        self.padding = padd
        self.draw(text)

    def draw(self, text: str) -> None:
        self.text = self.font.render(text, True, self.text_color)
        s = self.text.get_size()
        self.box = Rect(
            self.pos[0],
            self.pos[1],
            s[0] + 2 * self.padding[0],
            s[1] + 2 * self.padding[1],
        )
        pg.draw.rect(self.screen, self.color_box, self.box)
        self.screen.blit(self.text, (self.box.x, self.box.y))
        pg.display.update(self.box)


class Tools:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen

    def compute_total_size(
        self, array_text: list[list[Surface]]
    ) -> tuple[int, list[int]]:
        """Compute the height of a list of line of texts and the width of each line"""
        total_height = 0
        total_width = []
        for line_text in array_text:
            total_height += (
                max([t.get_size()[1] for t in line_text]) + 2 * var.text_box_spacing
            )
            width_now = (
                sum([t.get_size()[0] for t in line_text])
                + 2 * var.text_box_spacing * len(line_text)
                + (len(line_text) - 1) * var.options_spacing
            )
            total_width.append(width_now)
        total_height += (len(array_text) - 1) * var.options_spacing
        return (total_height, total_width)

    def write_text_box(
        self,
        text: Surface,
        color_box: Color,
        x: int,
        y: int,
        spacing_x: int = var.text_box_spacing,
        spacing_y: int = var.text_box_spacing,
    ) -> Rect:
        """Write the text and create the box arround it"""
        size = text.get_size()
        b_rect = Rect(x, y, size[0] + 2 * spacing_x, size[1] + 2 * spacing_y)
        pg.draw.rect(self.screen, color_box, b_rect)
        self.screen.blit(text, (x + spacing_x, y + spacing_y))
        return b_rect

    def write_on_line(
        self,
        list_text: list[Surface],
        color_box: Color,
        x: int,
        y: int,
        align: int = 0,
        space_x: int = var.text_box_spacing,
        space_y: int = var.text_box_spacing,
        space_box: int = var.options_spacing,
    ) -> list[Rect]:
        """write 'list_text' on a single line. 'align' can take -1 for left, 0 for middle, and 1 for right"""
        boxes = []
        width_line = self.compute_total_size([list_text])[1][0]
        if align == -1:
            write_x = x
        elif align == 0:
            write_x = (x - width_line) // 2
        elif align == 1:
            write_x = x - width_line
        else:
            raise ValueError("align is not -1, 0, or 1. Correct this")
        for text in list_text:
            boxes.append(
                self.write_text_box(text, color_box, write_x, y, space_x, space_y)
            )
            write_x += text.get_size()[0] + 2 * space_x + space_box
        # pg.display.update()
        return boxes

    def center_all(
        self,
        array_text: list[list[Surface]],
        color_box: list[Color] = [var.color_options_box],
    ) -> list[list[Rect]]:
        """Write the texts in 'array_text' centered in the middle of the screen.
        If 'color_box' is a single element, then all boxes will have the same color"""

        color = [color_box[-1]] * (len(array_text) - len(color_box)) + color_box
        total_size = self.compute_total_size(array_text)
        rect_boxes = []
        y_now = (var.height_screen - total_size[0]) // 2
        for i in range(len(array_text)):
            line_text = array_text[i]
            box_rect = self.write_on_line(line_text, color[i], var.width_screen, y_now)
            y_now += (
                line_text[0].get_size()[1]
                + 2 * var.text_box_spacing
                + var.options_spacing
            )
            rect_boxes.append(box_rect)
        pg.display.update()
        return rect_boxes

    def create_text_rendered(
        self,
        text: str,
        color: Color = var.color_options_text,
        font: str = var.text_font,
        size: int = var.text_size,
    ) -> Surface:
        """Create text in the color, font, and size asked"""
        pg_font = pg.font.SysFont(font, size)
        return pg_font.render(text, True, color)

    def highlight_box(
        self, box: Rect, color_box: Color, screen: Surface, text: str, color_text: Color
    ) -> None:
        """Highlight the clicked box to be in a color or another"""
        pg_text = self.create_text_rendered(text, color_text)
        pg.draw.rect(screen, color_box, box)
        screen.blit(
            pg_text, (box.x + var.text_box_spacing, box.y + var.text_box_spacing)
        )
        pg.display.update()

    def draw_agreement_box(self, text: str, position: float = 0.75) -> Rect:
        """Draw a agreement box in the center of the screen at position (in %) of the height of the screen"""
        agreement = self.create_text_rendered(text, var.black)
        s = agreement.get_size()
        x = (var.width_screen - s[0]) // 2 - var.text_box_spacing
        y = int(position * var.height_screen)
        box = self.write_text_box(agreement, var.color_screen, x, y)
        pg.display.update()
        return box


class Screen(Tools):
    """A screen is composed of what is shown to the user"""

    def __init__(
        self,
        screen: Surface,
        cancel_box: bool = True,
        quit_box: bool = True,
        color_fill: Color = var.color_options_screen,
    ) -> None:
        Tools.__init__(self, screen)
        self.elements: list[Element] = []
        self.cancel_box: Optional[Rect] = None
        self.box_clicked = var.box_out
        self.screen.fill(color_fill)
        if cancel_box:
            self.draw_cancel_box()
        if quit_box:
            self.draw_quit_box()

    def draw_cancel_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        cancel = self.create_text_rendered(var.text_cancel_box, var.black)
        self.cancel_box = self.write_on_line(
            [cancel],
            var.white,
            var.coor_cancel_box[0],
            var.coor_cancel_box[1],
            align=-1,
        )[0]

    def draw_quit_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        quit_t = self.create_text_rendered(var.text_quit_box, var.black)
        self.quit_box = self.write_on_line(
            [quit_t], var.white, var.coor_quit_box[0], var.coor_quit_box[1], align=1
        )[0]

    def reset_screen(
        self,
        color_screen: Color,
        text: list[list[Surface]],
        colors_boxes: list[Color],
    ) -> None:
        self.screen.fill(color_screen)
        self.center_all(text, colors_boxes)
        self.draw_cancel_box()
        self.draw_quit_box()
        pg.display.update()

    def get_mouse_pos(self) -> tuple[int, int]:
        """Return the mouse position"""
        # print("Change this to have the position from the camera")
        return pg.mouse.get_pos()

    def human_move(self, color: Color) -> None:
        self.screen.fill(var.color_screen)
        mouse_x, mouse_y = self.get_mouse_pos()
        if mouse_x < var.pos_min_x:
            mouse_x = var.pos_min_x
        elif mouse_x > var.pos_max_x:
            mouse_x = var.pos_max_x

        p = var.padding
        if p < mouse_x < p + var.width_board:
            col = (mouse_x - p) // var.size_cell
            rect_col = Rect(p + col * var.size_cell, 0, var.size_cell, p)
            pg.draw.rect(self.screen, var.color_highlight_column, rect_col)
        self.draw_quit_box()
        pg.draw.circle(self.screen, color, (mouse_x, p // 2), var.radius_disk)
        pg.display.update((mouse_x - p // 2, 0, p, p))

    def click(
        self,
        rect_play: Optional[Rect] = None,
        print_disk: bool = False,
        color_disk: Color = var.white,
    ) -> tuple[int, int]:
        """Quit the function only when there is a click. Return the position of the click.
        If f is not None, then the function is called whith the argument 'event' at every iteration"""
        allow_quit = False
        while not allow_quit:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    allow_quit = True
                if print_disk:
                    self.human_move(color_disk)
        click = self.get_mouse_pos()
        if self.is_canceled(click):
            self.box_clicked = var.boxAI_cancel
        self.handle_quit(click)
        if rect_play is not None:
            while not self.x_in_rect(click, rect_play):
                click = self.click(rect_play, print_disk, color_disk)
        return click

    def is_canceled(self, click: tuple[int, int]) -> bool:
        if self.cancel_box is None:
            return False
        return self.x_in_rect(click, self.cancel_box)

    def handle_quit(self, click: tuple[int, int]) -> None:
        """Function to call when wanting to see if user clicked in the quitting box"""
        if self.quit_box is not None and self.x_in_rect(click, self.quit_box):
            print("You choose to quit the game\nYou are disapointing me")
            pg.quit()
            sys.exit()

    def x_in_rect(self, coor: tuple[int, int], rect: Optional[Rect]) -> bool:
        """Return whether coor is in the rectangle 'rect'"""
        if rect is None:
            return False
        return rect.left <= coor[0] <= rect.right and rect.top <= coor[1] <= rect.bottom

    def handle_click(self, click_coor: tuple[int, int], list_rect: list[Rect]) -> int:
        """Return the index of the box the click was in"""
        for i in range(len(list_rect)):
            if self.x_in_rect(click_coor, list_rect[i]):
                return i
        return -1


class Screen_AI(Screen):
    def __init__(self, screen: Surface, number_AI: int = 1) -> None:
        Screen.__init__(self, screen)
        self.number_AI = number_AI

        texts_level = [
            self.create_text_rendered(f"Level {i}")
            for i in range(len(var.boxAI_text_levels))
        ]

        self.text_options = [
            [self.create_text_rendered(var.text_difficulty_options[number_AI])],
            texts_level,
        ]
        self.options_colors = [var.color_options_box, var.color_player_1]
        if self.number_AI == 2:
            self.options_colors.append(var.color_player_2)
        self.boxes_levels = self.center_all(self.text_options, self.options_colors)
        self.play_box: Optional[Rect] = None
        self.diff_AI_1, self.diff_AI_2 = -1, -1
        self.nbr_levels_AI_1 = len(self.boxes_levels[1])
        if self.number_AI == 2:
            self.text_options.append(texts_level)
            self.boxes_levels = self.center_all(self.text_options, self.options_colors)
            self.options_levels = [*self.boxes_levels[1], *self.boxes_levels[2]]
        else:
            self.options_levels = [*self.boxes_levels[1]]
        self.reset_screen(
            var.color_options_screen, self.text_options, self.options_colors
        )
        self.screen_loop()

    def screen_loop(self) -> None:
        while self.box_clicked not in [var.boxAI_play, var.boxAI_cancel]:
            mouse_click = self.click()
            index_box = self.handle_click(mouse_click, self.options_levels)
            print(index_box)
            if index_box != -1:
                if 0 <= index_box < self.nbr_levels_AI_1:
                    self.write_on_line(
                        self.text_options[1],
                        var.color_player_1,
                        var.width_screen,
                        self.boxes_levels[1][0].top,
                    )
                    self.diff_AI_1 = index_box
                elif self.nbr_levels_AI_1 <= index_box < len(self.options_levels):
                    self.write_on_line(
                        self.text_options[2],
                        var.color_player_2,
                        var.width_screen,
                        self.boxes_levels[2][0].top,
                    )
                    self.diff_AI_2 = index_box % self.nbr_levels_AI_1
                if self.diff_AI_1 != -1 and (
                    self.diff_AI_2 != -1 or self.number_AI == 1
                ):
                    self.play_box = self.draw_agreement_box("Sarah Connor ?")
                self.highlight_box(
                    self.options_levels[index_box],
                    var.color_options_highlight_box,
                    self.screen,
                    f"Level {index_box % self.nbr_levels_AI_1}",
                    var.color_options_highlight_text,
                )
            elif self.play_box is not None and self.x_in_rect(
                mouse_click, self.play_box
            ):
                self.box_clicked = var.boxAI_play
            else:
                self.play_box = None
                self.diff_AI_1 = -1
                self.diff_AI_2 = -1
                self.reset_screen(
                    var.color_options_screen, self.text_options, self.options_colors
                )
                pg.display.update()


class GamingScreen(Screen):
    """The gaming screen is used for the gaming part of the program"""

    def __init__(self, screen: Surface) -> None:
        Screen.__init__(self, screen)
        self.color_screen = var.white
        self.color_board = var.blue
        self.width_board = var.width_board
        self.height_board = var.height_board
        self.board_surface = Surface(
            (self.width_board, self.height_board)
        ).convert_alpha()

    def draw_circle(self, n: int, m: int, color: Color, r: int) -> None:
        """Draw a circle in the corresponding column, and row"""
        x = n * var.size_cell + var.size_cell // 2
        y = m * var.size_cell + var.size_cell // 2
        pg.draw.circle(self.board_surface, color, (x, y), r)

    def blit_board(self) -> None:
        self.screen.blit(self.board_surface, (var.padding, var.padding))
        self.draw_quit_box()

    def draw_board(self) -> None:
        self.screen.fill(self.color_screen)
        pg.draw.rect(
            self.board_surface,
            self.color_board,
            (0, 0, self.width_board, self.height_board),
        )
        for i in range(7):
            for j in range(6):
                self.draw_circle(i, j, var.color_trans, var.radius_hole)
        self.blit_board()
        pg.display.update()

    def animate_fall(self, col: int, row: int, color_player: Color) -> None:
        x = var.padding + col * var.size_cell + var.size_cell // 2
        for y in range(
            var.padding // 2, var.padding + row * var.size_cell + var.size_cell // 2, 5
        ):
            self.screen.fill(var.white)
            pg.draw.circle(self.screen, color_player, (x, y), var.radius_disk)
            self.blit_board()
            pg.display.update()
        self.draw_circle(col, row, color_player, var.radius_hole)


class Board(np.ndarray[Any, np.dtype[Any]]):
    def __new__(cls: np.ndarray[Any, np.dtype[Any]]) -> Any:
        self = np.array([[var.symbol_no_player] * 7 for i in range(6)]).view(cls)
        return self

    def find_free_slot(self, i: int) -> int:
        """Return the index of the first free slot"""
        col = self[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == var.symbol_no_player:
                return j
        return -1


class Player:
    """The class that keep all the options for a player"""

    def __init__(self, number: int, AI: bool, difficulty: int = -1) -> None:
        if number == 0:
            self.symbol = Symbol(var.symbol_no_player)
            self.color = var.color_trans
        elif number == 1:
            self.symbol = Symbol(var.symbol_player_1)
            self.color = var.color_player_1
        elif number == 2:
            self.symbol = Symbol(var.symbol_player_2)
            self.color = var.color_player_2
        else:
            raise ValueError("There can not be more than 2 players")
        self.is_ai = AI
        self.ai_difficulty = difficulty

    def play(self, board: Board, screen: Screen) -> tuple[int, int]:
        if self.is_ai:
            col = best_col_prediction(board, self.symbol)
        else:
            p = var.padding
            box_allowed = Rect(p, p, var.width_board, var.height_board)
            click = screen.click(box_allowed, print_disk=True, color_disk=self.color)
            col = (click[0] - var.padding) // var.size_cell
        row = board.find_free_slot(col)
        if row == -1:
            col, row = self.play(board, screen)
        return (col, row)

    def __eq__(self, other: object) -> bool:
        eq: bool = False
        if isinstance(other, Player):
            eq = self.symbol == other.symbol
        elif isinstance(other, Symbol):
            eq = self.symbol == other
        return eq


class Game:
    """The big class that will regulate everything"""

    def __init__(self) -> None:
        # Players
        self.player_1 = Player(1, False)
        self.player_2 = Player(2, False)
        self.player_playing = self.player_1
        self.player_null = Player(0, False)
        self.screen = pg.display.set_mode((var.width_screen, var.height_screen), 0, 32)
        pg.display.set_caption(var.screen_title)

    def inverse_player(self) -> None:
        """Return the symbols of the opponent of the player currently playing"""
        if self.player_playing == self.player_1:
            self.player_playing = self.player_2
        elif self.player_playing == self.player_2:
            self.player_playing = self.player_1
        else:
            raise ValueError(
                "How is that possible ? Read carefully the error and send me everything"
            )

    def state_to_bits(self, state: np.ndarray[np.uint8, np.dtype[np.uint8]]) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        n = "0b"
        for j in range(len(state[0]) - 1, -1, -1):
            n += "0"
            for i in range(len(state)):
                n += f"{int(state[i, j])}"  # <==> n += str(b)
        return n

    def state_win(self, state: np.ndarray[Any, np.dtype[Any]]) -> bool:
        bits = int(self.state_to_bits(state), 2)

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

    def who_is_winner(self) -> Player:
        s = self.board.shape
        state_symbol_player_1 = np.zeros(s, dtype=np.uint8)
        state_symbol_player_2 = np.zeros(s, dtype=np.uint8)
        state_symbol_player_1[np.where(self.board == self.player_1.symbol)] = 1
        state_symbol_player_2[np.where(self.board == self.player_2.symbol)] = 1
        if self.state_win(state_symbol_player_1):
            return self.player_1
        elif self.state_win(state_symbol_player_2):
            return self.player_2
        else:
            return self.player_null

    def draw_winner(self) -> None:
        winner = self.who_is_winner()
        if winner == self.player_1:
            print("Winner is the first player")
        elif winner == self.player_2:
            print("Winner is the second player")
        else:
            print("That is a draw")
        print("Not finished")

    def start(self) -> None:
        self.draw_start_screen()
        self.board = Board()
        self.CLOCK = pg.time.Clock()
        self.num_turn = 0
        self.start_game()

    def start_game(self) -> None:
        gaming = GamingScreen(self.screen)
        gaming.draw_board()
        self.player_playing = self.player_1
        while (
            self.who_is_winner() == self.player_null and self.num_turn < self.board.size
        ):
            if self.player_playing == self.player_1:
                play = self.player_1.play(self.board, gaming)
            else:
                play = self.player_2.play(self.board, gaming)
            gaming.animate_fall(play[0], play[1], self.player_playing.color)
            self.board[play[1], play[0]] = self.player_playing.symbol.v
            self.inverse_player()
            self.num_turn += 1
        self.draw_winner()

    def draw_options_screen(self) -> None:
        raise NotImplementedError("Not for now")

    def draw_play_options(self) -> None:
        """Show the different options when choosing to play"""
        screen = Screen(self.screen)
        text_HvH = screen.create_text_rendered(var.text_options_play_HvH)
        text_HvAI = screen.create_text_rendered(var.text_options_play_HvAI)
        text_AIvAI = screen.create_text_rendered(var.text_options_play_AIvAI)
        text_options = [[text_HvH], [text_HvAI], [text_AIvAI]]
        boxes = screen.center_all(text_options)
        self.status = var.options_menu_play
        self.screen_AI = None
        while self.status == var.options_menu_play:
            mouse = screen.click()
            if screen.x_in_rect(mouse, boxes[0][0]):
                self.status = var.options_play_HvH
            elif screen.x_in_rect(mouse, boxes[1][0]):
                self.status = var.options_play_HvAI
                self.screen_AI = Screen_AI(self.screen, number_AI=1)
                self.player_2 = Player(2, True, self.screen_AI.diff_AI_1)
            elif screen.x_in_rect(mouse, boxes[2][0]):
                self.status = var.options_play_AIvAI
                self.screen_AI = Screen_AI(self.screen, number_AI=2)
                self.player_1 = Player(1, True, self.screen_AI.diff_AI_1)
                self.player_2 = Player(2, True, self.screen_AI.diff_AI_2)
            elif screen.x_in_rect(mouse, screen.cancel_box):
                self.status = var.options_clicked_cancel
        if self.player_2.ai_difficulty == -1 and self.status not in [
            var.options_play_HvH,
            var.options_clicked_cancel,
        ]:
            self.draw_play_options()

    def draw_start_screen(self) -> None:
        """Show the start screen.
        For now it is only the play button but soon there will be more options"""

        start_screen = Screen(self.screen, cancel_box=False)
        text_play = start_screen.create_text_rendered(var.text_options_play)
        boxes_options = start_screen.center_all([[text_play]])
        rect_play = boxes_options[0][0]
        self.status = var.options_menu_start
        while self.status == var.options_menu_start:
            mouse = start_screen.click()
            if start_screen.x_in_rect(mouse, rect_play):
                self.draw_play_options()
        if self.status == var.options_clicked_cancel:
            self.draw_start_screen()
