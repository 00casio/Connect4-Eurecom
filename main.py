#!/usr/bin/python3
# -*- coding: utf-8 -*-

from arguments import args
from game import Game
from variables import Variables

if not args.no_libai:
    import libai
    game = Game(Variables(), args, libai.Game(), libai.Game())
else:
    game = Game(Variables(), args, None, None)
game.start()
