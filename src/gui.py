"""
GUI for Checkers!
"""
#took inspiration from connectm! 

import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_VIDEODRIVER"] = "dummy"
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

    Returns: None
    """
    board_grid = board.board_to_str()
    rows = len(board_grid)
    cols = len(board_grid[0])

    # Compute row height and column width
    rh = HEIGHT // rows
    cw = WIDTH // cols

    # Fill entire surface window with dark brown
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

def play_checkers(board, players: Dict[PieceColor, GUIPlayer],
                  bot_delay):
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
    current_player = players[PieceColor.BLACK]

    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    size = len(board.board_to_str())

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

            if current_player.bot is not None:
                pygame.time.wait(int(bot_delay * 1000))
                end_col = current_player.bot.suggest_move()

        create_board(surface, board)
        pygame.display.update()
        clock.tick(24)

    winner = board.get_winner()
    if winner is not None:
        print(f"The winner is {players[winner].name}!")


@click.command(name="checkers-gui")
@click.option('--mode',
              type=click.Choice(['real'], case_sensitive=False),
              default="real")
@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def command(mode, player1, player2, bot_delay):
    if mode == "real":
        board = Game(3)

    player1 = GUIPlayer(1, player1, board, PieceColor.BLACK, PieceColor.RED)
    player2 = GUIPlayer(2, player2, board, PieceColor.RED, PieceColor.BLACK)
    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(board, players, bot_delay)

if __name__ == "__main__":
    command()