#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(
    description="Launch a connect 4 window with some options already in place"
)

parser.add_argument(
    "-l",
    "--language",
    dest="language",
    type=str,
    default="en",
    help="Choose the language",
)

parser.add_argument(
    "--no-sound",
    dest="novolume",
    action="store_const",
    const=True,
    default=False,
    help="Disable the sound",
)

parser.add_argument(
    "--no-camera",
    dest="nocamera",
    action="store_const",
    const=True,
    default=False,
    help="Disable the camera",
)

parser.add_argument(
    "--no-libai",
    dest="no_libai",
    action="store_const",
    const=True,
    default=False,
    help="Do not use libai for the AI movement",
)

args = parser.parse_args()
