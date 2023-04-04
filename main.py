#!/usr/bin/python3
# -*- coding: utf-8 -*-

from extern.arguments import args
from core.game import Game

if not args.no_libai:
    import ai.libai as libai
    game = Game(args, libai.Game(), libai.Game())
else:
    game = Game(args, None, None)
game.start()
