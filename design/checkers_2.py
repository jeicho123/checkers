from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
"""
Enum type for representing piece colors.
"""

class Piece:
    def __init__(self, color, king=False):
        self._color = color
        self._king = king

    def get_color(self):
        raise NotImplementedError

    def is_king(self):
        raise NotImplementedError
    
    def promote(self):
        raise NotImplementedError

class Board:
    def __init__(self, n):
        self._grid = [[None] * n for _ in range(n)]

    def get(self, coord):
        raise NotImplementedError

    def set(self, coord, item):
        raise NotImplementedError
    
    def remove(self, coord):
        raise NotImplementedError

    def move(self, start, end):
        raise NotImplementedError

    def board_to_str(self):
        raise NotImplementedError

class CheckersGame:
    def __init__(self, nrows):
        self._board = []
        self._black_pieces = []
        self._red_pieces = []
        self._jumping = None
        self._winner = None
        self._draw_offered = False
        self._reset(nrows)

    def __str__(self):
        raise NotImplementedError

    def board_to_str(self):
        raise NotImplementedError

    def _reset(self, nrows):
        raise NotImplementedError

    def player_valid_moves(self, color):
        raise NotImplementedError

    def piece_valid_moves(self, coord):
        raise NotImplementedError

    def is_valid_move(self, color, start, end):
        raise NotImplementedError

    def is_valid_dest(self, start, end):
        raise NotImplementedError

    def move(self, start, end):
        raise NotImplementedError

    def turn_incomplete(self):
        raise NotImplementedError

    def end_turn(self, color, cmd):
        raise NotImplementedError
    
    def accept_draw(self, cmd):
        raise NotImplementedError

    def get_winner(self):
        raise NotImplementedError

    def composition():
        raise NotImplementedError

    def evaluate():
        raise NotImplementedError
    
    #
    # PRIVATE METHODS
    #
    
    def _piece_move_to(self, start, end):
        raise NotImplementedError
    
    def _piece_jump_to(self, start, end):
        raise NotImplementedError

    def _get_jumps(self, start):
        raise NotImplementedError
    
    def _get_non_jumps(self, start):
        raise NotImplementedError

    def _get_complete_jumps(self, start, color, king, jumped):
        raise NotImplementedError

    def _get_single_jumps(self, start, color, king, jumped):
        raise NotImplementedError

    def _require_jump(self, color):
        raise NotImplementedError

    def _check_promote():
        raise NotImplementedError
