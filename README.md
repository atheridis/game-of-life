<h1 align="center">Conway's Game of Life - In Python's Pygame</h1>

<p align="center">
    <img width="600"
        alt="Conway's Game of Life - In Python's Pygame"
        src="https://i.imgur.com/mHcbvKw.png">
</p>

## Installation

To install the latest version just type `$ pip install git+https://github.com/atheridis/game-of-life.git`
in your terminal. To run the program type `$ gameoflife`.

You may also clone this repository and install it from there.
```
$ git clone https://github.com/atheridis/game-of-life.git
$ cd game-of-life
$ pip install .
```

## Settings

You will find settings in `~/.config/game-of-life`. Currently Settings are changed through
editing a json file. You can choose the game resolution, the width of the cells in pixels,
the colour of dead and alive cells, and the maximum amount of frames that get computed
each second.

You will need to run the game at least once before the directory becomes available.n your terminal.
To run the program type `$ gameoflife`.

## How to use

### Loading and Saving

Your numrow allow you to load saved states. Some saved states already exist for you to try.
You may press the Function Keys, F1, F2, ..., F10 to save to the corresponding slot (where F10 is 0 on the numrow).
If a state is already saved in one of those keys it will be overwritten **without warning**.

### Keybindings

* Use the Up and Down arrow keys to speed up or slow down the game respectively.
* Use the Spacebar to pause and resume the game
* Press [c] to clear the board
* Press [r] to randomize the board
* Press [ESC] to quit.

## OLD PROJECT

This is one of many of my older projects which I never used git with.
I have decided to turn it into a package and upload it to github.
