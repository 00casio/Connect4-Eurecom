#!/usr/bin/python3
# -*- coding: utf-8 -*-

from classes import Game
from variables import Variables
from arguments import args

game = Game(Variables(), args)
game.start()
