from checkers import Game, PieceColor
from copy import deepcopy
import random
import click

class randomBot():
    """
    Class for bot that suggests random moves
    """
    def __init__(self, board, color):
        """
            Constructor

            board (Game obj): board that bot will play on
            color (PieceColor obj): color of the pieces the bot will play with 
        """
        self._board = board
        self._color = color

    def suggest_move(self):
        """
        Randomly selects a piece and randomly selects out of the viable paths
        from the piece can choose to take.

        Parameters:
            None

        Returns:
            tuple(tuple, tuple): first tuple represents starting coordinates of 
            the random piece, second tuple represents end coordinates of the 
            random path
        """
        rand_piece = random.choice(list(self._board.player_valid_moves(self._color).items()))
        rand_path = random.choice(rand_piece[1])
        return rand_piece[0], rand_path[-1]

class smartBot():
    """
    Class for bot that uses Minimax algorithm to suggest moves
    """
    def __init__(self, board, color, depth):
        """
            Constructor

            board (Game obj): board that bot will play on
            color (PieceColor obj): color of the pieces the bot will play with 
            depth (int): depth of the Minimax algorithm
        """
        self._board = board
        self._color = color
        self._depth = depth
    
    def suggest_move(self):
        """
        Calls the private method _minimax() to return the coordinates of the 
        piece that should be moved and where it should be moved to.

        Parameters:
            None

        Returns:
            tuple(tuple): first tuple represents starting coordinates of Minimax
            chosen piece, second tuple represents end coordinates of Minimax 
            chosen path
        """
        move = self._minimax(self._board, self._depth, self._color)
        return move[:2]

    def _minimax(self, board, depth, color):
        """
        Minimax algorithm that traverses a tree of paths given a starting 
        position and bottoms up to the root, returning the next best move for 
        the bot. At each node, depending on the color, the algorithm will
        maximize/minimize the values of the level of nodes below it and obtain
        the move needed to reach that minimal/maximal position. 

        Parameters:
            board (Game obj): board that bot will play on
            depth (int): the number of moves that the bot thinks ahead
            color (PieceColor obj): color of the pieces the bot will play with 

        Returns:
            tuple(tuple, tuple, int): first tuple represents starting 
            coordinates of Minimax chosen piece, second tuple represents end 
            coordinates of Minimax chosen path, third tuple represents 
            evaluation of the board
        """
        # Base case --> leaf of tree or game recognizes a winner
        if depth == 0: 
            return None, None, board.evaluate()
        
        if color == PieceColor.BLACK:
            # Maximize eval value for "BLACK"
            max_val = -float('inf')
            start_coord = None
            best_move = None
            # Consider all paths for a given position
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    # Use deepycopy so original board is not affected when a 
                    # move is made
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    # Recurses a level below. "BLACK" will try to maximize the
                    # values of the nodes in this level
                    _, _, val = self._minimax(tmp_board, depth - 1, PieceColor.RED)
                    if val > max_val:
                        max_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, max_val

        if color == PieceColor.RED:
            # Minimize eval value for "RED"
            min_val = float('inf')
            start_coord = None
            best_move = None
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    # Recurses a level below. "RED" will try to minimize the
                    # values of the nodes in this level
                    _, _, val = self._minimax(tmp_board, depth - 1, PieceColor.BLACK)
                    if val < min_val:
                        min_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, min_val


# SIMULATION

@click.command()
@click.option('-n', '--n',  type=click.INT, default=10)
@click.option('-d', '--depth',  type=click.INT, default=3)
@click.option('-r', '--row',  type=click.INT, default=3)
def simulate(n, row, depth):
    """
        Test win rate of smartBot vs randomBot over the course of n games.

        Parameters:
            n (int): number of games
            row (int): row of pieces for board
            depth (int): depth for smartBot

        Returns:
            str: win-rate percentage
        """
    win = 0
    for _ in range(n):
        board = Game(row)
        bot1 = smartBot(board, PieceColor.BLACK, depth)
        bot2 = randomBot(board, PieceColor.RED)
        # Flag alternates to decide the turn of the bots
        flag = True
        while True:
            if flag:
                # Game ends when bot has no more move to play
                if not board.player_valid_moves(PieceColor.BLACK):
                    break
                else:
                    start_move, end_move = bot1.suggest_move()
                    board.move(PieceColor.BLACK, start_move, end_move)
                    flag = False
            else:
                if not board.player_valid_moves(PieceColor.RED):
                    win += 1
                    break
                else:
                    start_move, end_move = bot2.suggest_move()
                    board.move(PieceColor.RED, start_move, end_move)
                    flag = True
    print (f"Win rate of smart bot: {win // n * 100}%")


if __name__ == "__main__":
    simulate()