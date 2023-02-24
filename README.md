# Checkers  
Game Logic: Patrick Lin  
TUI:  Nathan Moonesinghe  
GUI: Tiffany Lee  
Bot: Jei Ho

## Running the TUI  
To run the TUI, run the following from the root of the repository:

python3 src/tui.py

The TUI first asks for the number of rows of pieces in order to create the 
correct board size. It then displays the state of the board. Starting with 
black, it asks the player for a piece they want to move. You must specify the
coordinates of the piece in row, col form. If the given piece is movable, 
it will ask for the desired coordinates of the piece in row, col form. 
The board is 0 indexed, so the row and col numbers must be less than 
2 * board_rows + 2. If the coordinates are not valid, you will be prompted
again. 

You can also play against a bot like this:

python3 src/tui.py --player2 <bot>

Where <bot> is either random-bot or smart-bot

You can even have two bots play against each other:

python3 src/tui.py --player1 <bot> --player2 <bot>

There is no aftificial delay between each bot's move.
## Running the GUI  
To run the GUI, run the following from the root of the repository:

python3 src/gui.py

The GUI displays the current state of the board. To move a piece, the current and selected piece's valid moves will be highlighted, and the player can select where they want to move (out of the valid moves).

Like the TUI, you can play against a bot, or have two bots play against each other.

## Bots  
## Running the GUI  
To run the GUI, run the following from the root of the repository:

> python3 src/gui.py

The GUI displays the current state of the board. To move a piece, the current and selected piece's valid moves will be highlighted, and the player can select where they want to move (out of the valid moves).

Like the TUI, you can play against a bot, or have two bots play against each other:

python3 src./tui.py --player2 <bot>

python3 src./tui.py --player1 <bot> --player2 <bot>

The --bot delay <seconds> parameter is also supported.

## Bots  
To simulate a random bot playing with a smart bot that uses minimax algorithm and display the win percentage of the smart bot, run:

> python3 src/bot.py

If you like to change the depth (-d) of the minimax algorithm, the row (-r) of the board, the number (-n) of simulated games, you can run (as an example)

> python3 src/bot.py -n 20 -d 4 -r 4

