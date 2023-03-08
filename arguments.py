#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(description="Launch a connect 4 window with some options already in place")

parser.add_argument(
    "--no-sound",
    dest="novolume",
    action="store_const",
    const=True,
    default=False,
    help="Disable sound by default"
)

parser.add_argument(
    "-l",
    "--language",
    dest="language",
    type=str,
    default="en",
    help="Choose the language"
)

args = parser.parse_args()
