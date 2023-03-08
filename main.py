#!/usr/bin/python3
# -*- coding: utf-8 -*-

from arguments import args
from classes import Game
from variables import Variables

game = Game(Variables(), args)
game.start()
