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

    def get(self, coord):
        row, col = coord
        return self._grid[row][col]

    def set(self, coord, item):
        row, col = coord
        self._grid[row][col] = item
    
    def remove(self, coord):
        self.set(coord, None)

    def move(self, start, end):
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
        self._board = []
        self._black_pieces = []
        self._red_pieces = []
        self._jumping = None
        self._winner = None
        self._draw_offered = False
        self._reset(nrows)

    def __str__(self):
        board_string = ""
        for row in self.board_to_str():
            for sqaure in row:
                board_string += sqaure
            board_string += "\n"
        return board_string

    def board_to_str(self):
        return self._board.board_to_str()

    def _reset(self, nrows):
        self._board = Board(2 * nrows + 2)
        self._red_pieces = []
        self._black_pieces = []
        self._jumping = None
        self._winner = None
        self.draw_offered = False

        size = 2 * nrows + 2
        # steup game board
        for r in range(size):
            for c in range(size):
                if r < nrows and r % 2 != c % 2:
                    self._board.set((r, c), Piece(PieceColor.BLACK))
                    self._black_pieces.append((r, c))
                elif r >= size - nrows and r % 2 != c % 2:
                    self._board.set((r, c), Piece(PieceColor.RED))
                    self._red_pieces.append((r, c))
                else:
                    self._board.set((r, c), None)
