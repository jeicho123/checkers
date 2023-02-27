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
    def __init__(self, n):
        self._grid = [[None] * n for _ in range(n)]

    def get(coord):
        row, col = coord
        return self._grid[row][col]

    def set(coord, item):
        row, col = coord
        self._grid[row][col] = item
    
    def remove(coord):
        self.set(coord, None)

    def move(start, end):
        piece = self.get(start)
        self.set(start, None)
        self.set(end, piece)

    def board_to_str(self):
        grid = []
        for row in self._grid:
            new_row = []
            for square in row:
                if square is None:
                    new_row.append(" ")
                elif square.get_color() == PieceColor.BLACK and square.is_king():
                    new_row.append("B")
                elif square.get_color() == PieceColor.BLACK and not square.is_king():
                    new_row.append("b")
                elif square.get_color() == PieceColor.RED and square.is_king():
                    new_row.append("R")
                else:
                    new_row.append("r")
            grid.append(new_row)
        return grid

class CheckersGame:
    def __init__(self, nrows):
        self._board = Board(2 * nrows + 2)