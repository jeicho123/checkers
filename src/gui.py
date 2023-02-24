"""
GUI for Checkers!
"""
#took inspiration from connectm! 

import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import click

from checkers import Game, PieceColor
from bot import randomBot, smartBot

WIDTH = 800
HEIGHT = 800

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (210, 180, 140)

class GUIPlayer:
    """
    A class to represent a GUI player.
    """
    name: str
    bot: Union[None, randomBot, smartBot]
    board: Game
    color: PieceColor

    def __init__(self, n, player, board, color, opponent_color):
        """
        Args:
            n: The player's number (1 or 2)
            player: "human", "random bot", or "smart bot"
            board: The checkers board
            player_color: The player's color
            opponent_color: The opponent's color
        """
        if player == "human":
            self.name = f"Player {n}"
            self.bot = None
        elif player == "random bot":
            self.name = f"Random Bot {n}"
            self.bot = randomBot(board, color, opponent_color)
        elif player == "smart bot":
            self.name = f"Smart Bot {n}"
            self.bot = smartBot(board, color, opponent_color)
        self.board = board
        self.color = color

    def create_board(surface: pygame.surface.Surface, board):
        """
        Creates and draws the board in its current state.

        Args:
            surface: Pygame surface that the board is drawn on
            board: The board that needs to be drawn

<<<<<<< HEAD
    Returns: None
    """
    board_grid = board.board_to_str()
    rows = len(board_grid)
    cols = len(board_grid[0])

    # Compute row height and column width
    rh = HEIGHT // rows
    cw = WIDTH // cols

    # Fill entire surface window with red
    surface.fill(DARK_BROWN)

    # Drawing each square of the board
    for row in range(rows):
        for col in range(row % 2, rows, 2):
            rect = (col * cw, row * rh, cw, rh)
            pygame.draw.rect(surface, LIGHT_BROWN, rect=rect)

    # Drawing each piece
    for i, r in enumerate(board_grid):
        for j, piececolor in enumerate(r):
            if piececolor == "R":
                color = (139,0,0)
            elif piececolor == "r":
                color = RED
            elif piececolor == "B":
                color = (128,128,128)
            elif piececolor == "b":
                color = BLACK
            else:
                continue

            center = ((j * cw) + (cw // 2), (i * rh) + (rh // 2))
            radius = rh // 2 - 8
            pygame.draw.circle(surface, color,
            center, radius)
    

def play_checkers(board, surface, players):
    """
    Plays a game of Checkers in Pygame.

    Args:
        board: The checkers board
        players (dict): A dictionary mapping piece colors to
            GUIPlayer objects

    Returns: None
    """
    pygame.init()
    pygame.display.set_caption("Checkers")

    #starting player is a black piece
    current_player = PieceColor.BLACK

    size = len(board.board_to_str)

    while board.get_winner() is None:
        events = pygame.event.get()

        start_row = None
        start_col = None
        end_row = None
        end_col = None

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_player.bot is None and event.type == pygame.KEYUP:
                num = event.unicode
                if num in range(size):
                    if start_row is None:
                        start_row = num
                    elif start_col is None:
                        start_col = num

                        start_coord = start_row, start_col
                        if start_coord in board.player_valid_moves(current_player):
                            for x in board.piece_all_valid(current_player):
                                for y in x:
                                    for position in y:
                                        pygame.draw.rect(surface, WHITE,
                                                         rect=position, width=2)
                        else:
                            start_row = None
                            start_col = None
                    elif end_row is None:
                        end_row = num
                    elif end_col is None:
                        end_col = num
                        end_coord = end_row, end_col
                        if board.valid_move(start_coord, end_coord):
                            board.move(current_player, start_coord, end_coord)
                            start_row = None
                            start_col = None
                            end_row = None
                            end_col = None
                            if not board.turn_incomplete():
                                if current_player == PieceColor.RED:
                                    current_player == PieceColor.BLACK
                                elif current_player == PieceColor.BLACK:
                                    current_player == PieceColor.RED
                        else:
                            end_row = None
                            end_col = None

    winner = board.get_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")
=======
        Returns: None
        """
        board_grid = board.board_to_str()
        rows = len(board_grid)
        cols = len(board_grid[0])

        # Compute row height and column width
        rh = HEIGHT // rows
        cw = WIDTH // cols

        # Fill entire surface window with red
        surface.fill(DARK_BROWN)

        # Drawing each square of the board
        for row in range(rows):
            for col in range(row % 2, rows, 2):
                rect = (col * cw, row * rh, cw, rh)
                pygame.draw.rect(surface, LIGHT_BROWN, rect=rect)

        # Drawing each piece
        for i, r in enumerate(board_grid):
            for j, piececolor in enumerate(r):
                if piececolor == "R":
                    color = (139,0,0)
                elif piececolor == "r":
                    color = RED
                elif piececolor == "B":
                    color = (128,128,128)
                elif piececolor == "b":
                    color = BLACK
                else:
                    continue

                center = ((j * cw) + (cw // 2), (i * rh) + (rh // 2))
                radius = rh // 2 - 8
                pygame.draw.circle(surface, color,
                center, radius)

    def play_checkers(board, players, bot_delay):
        """
        Plays a game of Checkers in Pygame.

        Args:
            board: The checkers board
            players (dict): A dictionary mapping piece colors to
                TUIPlayer objects
            bot_delay: The bot has a delay in which it waits a few
                seconds before making a move.

        Returns: None
        """
        pygame.init()
        pygame.display.set_caption("Checkers")
        surface = pygame.display.set_mode(WIDTH, HEIGHT)
        clock = pygame.time.Clock()

        #starting player is a black piece
        current_player = players["BLACK"]

        while board.get_winner() is None:
            events = pygame.event.get()
            column = None
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if current_player.bot is None and event.type == pygame.KEYUP:
                    key = event.unicode
                    if key in "1234567":
                        v = int(key) - 1
>>>>>>> 339464f306a766345c5b20260945f99cf73c5211
