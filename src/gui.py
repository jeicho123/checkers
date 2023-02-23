"""
GUI for Checkers!
"""
import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import click

from checkers import Game, Piece
from bot import randomBot, smartBot

WIDTH = 800
HEIGHT = 800

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GUIPlayer:
    """
    A class to represent a GUI player.
    """
    name: str
    bot: Union[None, randomBot, smartBot]
    board: Game
    color: Piece.get_color()

    def __init__(self, n: int, player: str, board, color: Piece.get_color(),
    opponent_color: Piece.get_color()):
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

    def create_board(surface: pygame.surface.Surface, board) -> None:
        """
        Creates and draws the board in its current state.

        Args:
            surface: Pygame surface that the board is drawn on
            board: The board that needs to be drawn
        """
        board_grid = board.board_to_str()
        rows = len(board_grid)
        cols = len(board_grid[0])

        # Compute row height and column width
        rh = HEIGHT // rows
        cw = WIDTH // cols

        # Fill entire surface window with red
        surface.fill(RED)

        # Drawing each square of the board
        for row in range(rows):
            for col in range(row % 2, rows, 2):
                rect = (col * cw, row * rh, cw, rh)
                pygame.draw.rect(surface, BLACK, rect=rect)

        # Drawing each piece
        for i, r in enumerate(board_grid):
            for j, piececolor in enumerate(r):
                if piececolor == "RED":
                    color = RED
                elif piececolor == "BLACK":
                    color = BLACK

                center = ((j * cw) + (cw // 2), (i * rh) + (rh // 2))
                radius = rh // 2 - 8
                pygame.draw.circle(surface, color=color, 
                center=center, radius=radius)

    def play_checkers(board):
        """
        Plays a game of Checkers in Pygame.
        """