from checkers import Game
from copy import deepcopy
import random

class randomBot():
    """
    Bot that makes random moves
    """
    def __init__(self, board, color):
        self._board = board
        self._color = color

    def suggest_move(self):
        """
        Returns suggested start and end move
        """
        rand_piece = random.choice(list(self._board.player_valid_moves(self._color).items()))
        rand_path = random.choice(rand_piece[1])
        return rand_piece[0], rand_path[-1]

class smartBot():
    """
    Bot that uses Minimax algo to suggest move based on curent position
    """
    def __init__(self, board, color):
        self._board = board
        self._color = color
    
    def suggest_move(self):
        move = self._minimax(self._board, 3, self._color)
        return move[:2]

    def _minimax(self, board, depth, color):
        if depth == 0 or board.get_winner(): 
            return None, None, board.evaluate()
        
        if color == "BLACK":
            max_val = -float('inf')
            start_coord = None
            best_move = None
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    _, _, val = self._minimax(tmp_board, depth - 1, "RED")
                    if val > max_val:
                        max_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, max_val

        if color == "RED":
            min_val = float('inf')
            start_coord = None
            best_move = None
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    _, _, val = self._minimax(tmp_board, depth - 1, "BLACK")
                    if val < min_val:
                        min_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, min_val

# SIMULATION
board = Game(3)
bot1 = smartBot(board, "BLACK")
bot2 = randomBot(board, "RED")
flag = True
while True:
    if flag:
        if not board.player_valid_moves("BLACK"):
            print("Red wins!")
            break
        else:
            start_move, end_move = bot1.suggest_move()
            print(start_move, end_move, "BLACK")
            board.move("BLACK", start_move, end_move)
            flag = False
    else:
        if not board.player_valid_moves("RED"):
            print("Black wins!")
            break
        else:
            start_move, end_move = bot2.suggest_move()
            print(start_move, end_move, "RED")
            board.move("RED", start_move, end_move)
            flag = True

def simulate(n):
    win = 0
    for _ in range(n):
        board = Game(3)
        bot1 = smartBot(board, "BLACK")
        bot2 = randomBot(board, "RED")
        flag = True
        while True:
            if flag:
                if not board.player_valid_moves("BLACK"):
                    break
                else:
                    start_move, end_move = bot1.suggest_move()
                    board.move("BLACK", start_move, end_move)
                    flag = False
            else:
                if not board.player_valid_moves("RED"):
                    win += 1
                    break
                else:
                    start_move, end_move = bot2.suggest_move()
                    board.move("RED", start_move, end_move)
                    flag = True
    return (win//n * 100)
# print(simulate(10))

