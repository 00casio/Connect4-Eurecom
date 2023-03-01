#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Any

import numpy as np
import pygame as pg

from AI_test import best_col_prediction
from variables import Variables

var = Variables()
pg.init()


class Symbol:
    """The Symbol class is used to make the difference between two players"""

    def __init__(self, value: Any) -> None:
        self.v = value

    def __eq__(self, o: object) -> Any:
        if not isinstance(o, Symbol):
            return NotImplemented
        return o.v == self.v


class Element:
    """An element is composed of a box and text"""

    def __init__(
        self,
        pos: tuple[int, int],
        text: str,
        screen: pg.Surface,
        text_color: pg.Color = var.black,
        box_color: pg.Color = var.color_options_box,
        font: pg.font.Font = var.main_font,
        padd: tuple[int, int] = (var.text_box_spacing, var.text_box_spacing),
    ) -> None:
        self.font = font
        self.pos = pos
        self.color_box = color_box
        self.screen = screen
        self.padding = (padd_x, padd_y)
        self.draw(text)

    def draw(self, text: str) -> None:
        self.text = self.font.render(text, True, self.text_color)
        s = self.text.get_size()
        self.box = pg.Rect(
            self.pos[0],
            self.pos[1],
            s[0] + 2 * self.padding[0],
            s[1] + 2 * self.padding[1],
        )
        pg.draw.rect(self.screen, self.color_box, self.box)
        self.screen.blit(self.text, (self.box.x, self.box.y))
        self.screen.update(self.box)


class Tools:
    def compute_total_size(
        self, array_text: list[list[pg.Surface]]
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
        text: pg.Surface,
        color_box: pg.Color,
        x: int,
        y: int,
        spacing_x: int = var.text_box_spacing,
        spacing_y: int = var.text_box_spacing,
    ) -> pg.Rect:
        """Write the text and create the box arround it"""
        size = text.get_size()
        b_rect = pg.Rect(x, y, size[0] + 2 * spacing_x, size[1] + 2 * spacing_y)
        pg.draw.rect(var.screen, color_box, b_rect)
        var.screen.blit(text, (x + spacing_x, y + spacing_y))
        return b_rect

    def write_on_line(
        self,
        list_text: list[pg.Surface],
        color_box: pg.Color,
        x: int,
        y: int,
        align: int = 0,
        space_x: int = var.text_box_spacing,
        space_y: int = var.text_box_spacing,
        space_box: int = var.options_spacing,
    ) -> list[pg.Rect]:
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

    def write_on_column(
        list_text: list[Surface],
        color_box: Color,
        x: int,
        y: int,
        align: int = 0,
        space_x: int = var.text_box_spacing,
        space_y: int = var.text_box_spacing,
        space_box: int = var.options_spacing,
    ) -> list[Rect]:
        boxes = []
        height_line = compute_total_size([list_text])[0]
        if align == -1:
            write_y = y
        elif align == 0:
            write_y = (y - height_line) // 2
        elif align == 1:
            write_y = y - height_line
        else:
            raise ValueError("align is not -1, 0, or 1. Correct this")
        for text in list_text:
            boxes.append(write_text_box(text, color_box, x, write_y))
            write_y += text.get_size()[1] + 2 * space_y + space_box
        # pg.display.update()
        return boxes

    def center_all(
        array_text: list[list[pg.Surface]],
        color_box: pg.Color | list[pg.Color] = var.color_options_box,
    ) -> list[list[pg.Rect]]:
        """Write the texts in 'array_text' centered in the middle of the screen.
        If 'color_box' is a single element, then all boxes will have the same color"""
        if type(color_box) == list:
            assert len(array_text) == len(
                color_box
            ), f"array_text and color_box are not the same size ({len(array_text)} and {len(color_box)})"
        total_size = compute_total_size(array_text)
        rect_boxes = []
        y_now = (var.height_screen - total_size[0]) // 2
        for i in range(len(array_text)):
            line_text = array_text[i]
            if type(color_box) == list:
                color = color_box[i]
            else:
                color = color_box
            box_rect = write_on_line(line_text, color, var.width_screen, y_now)
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


class Screen(Tools):
    """A screen is composed of what is shown to the user"""

    def __init__(
        self,
        screen,
        width: int,
        height: int,
        cancel_box: bool = True,
        quit_box: bool = True,
        color_fill: pg.Color = var.color_options_screen,
    ):
        self.screen = screen
        self.width = width
        self.height = height
        self.elements = []
        self.screen = None
        self.cancel_box = None
        self.suit_box = None
        self.screen.fill(color_fill)
        if cancel_box:
            self.draw_cancel_box()
        if quit_box:
            self.draw_quit_box()

    def draw_cancel_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        cancel = self.create_text_rendered(var.text_cancel_box, var.black)
        self.cancel_box = self.write_on_line(
            [cancel], var.white, *var.coor_cancel_box, align=-1
        )[0]

    def draw_quit_box(self) -> None:
        """Draw the box that allow the user to take a step back"""
        quit_t = self.create_text_rendered(var.text_quit_box, var.black)
        self.quit_box = self.write_on_line(
            [quit_t], var.white, *var.coor_quit_box, align=1
        )[0]

    def reset_screen(self,
        color_screen: pg.Color, text: list[list[pg.Surface]], colors_boxes: pg.Color | list[pg.Color]
    ) -> tuple[pg.Rect, pg.Rect]:
        self.screen.fill(color_screen)
        self.center_all(text, colors_boxes)
        self.draw_cancel_box(), self.draw_quit_box()
        pg.display.update()

    def get_mouse_pos(self):
        raise NotImplementedError("Not for now")
        """ Return the mouse position if conditions are met """
        return pg.mouse.get_pos()

    def x_in_rect(self, rect: pg.Rect, coor: tuple[int, int]) -> bool:
        """Return whether coor is in the rectangle 'rect'"""
        return rect.left <= coor[0] <= rect.right and rect.top <= coor[1] <= rect.bottom

    def handle_click(
        self, click_coor: tuple[int, int], list_rect: list[pg.Rect]
    ) -> int:
        """Return the index of the box the click was in"""
        for i in range(len(list_rect)):
            if self.x_in_rect(list_rect[i], click_coor):
                return i
        return -1

class Screen_AI(Screen):
    def __init__(self, screen, width, height, texts, colors):
        Screen.__init__(self, screen, width, height)
        boxes_levels = self.center_all(texts, colors)


class GamingScreen(Screen):
    """The gaming screen is used for the gaming part of the program"""

    def __init__(self, screen: pg.Surface, width: int, height: int) -> None:
        Screen.__init__(self, screen, width, height)
        self.color_screen = var.white
        self.color_board = var.light_blue
        self.width_board = var.width_board
        self.height_board = var.height_board
        self.board_surface = pg.surface.Surface(
            (self.width_board, self.height_board)
        ).convert_alpha()

    def draw_board():
        self.screen.fill(self.color_screen)
        pg.draw.rect(
            self.board_surface,
            self.color_board,
            (0, 0, self.width_board, self.height_board),
        )
        for i in range(7):
            for j in range(6):
                draw_circle(i, j, var.color_trans, var.radius_hole)
        update_screen()

    def find_free_slot(self, board, i: int) -> int:
        """Return the index of the first free slot"""
        col = board[:, i]
        for j in range(len(col) - 1, -1, -1):
            if col[j] == var.symbol_no_player:
                return j
        return -1

    def animate_fall(self, col: int, row: int, color_player: pg.Color) -> None:
        for y in range(var.padding + num_col * var.size_cell + var.size_cell // 2, 5):
            self.screen.fill(var.white)
            pg.draw.circle(self.screen, color_player, (x, y), var.radius_disk)
            update_screen()
        pg.draw.circle(self.board_surface, color, (x, y), var.radius_hole)

    def player_move(self, board, col: int) -> None:
        row = find_free_slot(board)
        self.animate_fall()
        raise NotImplementedError("Not finished")


class Player:
    """The class that keep all the options for a player"""

    def __init__(self, symbol: Any, color: pg.Color, AI: bool):
        self.symbol = Symbol(symbol)
        self.color = color
        self.is_ai = AI
        self.ai_difficulty = -1

    def play(self, board, screen):
        if self.is_ai:
            col = best_col_prediction(board, self.symbol)
        else:
            click = screen.get_mouse_pos()
            col = (click[0] - padding) // var.size_cell
        return col

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Player):
            return self.symbol == other.symbol
        elif isinstance(other, Symbol):
            return self.symbol.v == other.v
        return False


class Game:
    """The big class that will regulate everything"""

    def __init__(self):
        # Players
        self.player_1: Player = None
        self.player_2: Player = None
        self.player_playing: Player = None
        self.player_null = Player(var.symbol_no_player, var.color_trans, False)

        self.screen_size = (var.width_screen, var.height_screen)

    def inverse_player(self):
        """Return the symbols of the opponent of the player currently playing"""
        if self.player_playing == self.player_1:
            self.player_playing = self.player_2
        elif self.player_playing == self.player_2:
            self.player_playing = self.player_1
        else:
            raise ValueError(
                "How is that possible ? Read carefully the log and send me everything"
            )

    def state_to_bits(self, state: np.ndarray[np.dtype[np.float64], np.float64]) -> str:
        """Convert the state of the game for a player into the bits representation of the game"""
        n = "0b"
        for j in range(len(state[0]) - 1, -1, -1):
            n += "0"
            for i in range(len(state)):
                n += f"{int(state[i, j])}"  # <==> n += str(b)
        return n

    def state_win(self, state: np.ndarray[np.float64]) -> bool:
        bits = int(state_to_bits(state), 2)

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

    def who_is_winner(self):
        s = self.board.shape
        state_symbol_player_1 = np.zeros(s)
        state_symbol_player_2 = np.zeros(s)
        state_symbol_player_1[np.where(self.board == self.player_1.symbol)] = 1
        state_symbol_player_2[np.where(self.board == self.player_2.symbol)] = 1
        if self.state_win(state_symbol_player_1):
            return self.player_1.symbol
        elif self.state_win(state_symbol_player_2):
            return self.player_2.symbol
        else:
            return self.player_null.symbol

    def draw_winner(self):
        winner = self.who_is_winner()
        if winner == self.player_1:
            print("Winner is the first player")
        elif winner == self.player_2:
            print("Winner is the second player")
        else:
            print("That is a draw")
        print("Not finished")

    def start_game(self):
        raise NotImplementedError("Not for now")
        self.draw_start_screen()
        self.board = np.array([[symbol_no_player] * 7 for i in range(6)])
        self.screen = pg.display.set_mode(self.screen_size, 0, 32)
        self.CLOCK = pg.time.Clock()
        self.screen.display.set_caption(var.screen_title)
        self.num_turn = 0

    def draw_options_screen(self):
        raise NotImplementedError("Not for now")

    def draw_play_options(self):
        """Show the different options when choosing to play"""
        screen = Screen(self.screen, *self.screen_size)
        text_HvH = screen.create_text_rendered(var.text_options_play_HvH)
        text_HvAI = screen.create_text_rendered(var.text_options_play_HvAI)
        text_AIvAI = screen.create_text_rendered(var.text_options_play_AIvAI)
        text_options = [[text_HvH], [text_HvAI], [text_AIvAI]]
        boxes = screen.center_all(text_options)
        self.status = var.options_menu_play
        while self.status == var.options_menu_play:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    mouse = pg.mouse.get_pos()
                    screen.handle_quit(quit_box, mouse)
                    if screen.x_in_rect(boxes[0][0], mouse):
                        self.status = var.options_play_HvH
                        self.player_1 = Player(var.symbol_player_1, var.color_player_1, False)
                        self.player_2 = Player(var.symbol_player_2, var.color_player_2, False)
                    elif screen.x_in_rect(boxes[1][0], mouse):
                        self.status = var.options_play_HvAI
                        self.show_options_AI(1)
                    elif screen.x_in_rect(boxes[2][0], mouse):
                        self.status = var.options_play_AIvAI
                        self.show_options_AI(2)
                    elif screen.x_in_rect(cancel_box, mouse):
                        self.status = var.options_clicked_cancel
        if self.difficulty_AI_2 == -1 and self.status not in [
            var.options_play_HvH,
            var.options_clicked_cancel,
        ]:
            self.status = show_options_play()

    def draw_start_screen(self):
        raise NotImplementedError("Not for now")
        """Show the start screen.
        For now it is only the play button but soon there will be more options"""

        start_screen = Screen(self.screen, *self.screen_size, cancel_box=False)
        text_play = start_screen.create_text_rendered(var.text_options_play)
        boxes_options = start_screen.center_all([[text_play]])
        rect_play = boxes_options[0][0]
        self.status = var.options_menu_start
        while self.status == var.options_menu_start:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    mouse = pg.mouse.get_pos()
                    start_screen.handle_quit(quit_box, mouse)
                    if start_screen.x_in_rect(rect_play, mouse):
                        self.draw_play_options()
        if self.status == var.options_clicked_cancel:
            self.draw_start_screen()
