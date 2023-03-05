"""
GUI for Checkers!
"""
#took inspiration from connectm! 

import os
import sys
from typing import Union, Dict

import pygame
import click

from checkers import CheckersGame, Board, PieceColor
from bot import randomBot, smartBot

WIDTH = 800
HEIGHT = 800

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (210, 180, 140)
CYAN = (0,255,255)

class GUIPlayer:
    """
    A class to represent a GUI player.
    """
    name: str
    bot: Union[None, randomBot, smartBot]
    board: Board
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

def highlight_moves(start_color, board, surface, start_coord):
    """
    Highlights all valid moves of a piece. 

    Args:
        start_color: 
        board:
        surface:
        start_coord:

    """
    board_grid = board.board_to_str()
    rows = len(board_grid)
    cols = len(board_grid[0])

    rh = HEIGHT // rows
    cw = WIDTH // cols
    
    for moves in board.player_valid_moves(start_color)[start_coord]:
        for coord in moves:
            c, r = coord
            rect = (r * rh, c * cw, cw, rh)
            pygame.draw.rect(surface, CYAN, rect=rect, width=3)

    # pygame.display.update()

def remove_highlight(start_color, board, surface, start_coord):
    """
    Removes the highlight of all valid moves of a piece


    """
    board_grid = board.board_to_str()
    rows = len(board_grid)
    cols = len(board_grid[0])

    rh = HEIGHT // rows
    cw = WIDTH // cols

    x, y = pygame.mouse.get_pos()
    row = x // rh
    col = y // cw
    start_coord = col, row
    
    for moves in board.player_valid_moves(start_color)[start_coord]:
        for coord in moves:
            c, r = coord
            rect = (r * rh, c * cw, cw, rh)
            pygame.draw.rect(surface, DARK_BROWN, rect=rect, width=3)
    
    # pygame.display.update()

def get_coord(board, coord):
    """
    Returns the coordinate of a selected piece.


    """
    board_grid = board.board_to_str()
    rows = len(board_grid)
    cols = len(board_grid[0])

    rh = HEIGHT // rows
    cw = WIDTH // cols

    x, y = coord 

    row = x // rh
    col = y // cw

    return (col, row)

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
    # clock = pygame.time.Clock()

    piece1 = None
    piece2 = None
    board_grid = board.board_to_str()

    while board.get_winner() is None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                
                if piece1 != None:
                    piece1 = get_coord(board)
                    col = piece1[0]
                    row = piece1[1]

                    start_color = None
                    if board_grid[col][row] == 'B':
                        start_color = PieceColor.BLACK
                    elif board_grid[col][row] == 'b':
                        start_color == PieceColor.BLACK
                    elif board_grid[col][row] == 'R':
                        start_color = PieceColor.RED
                    elif board_grid[col][row] == 'r':
                        start_color = PieceColor.RED

                    highlight_moves(start_color, piece1, board, surface)
                elif piece2 != None:
                    piece2 = get_coord(board)
                    if piece2 is None:
                        piece1 = None
                        break

                if piece1 and piece2:
                    if piece1 == piece2:
                        remove_highlight(piece1.color, surface, board, piece1)
                        piece1 = None
                        piece2 = None
                        continue
                    if not board.is_valid_move(piece1, piece2):
                        print("Invalid move")
                    else:
                        board.move(piece1, piece2)
                        remove_highlight(piece1.color, surface, board, piece1)

                        if current_player == PieceColor.BLACK:
                            current_player == GUIPlayer.player2
                        else:
                            current_player == GUIPlayer.player1

                        piece1 = None
                        piece2 = None
                            
        # if current_player.bot is not None:
        #         pygame.time.wait(int(bot_delay * 1000))
        #         coord, move = current_player.bot.suggest_move()

        create_board(surface, board)
        pygame.display.update()
        # clock.tick(24)

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
        board = CheckersGame(3)

    player1 = GUIPlayer(1, player1, board, PieceColor.BLACK, PieceColor.RED)
    player2 = GUIPlayer(2, player2, board, PieceColor.RED, PieceColor.BLACK)
    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(board, players, bot_delay)

if __name__ == "__main__":
    command()