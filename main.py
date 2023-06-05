#!/usr/bin/python3
# -*- coding: utf-8 -*-

from core.game import Game
from extern.arguments import args
import ai.libai as libai

game = Game(args, libai.Game(), libai.Game())
game.start()
