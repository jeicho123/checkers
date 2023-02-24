from checkers import Game, Piece, PieceColor
from colorama import Fore, Style
#from bot import randomBot, smartBot
from typing import Union, Dict
import time
import click


class TUIPlayer:
    """
    Class that stores information about a TUI player

    The TUI player can either be a human or bot
    """
    name: str
    #bot: Union[None, randomBot, smartBot]
    board: Game
    color: PieceColor
    
    def __init__(self, player_num: int, board: Game, color: PieceColor, opponent_color: PieceColor):
        """
        Input:
            player_num (int): Player number (1 or 2)
            player_type (str): "human", "random-bot", or "smart-bot" 
            boar (board): Checker's board
            color (str): player's color 
            opponent_color (str): opponent's color 
            bot_delay (float): Artificial delay for a bot
        """
        
        self.name = f"Player {player_num}"
        self.bot = None
        self.board = board
        self.color = color
        self.opponent_color = opponent_color
    
    def get_movable_pieces(self):
        """
        Prompts the player for coordinates of the piece they want to select.
        If there is a movable piece at the given coordinates, it will print out
        all the valid moves for that piece and return the coordinates of the 
        given piece.

        Input: None

        Output: coordinates of the piece that's selected tuple(int, int)
        """
        while True:
            user_input = input(f"{self.name}" + 
            " Insert coordinates of piece: ")
            coord = user_input.split(",")
            if coord in self.board.player_valid_moves(self.color):
                for move in self.board.piece_all_valid(coord):
                    print(move) 
                return coord
            
    def get_move(self, coords):
        """
        Prompt the player for the coordinates they want to move a piece to.
        If the coordinates the player wants to move to are 
        """
        while True:
            input_move = input(f"{self.name}" + "Insert desired coordinates: ")
            final_coord = input_move.split(",")
            if self.board.valid_move(coords, final_coord):
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


def play_checkers(board: Game, players: Dict[PieceColor, TUIPlayer]):
    """
    Plays a game of Checkers on the terminal

    Inputs:
        board: board to play on
        players: A dictionary mapping piece colors to TUIPlayer objects

    Output: None
    """
    #starting player is black
    current = players[PieceColor.BLACK]

    #keep playing until there's a winner:
    while board.get_winner is None():
        #prints the board
        print()
        print_board(board)
        print()

        coords = current.get_piece()
        dest = current.get_move(coords)

        board.move(current.color, coords, dest)


        if not board.turn_incomplete():
            board.end_turn(current.color, "End Turn")
            if current.color == PieceColor.BLACK:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = PieceColor.RED

    print()
    print_board(board)

    winner = board.get_winner()
    if winner == "DRAW":
        print("It's a tie!")
    elif winner is not None:
        print(f"The winner is {players[winner].name}!")


def cmd(player1, player2):
    board = Game(2)

    player1 = TUIPlayer(1, player1, board, "BLACK", "RED")
    player2 = TUIPlayer(2, player2, board, "RED", "BLACK")

    players = {"BLACK": player1, "RED": player2}

    play_checkers(board, players)


if __name__ == "__main__":
    cmd()
