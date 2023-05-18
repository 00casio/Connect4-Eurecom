# Project S6

The project S6 of:

- Francois Barnouin (AI)
- Cindy Do (Communication)
- Henri Gasc (Interface)
- Guillaume Ung (AI)
- Hamza Jad AL Aoun (Hands gesture)

### This week objectives

- [x] Speed up the minimax algorithm
- [ ] Solve lag problem on gestures
- [x] Reorganize repo

### Objectives

The objectives of this project are the following:

- Building a Connect-4 game playable on a Raspberry Pi board
- Setting up a protocol to play with two different Raspberry Pi
- Building an AI capable of playing the game
- Building a program allowing a human to play the game with hand gestures using the Raspberry Pi camera module

We may be able to use the time between out move and the opponent's move to squeeze in some more time to compute things.

If we can use the [boost.Python](https://github.com/boostorg/python) library on the raspberry, it would bring many speed improvements over SWIG.

#### Interface

- [x] Choose mode
- [x] Grid
- [x] Play sound
- [x] Highlight selected column
- [ ] Menu to choose the opponent

Optional:

- [ ] Name
- [x] Options
- [ ] Change theme
- [ ] Background music

#### AI

- [x] Use minimax algorithm

Optional:

- [x] Change difficulty
- [ ] Different gameplay
- [ ] Add other algorithms
- [ ] Test if negamax is faster when using only int64/uint64

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
