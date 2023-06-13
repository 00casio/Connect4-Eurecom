# Project S6

The project S6 of:

- Francois Barnouin (AI)
- Cindy Do (Communication)
- Henri Gasc (Interface)
- Guillaume Ung (AI)
- Hamza Jad AL Aoun (Hands gesture)

The project was made under the guidance of Nicholas Evans.

## Specifications

To use the whole project (meaning, with the camera, the AI in C++, the communication module), you need to have installed:

- A version of Python (preferably >= 3.11),
- A C++ compiler (*clang++* produces better binary but *g++* works too),
- A working bash interpreter,
- A Raspberry Pi under Raspbian64 with a camera module, a Bluetooth chip, and at least 2 GB of RAM.

All those requirements are easy to fulfil, and you should not have anything to install on your own.

## Setting up

When the previous requirements are fulfilled, you only need to use the [launch](./launch.sh) script, and every other software and libraries required should be installed.  
If the script does not find something, then it prints it and launches the program with some options disabled.  
If you want to use Bluetooth in server mode, then you need to run the script as root (under Linux, you just need to use `sudo ./launch.sh`). It is because advertising the Bluetooth service need root permission.

## Objectives

The objectives of this project are the following:

- Building a Connect-4 game playable on a Raspberry Pi board
- Setting up a protocol to play with two different Raspberry Pi
- Building an AI capable of playing the game
- Building a program allowing a human to play the game with hand gestures using the Raspberry Pi camera module

## Communication code table

Code | Meaning | Action.s upon reception | Type
:---: | :---: | :---: | :---:
000 - 006 | Column number | Put token into right column | `byte`
100 | Asking for a game (asker will play in human mode) | Respond with 102 or 103 | `byte`
101 | Asking for a game (asker will play in AI mode) | Respond with 102 or 103 | `byte`
102 | Game accepted | Launch grid, wait for server to play | `byte`
103 | Game refused | - | `byte`
201 | Game aborted by user (during a game) | Abandon game | `byte`

## Criteria for AI

- An AI at any depth must always beat a player that is always choosing a column randomly.
- An AI at any depth must beat an AI which is at a depth level strictly lower than itself.
- For a given depth level, the AI who starts first must beat an AI at the same depth level.

## Copyright

One of the font used (AlanisHand) is the intellectual property of himasf, more at [1001fonts.com](https://www.1001fonts.com/users/himasf/)
