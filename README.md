# Checkers  
This repository contains a design and implementation for a resizable game of
checkers that supports board sizes from 6x6 to 20x20.  

## Division of Work
Game Logic: Patrick Lin  
TUI:  Nathan Moonesinghe  
GUI: Tiffany Lee  
Bot: Jei Ho  

## Summary of Changes  
### Design  

### Game Logic  
- Piece class no longer has an instance variable for its position on the board
- added DRAW to PieceColor enum type
- separated Checkers-specific game logic from the Board following the updated
design
- CheckersGame now stores lists of coordinates of player pieces rather than
lists of instances of the Piece class
    + CheckersGame methods have been updated to accommodate this change
- CheckersGame move method now accepts a color parameter so players cannot move
opponent's pieces

### TUI

### GUI

### Bot

## Setup  
We recommend setting up a virtual environment to install the libraries required
to run the code in this repository. To setup a virtual environment, run the
following from the root of the repository.

    python3 -m venv venv  

To activate your virtual environment, run the following:

    source venv/bin/activate  

To install the required Python libraries run the following:  

    pip3 install -r requirements.txt  

To deactivate the virtual environment, run the following:

    deactivate

## Running the TUI  
To run the TUI, run the following from the root of the repository:

    python3 src/tui.py

The TUI first asks for the number of rows of pieces in order to create the 
correct board size. It then displays the state of the board. Starting with 
black, it asks the player for a piece they want to move. You must specify the
coordinates of the piece in this form: row, col. If the given piece is movable, 
it will ask for the desired coordinates of the piece in this form: row, col. If 
the coordinates are not valid, you will be prompted for a new set of 
coordinates. 

You can also play against a bot like this:

    python3 src/tui.py --player2 <bot>

Where <bot> is either random-bot or smart-bot

You can even have two bots play against each other:

    python3 src/tui.py --player1 <bot> --player2 <bot>

There is no aftificial delay between each bot's move.  

Milestone3 improvements:
- board has row and col index on the side, making it easier to identify 
 a given square on the board
- bug for mis-inputs fixed to allow you to enter a new set of coordinates rather
 than raise an error when invalid coordinates are entered as a move
- pieces changed to be more representative of a Checkers game 
    + ● represent regular pieces
    + K represent Kings


## Running the GUI  
To run the GUI, run the following from the root of the repository:

    python3 src/gui.py

The GUI displays the current state of the board. To move a piece, the current and selected piece's valid moves will be highlighted, and the player can select where they want to move (out of the valid moves).

Like the TUI, you can play against a bot, or have two bots play against each other:

    python3 src./tui.py --player2 <bot>

    python3 src./tui.py --player1 <bot> --player2 <bot>

The --bot delay <seconds> parameter is also supported.

## Bots  
To simulate a random bot playing with a smart bot that uses minimax algorithm and display the live game move by move, run:

    python3 src/bot.py playout

To display the win percentage of the smart bot vs the random bot over the course of 10 games, run:

    python3 src/bot.py simulate

If you like to change the depth (-d) of the minimax algorithm, the row (-r) of the board, the number (-n) of simulated games for the above, you can run (as an example) 

    python3 src/bot.py playout -n 20 -d 4 -r 4

or

    python3 src/bot.py simulate -n 20 -d 4 -r 4

