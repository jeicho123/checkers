import click
from colorama import Fore

from checkers import Game, PieceColor, Piece
from bot import randomBot, smartBot

class TUIPlayer:
    """
    Class that stores information about a TUI player

    The TUI player can either be a human or bot
    """
    def __init__(self, player_num, player, board, color, opponent_color,
    depth = 0):
        """
        Input:
            player_num (int): Player number (1 or 2)
            player (str): "human", "random-bot", or "smart-bot" 
            boar (board): Checker's board
            color (PieceColor): player's color 
            opponent_color (PieceColor): opponent's color 
            depth (int): optional parameter that only applies to smart-bot 
            algorithm
        """
        self.color = color
        if player == "human":
            self.name = ("Player " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = None
        if player == "random-bot":
            self.name = ("Random Bot " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = randomBot(board, color)
        elif player == "smart-bot":
            self.name = ("Smart Bot " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = smartBot(board, color, depth)
        
        self.board = board
        self.opponent_color = opponent_color

    def get_movable_pieces(self):
        """
        Prompts the player for coordinates of the piece they want to select.
        If there is a movable piece at the given coordinates, it will print out
        all the valid moves for that piece

        Input: None

        Output: coordinates of the piece that's selected 
        (list[list[(tuple(int, int))])
        """   
        while True:
            user_input = input(self.name + 
            ": Insert coordinates of a piece: ")
            row = int(user_input.split(",")[0])
            col = int(user_input.split(",")[1])
            coord = (row, col)
            if coord in self.board.player_valid_moves(self.color):
                moves = []
                for move in self.board.piece_all_valid(coord):
                    moves.append(move) 
                print("Possible moves: " + str(moves))
                return coord
            
    def get_move(self, coords):
        """
        Prompt the player for the coordinates they want to move a piece to.
        If the coordinates the player wants to move to are valid, will move
        the piece. 

        Input:
            coords (tuple(int, int)): Takes in the starting coordinates of the 
            piece

        Output: None
        """
        while True:
            input_move = input(self.name + 
            ": Insert desired coordinates: ")
            row = int(input_move.split(",")[0])
            col = int(input_move.split(",")[1])
            final_coord = (row, col)
            if self.board.valid_move(self.color, coords, final_coord):
                return final_coord
                
def print_board(board):
    """
    Prints the board to the screen

    Input: 
        board: board to print

    Returns: None
    """
    final = []
    grid = board.board_to_str()
    for r, row in enumerate(grid):
        string = ""
        for c, col in enumerate(row):
            if r % 2 == c % 2:
                if col == " ":
                    string += Fore.WHITE + "[ ]"
                elif col == "B":
                    string += Fore.WHITE + "[B]"
                elif col == "b":
                    string += Fore.WHITE + "[b]"
                elif col == "R":
                    string += Fore.WHITE + "[R]"
                elif col == "r":
                    string += Fore.WHITE + "[r]"
            else:
                if col == " ":
                    string += Fore.BLACK + "[ ]"
                elif col == "B":
                    string += Fore.BLACK + "[B]"
                elif col == "b":
                    string += Fore.BLACK + "[b]"
                elif col == "R":
                    string += Fore.BLACK + "[R]"
                elif col == "r":
                    string += Fore.BLACK + "[r]"
        final.append(string)
    print("\n".join(final))
    return "\n".join(final)


def play_checkers(board, players):
    """
    Plays a game of Checkers on the terminal

    Inputs:
        board (Game): board to play on
        players (Dict[PieceColor, TUIPlayer]): A dictionary mapping 
        piece colors to TUIPlayer objects

    Output: None
    """
    #starting player is black
    current = players[PieceColor.BLACK]

    #keep playing until there's a winner:
    while board.get_winner() is None:
        #prints the board
        print()
        print_board(board)
        print()
       
        if current.bot is not None:
            loc = current.bot.suggest_move()
            start_str = (str(loc[0]))
            end_str = (str(loc[1]))
            start_row_int = int(start_str[1])
            start_col_int = int(start_str[4])
            end_row_int = int(end_str[1])
            end_col_int = int(end_str[4])
            start = (start_row_int, start_col_int)
            end = (end_row_int, end_col_int)
            board.move(current.color, start, end)
        else:
            coords = current.get_movable_pieces()
            dest = current.get_move(coords)
            board.move(current.color, coords, dest)

        #Update the player
        if not board.turn_incomplete():
            board.end_turn(current.color, "End Turn")
            if current.color == PieceColor.BLACK:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.BLACK]
    
    #prints the board
    print()
    print_board(board)

    #checks if there's a winner
    winner = board.get_winner()
    if winner == "DRAW":
        print("It's a tie!")
    elif winner is not None:
        print("The winner is " + str(players[winner].name) + " !")

#
#Command-line interface
#

@click.command(name = "Checkers-tui")
@click.option('--player1',
              type = click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive=False), default = "human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive = False), default = "human")
@click.option('--piece_rows', required = True, prompt = True,
type = click.Choice(["2", "3", "4", "5", "6", "7", "8", "9"]))

def cmd(piece_rows, player1, player2):
    if piece_rows == "2":
        board = Game(2)
    elif piece_rows == "3":
        board = Game(3)
    elif piece_rows == "4":
        board = Game(4)
    elif piece_rows == "5":
        board = Game(5)
    elif piece_rows == "6":
        board = Game(6)
    elif piece_rows == "7":
        board = Game(7)
    elif piece_rows == "8":
        board = Game(8)
    elif piece_rows == "9":
        board = Game(9)

    player1 = TUIPlayer(1, player1, board, PieceColor.BLACK, 
    PieceColor.RED)
    player2 = TUIPlayer(2, player2, board, PieceColor.RED, 
    PieceColor.BLACK)

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(board, players)

if __name__ == "__main__":
    cmd()

