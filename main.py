#!/usr/bin/python3
# -*- coding: utf-8 -*-

from arguments import args
from game import Game
from variables import Variables

game = Game(Variables(), args)
game.start()
