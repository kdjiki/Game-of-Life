# Game-of-Life

## Introduction
Conway's Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. The Game of Life consists of a grid of cells that can be either alive or dead. Each cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbors dies (underpopulation).
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies (overpopulation).
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

These simple rules can lead to surprisingly complex and varied behavior, including patterns that remain stable, oscillate, or even produce moving structures. Conway's Game of Life has fascinated scientists, mathematicians, and hobbyists for decades and is a classic example of emergent behavior.

## Project Description
This implementation of Conway's Game of Life is built using Python and the PyGame library. It provides an interactive graphical interface where users can create their initial configuration of live cells and watch how they evolve over time according to the rules of the game. The program offers various features to enhance user interaction and customization.

## Features
- Interactive Grid: Click on the grid to add or remove cells.
- Start/Pause Control: Use the spacebar or on-screen buttons to start or pause the game.
- Random Grid Generation: Automatically generate a random grid configuration.
- Save and Load Setups: Save the current grid configuration to a file and load previously saved configurations.
- Music: Background music that can be muted/unmuted using the mute button.
- Instructions: In-game instructions are available to help users understand how to interact with the program.
- Step Counter: Tracks the number of steps (generations) since the start.
- Control Panel: Buttons for muting, clearing the grid, viewing instructions, and managing saved setups.
- Setup Management: Load and delete saved grid setups through an intuitive menu.

## Getting Started

### Prerequisites
- Python 3.x
- PyGame library
- tkinter library (comes with Python standard library)

### Installation
- Clone this repository to your computer.
- Open the project.
- Start the game.

## How to Play
- Adding/Removing Cells: Click on the grid to toggle the state of a cell (alive or dead).
- Starting/Pausing the Game: Press the spacebar or click the play/pause button to start or pause the game.
- Clearing the Grid: Press 'C' or click the clear button to clear all cells.
- Random Generation: Press 'A' to generate a random grid configuration.
- Saving a Setup: Press 'S', then type a name and press 'Enter' to save the current grid setup.
- Loading a Setup: Press 'L', then type a name and press 'Enter' to load a saved grid setup.
- Muting/Unmuting Music: Click the mute button to mute or unmute the background music.
- Viewing Instructions: Click the instructions button to view the game instructions.
- Viewing Saved Setups: Click the 'Load' button to view a list of saved setups and load or delete them.

## File Structure
- game_of_life.py: The main Python script containing the game logic and interface.
- grid_setups.json: A JSON file that stores saved grid configurations.
- Martin Roth - An Analog Guy In A Digital World.mp3: Background music file.
- README.md: This file, which contains information about the project.
