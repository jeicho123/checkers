from checkers import CheckersGame, PieceColor
from bot import randomBot, smartBot
import random

def test_random_1():
    """
    Checks that the start and end coordinate returned by bot corresponds to a
    valid move.
    """
    board = CheckersGame(3)
    bot = randomBot(board, PieceColor.BLACK)

    start, end = bot.suggest_move()

    assert board.is_valid_move(PieceColor.BLACK, start, end)

def test_random_2():
    """
    Checks that the random bot is truly random and cannot distinguish between a
    winning move and a regular move
    """
    board = CheckersGame(3)
    bot = randomBot(board, PieceColor.BLACK)
    # This move creates a trap that will result in forced moves being played so 
    # the player will ultimately emerge one piece up
    best_move_black = ((2, 5), (3, 6))

    # Moves below are not part of a game, simply setting up a position
    board.move(PieceColor.BLACK, (2, 1), (3, 0))
    board.move(PieceColor.BLACK, (2, 3), (3, 4))
    board.move(PieceColor.BLACK, (1, 2), (2, 1))
    board.move(PieceColor.RED, (5, 2), (4, 3))
    board.move(PieceColor.RED, (6, 1), (5, 2))
    board.move(PieceColor.RED, (5, 0), (4, 1))
    board.move(PieceColor.RED, (4, 1), (3, 2))

    # Check multiple times in case the random bot coincidentally finds the
    # best move
    random.seed("test_random_2")
    for _ in range(100):
        move = bot.suggest_move()
        assert move == best_move_black

def test_smart_1():
    """
    Checks that the start and end coordinate returned by bot corresponds to a 
    valid move.
    """
    board = CheckersGame(3)
    bot = smartBot(board, PieceColor.BLACK, 4)

    start, end = bot.suggest_move()

    assert board.is_valid_move(PieceColor.BLACK, start, end)

def test_smart_2():
    """
    Checks that the smart bot makes the best possible move and seizes an
    opportunity when presented. Using the same earlier puzzle, the smart bot 
    with its depth set to a minimum of 5 is able to find the best move.
    """
    board = CheckersGame(3)
    bot = smartBot(board, PieceColor.BLACK, 5)
    best_move_black = ((2, 5), (3, 6))

    board.move(PieceColor.BLACK, (2, 1), (3, 0))
    board.move(PieceColor.BLACK, (2, 3), (3, 4))
    board.move(PieceColor.BLACK, (1, 2), (2, 1))
    board.move(PieceColor.RED, (5, 2), (4, 3))
    board.move(PieceColor.RED, (6, 1), (5, 2))
    board.move(PieceColor.RED, (5, 0), (4, 1))
    board.move(PieceColor.RED, (4, 1), (3, 2))

    # Checks multiple times that the best move is found every time
    for _ in range(100):
        move = bot.suggest_move()
        assert move == best_move_black




