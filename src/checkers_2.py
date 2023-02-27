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
        return self._winner()

    def composition():
        raise NotImplementedError

    def evaluate():
        raise NotImplementedError
    
    #
    # PRIVATE METHODS
    #
    
    def _piece_move_to(self, start, end):
        piece = self._board.get(start)
        self._board.remove(start)
        self._board.set(end, piece)
    
    def _piece_jump_to(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        jump_over = (int((start_row + end_row) / 2), 
                int((start_col  + end_col) / 2))
        
        self._piece_move_to(self, start, end)
        self._borad.remove(jump_over)
    
    def _get_jumps(self, start):
        piece = self._board.get(start)
        return self._get_complete_jumps(start, piece.get_color(), piece.is_king())

    def _get_complete_jumps(self, start, color, king, jumped=set()):
        if self._get_single_jumps(start, color, king, jumped) == {}:
            return []
        else:
            paths = []
            for pos, gap in self._get_single_jumps(start, color, king,
                    jumped).items():
                sub_paths = self._get_complete_jumps(pos, color, king, jumped | {gap})
                if sub_paths == []:
                    paths.append([pos])
                else:
                    for sub_path in sub_paths:
                        paths.append([pos] + sub_path)
            return paths

    def _get_single_jumps(self, start, color, king, jumped):
        row, col = start
        valid = {}

        if color == PieceColor.BLACK or king:
            try:
                dest = (row + 2, col + 2)
                jump_over = (row + 1, col + 1)
                if (self._get(dest) is None
                        and self._get(jump_over) is not None
                        and self._get(jump_over).get_color() != color
                        and jump_over not in jumped):
                    valid[dest] = jump_over
            except IndexError:
                pass

            try:
                dest = (row + 2, col - 2)
                jump_over = (row + 1, col - 1)
                if (self._get(dest) is None
                        and self._get(jump_over) is not None
                        and self._get(jump_over).get_color() != color
                        and jump_over not in jumped):
                    valid[dest] = jump_over
            except IndexError:
                pass
            
        if color == PieceColor.RED or king:
            try:
                dest = (row - 2, col + 2)
                jump_over = (row - 1, col + 1)
                if (self._get(dest) is None
                        and self._get(jump_over) is not None
                        and self._get(jump_over).get_color() != color
                        and jump_over not in jumped):
                    valid[dest] = jump_over
            except IndexError:
                pass
                
            try:
                dest = (row - 2, col - 2)
                jump_over = (row - 1, col - 1)
                if (self._get(dest) is None
                        and self._get(jump_over) is not None
                        and self._get(jump_over).get_color() != color
                        and jump_over not in jumped):
                    valid[dest] = jump_over
            except IndexError:
                pass

        return valid

    def _get_non_jumps(self, start):
        valid_moves = []
        row, col = start
        piece = self._board.get(start)

        if piece.get_color() == PieceColor.BLACK or piece.is_king():
            try:
                dest = (row + 1, col + 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

            try:
                dest = (row + 1, col - 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

        if piece.get_color() == PieceColor.RED or piece.is_king():
            try:
                dest = (row - 1, col + 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

            try:
                dest = (row - 1, col - 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

        return valid_moves

    def _require_jump(self, color):
        if self.turn_incomplete() and self._jumping.get_color() == color:
            return True

        if color == PieceColor.BLACK:
            pieces = self._black_pieces
        else:
            pieces = self._red_pieces

        for piece in pieces:
            if self._piece_valid_jumps(piece.get_coord()):
                return True
        return False

    def _check_promote():
        raise NotImplementedError
