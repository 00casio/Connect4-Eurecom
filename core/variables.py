#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from argparse import Namespace

pg.init()
Color = pg.Color
Rect = pg.Rect
Surface = pg.Surface


class Variables:
    """Contains all variables in the game"""

    def __init__(self) -> None:
        # Texts
        self.texts = {
            "en": {
                "boxAI_text_levels": [
                    "Start",
                    "Start",
                    "Meh, begin",
                    "Get my a** kicked",
                    "Welcome to Hell",
                ],
                "options_play_local": "Play locally",
                "options_play_online": "Play online",
                "options_options": "Options",
                "options_play_HvH": "Human vs. Human",
                "options_play_HvAI": "Human vs. AI",
                "options_play_AIvAI": "Watch the world burn",
                "options_difficulty_HvAI": "Choose your poison",
                "options_difficulty_AIvAI": "How badly do you want this game to go ?",
                "confirmation_button": "Sarah Connor ?",
                "cancel_box": "Return",
                "quit_box": "Quit",
                "message_quit": "You chose to quit the game\nYou are disapointing me",
                "text_levels": "Level",
                "online_agreement_box": "Broadcast myself as is",
                "online_text_waiting": [
                        "Please wait a few seconds",
                        "We are getting a list of all potential opponents",
                    ],
                "online_text_waiting_empty": [
                        "Looks like we did not find any.",
                        "Please wait we will look",
                        "again in a few seconds",
                    ],
                "text_retry": "Retry"
            },
            "fr": {
                "boxAI_text_levels": [
                    "Commencer",
                    "Commencer",
                    "Bon, commence",
                    "Je veux souffrir",
                    "LEROYYYYYYYY",
                ],
                "options_play_local": "Jouer localement",
                "options_play_online": "Jouer en ligne",
                "options_options": "Options",
                "options_play_HvH": "Humain vs. Humain",
                "options_play_HvAI": "Humain vs. IA",
                "options_play_AIvAI": "[Insérer citation connue de 'The Dark Knight']",
                "options_difficulty_HvAI": "Choisis ton poison",
                "options_difficulty_AIvAI": "À quoi voulez-vous condamner la Terre ?",
                "confirmation_button": "Sarah Connor ?",
                "cancel_box": "Retour",
                "quit_box": "Quitter",
                "message_quit": "Vous avez choisis d'abandonner le jeu.\nVous me décevez.",
                "text_levels": "Niveau",
                "online_agreement_box": "Participer ainsi",
                "online_text_waiting": [
                        "Merci d'attendre un peu",
                        "Nous cherchons des adversaires",
                    ],
                "online_text_waiting_empty": [
                        "Ici t'es personne ! Non sérieusement.",
                        "On cherche à nouveau dans quelques secondes"
                    ],
                "text_retry": "Recommencer"
            },
            "cat": {
                "boxAI_text_levels": [
                    "Nya",
                    "Nyaaaa",
                    "Nyah !",
                    "Nyaaaaaaa?",
                    "Nya.",
                ],
                "options_play_local": "NYA",
                "options_play_online": "NYA NYA. nya.",
                "options_options": "Nya Nya",
                "options_play_HvH": "Nyaaa Nya",
                "options_play_HvAI": "NYAAAA !",
                "options_play_AIvAI": "Nya. Nya nyah nya. Nya nyah !",
                "options_difficulty_HvAI": "Nyah nyah",
                "options_difficulty_AIvAI": "Nya nya, nyanyanya nya",
                "confirmation_button": "Nyyyaaaaa ?",
                "cancel_box": "Nyah",
                "quit_box": "Nya Nya",
                "message_quit": "Nya nya.\n Nya nya (－‸ლ) nya",
                "text_levels": "Nyaaa",
                "online_agreement_box": "Nya nyyyya nya !",
                "online_text_waiting": [
                        "Nya ! Nya nyaaaa nya nhya. nyah",
                        "NYYYA, nhya NYA. Nyaaaah nyyaa",
                    ],
                "online_text_waiting_empty": [
                        "Nyanyanya nya NHAY???",
                        "Nya nyaaaaa nya...",
                        "Nya nya nyaaah nyyyyya",
                    ],
                "text_retry": "Nyhaaa"
            },
            "wls": {
                "boxAI_text_levels": [
                    "Cychwyn",
                    "Dechrau",
                    "Lefel fy mrawd",
                    "O'r diwedd rhywfaint o boen",
                    "Rydych yn deffro'r ddraig goch",
                ],
                "options_play_local": "Chwarae",
                "options_play_online": "Ar-lein",
                "options_options": "Dewisiadau",
                "options_play_HvH": "Dynol vs. Dynol",
                "options_play_HvAI": "Dynol vs. Ddraig",
                "options_play_AIvAI": "Welwn ni chi yn uffern",
                "options_difficulty_HvAI": "Dewiswch eich gwenwyn",
                "options_difficulty_AIvAI": "Faint ydych chi am gael eich curo ?",
                "confirmation_button": "Gwneud Geraint yn falch",
                "cancel_box": "Dychwelyd",
                "quit_box": "Ymddiswyddo",
                "message_quit": "Byddai gan Aeronwen gywilydd ohonoch chi",
                "text_levels": "Lefel",
                "online_agreement_box": "Dechreuwch y twrnamaint",
                "online_text_waiting": [
                        "Arhoswch ychydig eiliadau os gwelwch yn dda",
                        "Rydym yn cael rhestr o'r holl wrthwynebwyr posibl",
                    ],
                "online_text_waiting_empty": [
                        "Nid oes neb o gwmpas",
                        "Os gwelwch yn dda aros,",
                        "byddwn yn edrych mewn ychydig eiliadau",
                    ],
                "text_retry": "Ailgynnig"
            },
            "fra": {
                "boxAI_text_levels": [
                    "Start",
                    "Start",
                    "Meh, begin",
                    "Get my a** kicked",
                    "Welcome to Hell",
                ],
                "options_play_local": "Play locally",
                "options_play_online": "Play online",
                "options_options": "Options",
                "options_play_HvH": "Human vs. Human",
                "options_play_HvAI": "Human vs. AI",
                "options_play_AIvAI": "Watch the world burn",
                "options_difficulty_HvAI": "Choose your poison",
                "options_difficulty_AIvAI": "How badly do you want this game to go ?",
                "confirmation_button": "Sarah Connor ?",
                "cancel_box": "Return",
                "quit_box": "Quit",
                "message_quit": "You chose to quit the game\nYou are disapointing me",
                "text_levels": "Level",
                "online_agreement_box": "Broadcast myself as is",
                "online_text_waiting": [
                        "Please wait a few seconds",
                        "We are getting a list of all potential opponents",
                    ],
                "online_text_waiting_empty": [
                        "Looks like we did not find any.",
                        "Please wait we will look",
                        "again in a few seconds",
                    ],
                "text_retry": "Retry"
            },
        }
        self.language = "en"

        self.text_draw = {
            "en": "No one won",
            "fr": "C'est une égalité",
            "cat": "Nya nya...",
            "welsh": "Rydych yn mynd i raffl"
        }

        # Symbols
        self.symbol_no_player = "0"
        self.symbol_player_1 = "1"
        self.symbol_player_2 = "2"

        # Boxes for levels of AI
        self.box_out = 0
        self.boxAI_out = -1
        self.boxAI_play = -255
        self.boxAI_cancel = 255

        # Colors
        self.white = Color(255, 255, 255)
        self.black = Color(0, 0, 0)
        self.red = Color(255, 0, 0)
        self.green = Color(0, 255, 0)
        self.purple = Color(240, 50, 255)
        self.blue = Color(38, 60, 255)
        self.yellow = Color(239, 248, 62)
        self.dark_blue = Color(0, 0, 229)
        self.light_blue = Color(30, 160, 255)
        self.very_light_blue = Color(20, 235, 255)
        self.cyan = Color(45, 245, 255)
        self.grey = Color(200, 200, 200)
        self.color_trans = Color(0, 0, 0, 0)
        self.color_player_1 = self.red
        self.color_player_2 = self.yellow
        self.color_hover_player_1 = self.color_player_2
        self.color_hover_player_2 = self.color_player_1
        self.color_board = self.blue
        self.color_screen = self.white
        self.color_highlight_column = self.grey
        self.color_options_screen = self.light_blue
        self.color_options_highlight_box = self.cyan
        self.color_options_highlight_text = self.black
        self.color_options_box = self.blue
        self.color_options_text = self.white
        self.color_hovering_box = self.red

        # Size
        self.size_cell = 100
        self.padding = int(self.size_cell * 1.5)
        self.width_board = 7 * self.size_cell
        self.height_board = 6 * self.size_cell
        self.radius_hole = 40
        self.radius_disk = 49
        self.width_screen = 2 * self.padding + self.width_board
        self.height_screen = 2 * self.padding + self.height_board
        self.options_spacing = self.padding // 4
        self.text_box_spacing = self.padding // 10
        self.center_screen = (
            self.width_screen // 2,
            self.height_screen // 2,
        )

        # Options
        self.options_menu_start = -1
        self.options_menu_play = 0
        self.options_play_HvH = 1
        self.options_play_HvAI = 2
        self.options_play_AIvAI = 3
        self.options_clicked_cancel = -255

        # Pygame
        self.fps = 30
        self.screen_title = "Connect 4"
        self.pos_min_x = self.padding + self.size_cell // 2
        self.pos_max_x = self.padding + self.width_board - self.size_cell // 2
        self.text_size = 30
        self.text_font = "monospace"
        self.text_franz_font = "assets/franz/AlanisHand.ttf"

        # Assets
        self.camera = True
        self.sound = True
        self.sound_click_box = "assets/box.mp3"
        self.sound_error = "assets/error.mp3"
        self.sound_disk_touch = "assets/tuck.mp3"
        self.sound_winner_draw = "assets/draw.mp3"
        self.sound_winner_victory = "assets/victory.mp3"
        self.sound_winner_defeat = "assets/lose.mp3"
        self.sound_franz_disk = "assets/franz/tuck.mp3"
        self.sound_franz_win = "assets/franz/win.mp3"
        self.sound_franz_lose = "assets/franz/lose.mp3"
        self.image_volume_on = "assets/volume.svg"
        self.image_volume_muted = "assets/muted.svg"
        self.image_camera = "assets/camera.svg"
        self.image_nocamera = "assets/no-camera.svg"
        self.image_english = "assets/english.svg"
        self.image_french = "assets/french.svg"
        self.image_cat = "assets/cat.png"
        self.image_welsh = "assets/welsh.svg"
        self.image_cat_tails = "assets/cat/tails.png"
        self.image_cat_heads = "assets/cat/heads_1.png"
        self.image_franz_tails = "assets/franz/pile.png"
        self.image_franz_heads = "assets/franz/face.png"

        # Quit and cancel
        self.coor_cancel_box = (10, 10)
        self.coor_quit_box = (self.width_screen - 10, 10)

    # Text changing with language
    def load_language(self) -> None:
        """ Change the variables according to the language chosen """
        self.text_options_play_local = self.texts[self.language]["options_play_local"]
        self.text_options_play_online = self.texts[self.language]["options_play_online"]
        self.text_options_options = self.texts[self.language]["options_options"]
        self.text_options_play_HvH = self.texts[self.language]["options_play_HvH"]
        self.text_options_play_HvAI = self.texts[self.language]["options_play_HvAI"]
        self.text_options_play_AIvAI = self.texts[self.language]["options_play_AIvAI"]
        self.text_options_difficulty_HvAI = self.texts[self.language]["options_difficulty_HvAI"]
        self.text_options_difficulty_AIvAI = self.texts[self.language][
            "options_difficulty_AIvAI"
        ]
        self.text_difficulty_options = [
            "Waouh, an easter egg !",
            self.text_options_difficulty_HvAI,
            self.text_options_difficulty_AIvAI,
        ]
        self.text_confirmation = self.texts[self.language]["confirmation_button"]
        self.text_box_levels = self.texts[self.language]["text_levels"]
        self.text_online_agreement_box = self.texts[self.language]["online_agreement_box"]
        self.boxAI_text_levels = self.texts[self.language]["boxAI_text_levels"]
        self.text_cancel_box = self.texts[self.language]["cancel_box"]
        self.text_quit_box = self.texts[self.language]["quit_box"]
        self.message_quit = self.texts[self.language]["message_quit"]
        self.text_online_waiting = self.texts[self.language]["online_text_waiting"]
        self.text_online_empty_waiting = self.texts[self.language]["online_text_waiting_empty"]
        self.text_retry = self.texts[self.language]["text_retry"]
        if self.language == "fra":
            self.color_board = self.color_trans
        else:
            self.color_board = self.blue


class Config(Variables):
    """The config class is a simple wrapper around the Variables class"""

    def __init__(self, arguments: Namespace) -> None:
        Variables.__init__(self)
        self.sound = not arguments.novolume
        self.camera = not arguments.nocamera
        self.language = arguments.language
        self.change_language(self.language)

    def change_language(self, language: str) -> None:
        """Load the correct language in the variables"""
        if language not in list(self.texts):
            print(f"This language {language} is not available.\nI will use English")
            language = "en"
        self.language = language
        self.load_language()
