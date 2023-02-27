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
        return self._color

    def is_king(self):
        return self._king
    
    def promote(self):
        self._king = True

class Board:
    def __init(self, n):
        self._board = [[None] * n for _ in range(n)]

    def get(coord):
        row, col = coord
        return self._board[row][col]

    def set(coord, piece):
        row, col = coord
        self._board[row][col] = piece

    def move(start, end):
        piece = self.get(start)
        self.set(start, None)
        self.set(end, piece)