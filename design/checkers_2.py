from Typing import Optional, List
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
"""
Enum type for representing piece colors.
"""

class Piece:
    """
    Class for representing a piece.
    """

    #
    # PRIVATE ATTRIBUTES
    #
        
    # color of the piece        
    _color: PieceColor

    # if the piece is a king
    _king: PieceColor

    #
    # PUBLIC METHODS
    #
    
    def __init__(self, color: PieceColor):
        """
        Constructor
    
        Parameters:
            color (PieceColor): color of the piece

        Returns:
            None
        """
        self._color = color
        self._king = False

    def get_color(self) -> PieceColor:
        """
        Gets the color of the piece.
    
        Parameters:
            None

        Returns:
            PieceColor: color of the given piece
        """
        raise NotImplementedError

    def is_king(self) -> bool:
        """
        Returns if the piece is a king or not.
    
        Parameters:
            None
    
        Returns:
            bool: returns True if the piece is a king, otherwise, returns False
        """
        raise NotImplementedError
    
    def promote(self) -> None:
        """
        Promotes the piece to a king.
    
        Parameters:
            None
    
        Returns:
            None
        """
        raise NotImplementedError

class Board:
    """
    Class for representing a rectangular board.
    """

    #
    # PRIVATE ATTRIBUTES
    #
        
    # the board itself
    _grid: List[List[Optional[Piece]]]
        
    #
    # PUBLIC METHODS
    #

    def __init__(self, nrows: int, ncols: int):
        """
        Constructor

        Parameters:
            nrows (int): number of rows
            ncols (int): number of columns
        
        Returns:
            None
        """
        self._grid = [[None] * ncols for _ in range(nrows)]

    def get(self, coord: Tuple[int, int]) -> Optional[Piece]:
        """
        Gets the piece at the given location if there is one.
    
        Parameters:
            coord (tuple(int, int)): location on the board
        
        Raises:
            ValueError: If the given location is not valid
        
        Returns:
            Optional[Piece]: the piece at the location if there is one
        """
        raise NotImplementedError

    def set(self, coord: Tuple[int, int], piece: Piece) -> None:
        """
        Sets the location on the board to the given piece.

        Parameters:
            coord (tuple (int, int)): location on the board
            piece (Piece): given piece to be set

        Raises:
            ValueError: If the given location is invalid or there is alreay a
            piece at the given location
    
        Returns:
            None
        """
        raise NotImplementedError
    
    def remove(self, coord: Tuple[int, int]) -> None:
        """
        Removes the piece at the given location.

        Paramters:
            coord (tuple (int, int)): location on the board
    
        Raises:
            ValueError: If the given location is invalid or if there is not a
            piece at the given location
    
        Returns:
            None
        """
        raise NotImplementedError

    def move(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
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
