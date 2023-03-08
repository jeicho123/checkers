# Checkers  
This repository contains a design and implementation for a resizable game of
checkers that supports board sizes from 6x6 to 20x20.  

## Division of Work
Game Logic: Patrick Lin  
TUI:  Nathan Moonesinghe  
GUI: Tiffany Lee  
Bot: Jei Ho  

## Summary of Changes  
### Design Changes
- As suggested by the TA's feedback, the Game class has been separated into
a Board class, which is a generic rectangular board for board games, and a 
CheckersGame class which utilizes the Borad class to implement a game of
checkers

### Game Logic Changes
- Piece class no longer has an instance variable for its position on the board
- Added DRAW to PieceColor enum type
- Separated Checkers-specific game logic from the Board following the updated
design
- CheckersGame now stores lists of coordinates of player pieces rather than
lists of instances of the Piece class
    + CheckersGame methods have been updated to accommodate this change
- CheckersGame move method now accepts a color parameter so players cannot move
opponent's pieces
- Edited method names for clarity

### TUI Changes
- Board has row and col index on the side, making it easier to identify 
 a given square on the board
- Bug for mis-inputs fixed to allow you to enter a new set of coordinates rather
 than raise an error when invalid coordinates are entered as a move
- Pieces changed to be more representative of a Checkers game 
    + ● represent regular pieces
    + ♔ represent Kings

### GUI Changes
- Pygame window displays properly
- Added new methods to organize the logic in play_checkers:
    + get_coord: Returns the coordinate of the piece 
    + highlight_moves: Highlights the selected piece's valid moves
        - Checks if selected piece has valid moves
    + remove_highlight: Removes the highlighted moves
        - Removes highlights after checking for selected piece's valid moves
- MAROON piece represents a red piece's king
- GRAY piece represents a black piece's king
- Remove highlights and reset pieces if the same piece2 is selected as piece1, or if selected piece2 is an invalid move from piece1
    + If the move is valid, the highlight from piece1 

### Bot Changes
- Added sources for Minimax algorithm
- Created Botplayer class to store info about bots under Simulation phase 
- Added flexibility to bot matches, user can choose the kind of bot (random/smart) to
  play with each other by assigning the bot's depth value (depth = 0 --> random, depth > 0 --> smart)
- Added option to view live simulation of games between bots
- Took into account draw matches between bots 
- Added ``test_bot.py`` file to test for the methods of each bot

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

    python3 src/tui.py --player2 {bot}

Where {bot} is either random-bot or smart-bot

You can even have two bots play against each other:

    python3 src/tui.py --player1 {bot} --player2 {bot}

Where {bot} is either random-bot or smart-bot

There is no aftificial delay between each bot's move.  

## Running the GUI  
To run the GUI, run the following from the root of the repository:

    python3 src/gui.py

The GUI displays the current state of the board. To move a piece, the current and selected piece's valid moves will be highlighted, and the player can select where they want to move (out of the valid moves).

Like the TUI, you can play against a bot, or have two bots play against each other:

    python3 src/gui.py --player2 {bot}

    python3 src/gui.py --player1 {bot} --player2 {bot}

Where {bot} is either random-bot or smart-bot  
The --bot delay {seconds} parameter is also supported.

## Bots  
The ``bots.py`` file includes two classes:

- ``RandomBot``: A bot that will just choose a move at random
- ``SmartBot``: A bot that uses the Minimax algorithm to make a move, which is given a depth that is the number of moves the algorithm will see ahead. The higher the depth, the more informed of a move the bot will make. It is recommended to set the depth to at least 4 to see its dominant effect when playing against a random bot. Keep in mind that a high depth like 4 paired with a high number of simulated games will correspond to a slower runtime.

The two classes are used in the TUI and GUI, but you can also run ``bots.py`` to run simulated games where two bots face each other, and see the percentage of wins and ties. For example:

    $ python3 src/bot.py -n 1000
        Bot 1 wins (Depth = 0): 43.80%
        Bot 2 wins (Depth = 0): 51.30%
        Ties: 4.90%
        
    $ python3 src/bot.py -n 1000 -d1 3
        Bot 1 wins (Depth = 3): 83.70%
        Bot 2 wins (Depth = 0): 1.60%
        Ties: 14.70%

You can control the identity of the bot through the depth value using the ``-d1 <depth value>`` or ``-d2 <depth value>`` parameter. A bot with depth of 0 will use the RandomBot class whereas a bot with depth greater than 0 will use the SmartBot. 

You can also control the number of simulated games using the ``-n <number of games>`` parameter, the board's initial state using the ``-r <number of rows of pieces>`` parameter, and whether you would like to see a live playout of the simulated games using the ``-p <True/False>``.

The default values are d1=0, d2=0, n=10, r=3, p=False.

