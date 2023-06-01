# Project S6

The project S6 of:

- Francois Barnouin (AI)
- Cindy Do (Communication)
- Henri Gasc (Interface)
- Guillaume Ung (AI)
- Hamza Jad AL Aoun (Hands gesture)

### This week objectives

- Correct bugs:
  - Clicking after online game send to local menu
  - Clicking return after end online game start a new online game
  - Seems like when root, hovering line is not correct
- Finish communication protocol implementation:
  - When online and click on quit, send message to opponent
  - When connecting, send correct message (100 or 101)
  - Do not close the program when receiving 103
  - For server: ask confirmation when someone asks for a game
  - For client: make sure we receive 102 before proceeding
- Polish the game:
  - Show name of raspberry for server
  - Place filter on possible communications
  - Put texts in variables (with languages)
  - Fuse a "perfect" (look for all poss) AI in our program
- Report:
  - Make benchmarks, comparisons
  - Do almost everything

### Objectives

The objectives of this project are the following:

- Building a Connect-4 game playable on a Raspberry Pi board
- Setting up a protocol to play with two different Raspberry Pi
- Building an AI capable of playing the game
- Building a program allowing a human to play the game with hand gestures using the Raspberry Pi camera module

We may be able to use the time between out move and the opponent's move to squeeze in some more time to compute things.

If we can use the [boost.Python](https://github.com/boostorg/python) library on the raspberry, it would bring many speed improvements over SWIG.

For the first installation, you need to make sure that `libcairomm-dev` (or equivalent) and `libgirepository-dev` (or equivalent) are installed. They are needed by `pygobject` which is needed by `playsound`.

#### Interface

- [x] Choose mode
- [x] Grid
- [x] Play sound
- [x] Highlight selected column
- [x] Menu to choose the opponent

Optional:

- [ ] Name
- [x] Options
- [ ] Change theme
- [ ] Background music
- [ ] Tidy the codebase
  - [x] rewrite reset_screen
  - [x] create class for box (will have coordinate of rect, color of box, text, color of text, if the box is "clickable")

#### AI

- [x] Use minimax algorithm

Optional:

- [x] Change difficulty
- [ ] Different gameplay
- [ ] Add other algorithms
- [x] Test if negamax is faster when using only int64/uint64 (yes it is)

#### Hands gesture

- [x] Choose gestures
- [x] Continuous gesture

Optional:

- [ ] Change on the fly
- [ ] Detect shapes
- [ ] Maybe discrete gestures

#### Communication

- [ ] Choose the mean of communication
- [ ] Choose the protocol

Code | Meaning | Action.s upon reception | Type
--- | --- | --- | ---
000 - 006 | Column number | Put token into right column | `byte`
100 | Asking for a game (asker will play in human mode) | Respond with 102 or 103 | `byte`
101 | Asking for a game (asker will play in AI mode) | Respond with 102 or 103 | `byte`
102 | Game accepted | Launch grid, wait for askee to play (or to send who plays first? **TBD together**) | `byte`
103 | Game refused | - | `byte`
201 | Game aborted by user (during a game) _For now, we wait our turn to send this? (beware of this)_ | Abandon game (this way we know the game was ended because of user request, not because of disconnection) | `byte`

Example of result from find_services:  
[{'service-classes': ['94F39D29-7D6D-437D-973B-FBA39E49D4EE', '1101'], 'profiles': [('1101', 256)], 'name': 'connect4_1', 'description': None, 'provider': None, 'service-id': '94F39D29-7D6D-437D-973B-FBA39E49D4EE', 'protocol': 'RFCOMM', 'port': 1, 'host': 'E4:5F:01:D2:D2:94'}]
