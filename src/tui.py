import time
from typing import Union, Dict

import click
from colorama import Fore

from checkers import Game, PieceColor, Piece

#from bot import randomBot, smartBot


class TUIPlayer:
    """
    Class that stores information about a TUI player

    The TUI player can either be a human or bot
    """
    def __init__(self, player_num, board, color, opponent_color):
        """
        Input:
            player_num (int): Player number (1 or 2)
            player_type (str): "human", "random-bot", or "smart-bot" 
            boar (board): Checker's board
            color (PieceColor): player's color 
            opponent_color (PieceColor): opponent's color 
            bot_delay (float): Artificial delay for a bot
        """
        
        self.name = str(player_num)
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
            user_input = input(str(self.name) + 
            " Insert coordinates of piece: ")
            row = int(user_input.split(",")[0])
            col = int(user_input.split(",")[1])
            coord = (row, col)
            print(self.color)
            print(self.board.player_valid_moves(self.color))
            if coord in self.board.player_valid_moves(self.color):
                for move in self.board.piece_all_valid(coord):
                    print(move) 
                return coord
            
    def get_move(self, coords):
        """
        Prompt the player for the coordinates they want to move a piece to.
        If the coordinates the player wants to move to are valid, will return 
        the final coordinates.

        Input:
            coords tuple(int, int): Takes in the starting coordinates of the piece
        """
        while True:
            input_move = input(str(self.name) + "Insert desired coordinates: ")
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

    print()
    print_board(board)

    winner = board.get_winner()
    if winner == "DRAW":
        print("It's a tie!")
    elif winner is not None:
        print("The winner is " + str(players[winner].name) + " !")


@click.command(name = "Checkers-tui")
@click.option('--player1',
              type = str, default = "human")
@click.option('--player2',
              type = str, default = "human")
@click.option('--rows', type = click.Choice([2, 3, 4, 5, 6, 7, 8, 9]), 
default = 2)
def cmd(rows, player1, player2):
    if rows == 2:
        board = Game(2)
    elif rows == 3:
        board = Game(3)
    elif rows == 4:
        board = Game(4)
    elif rows == 5:
        board = Game(5)
    elif rows == 6:
        board = Game(6)
    elif rows == 7:
        board = Game(7)
    elif rows == 8:
        board = Game(8)
    elif rows == 9:
        board = Game(9)
    board = Game(5)
    player1 = TUIPlayer(1, board, "BLACK", "RED")
    player2 = TUIPlayer(2, board, "RED", "BLACK")
    

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(board, players)


if __name__ == "__main__":
    cmd()
