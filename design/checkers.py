"""
Classes for implementing a checkers game with varying board size (supports 6x6
up to 20x20).

Examples:
    1. Create new Checkers Board

        game = CheckersGame(nrows)

    2. Check whether a given move is legal

        game.is_valid_move(start, end)

    3. Obtain all valid moves of a piece:

        game.piece_valid_moves(coords)

    4. List of all possible moves a player can make

        game.player_valid_moves(color)

    5. Check whether there's a winner and who

        game.get_winner()
"""
from typing import Optional, List, Tuple, Dict, Set
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

    # number of rows and columns
    _nrows: int
    _ncols: int
        
    #
    # PUBLIC METHODS
    #

    def __init__(self, nrows: int, ncols: int):
        """
        Constructor

        Parameters:
            nrows (int): number of rows
            ncols (int): number of columns
        """
        self._grid = [[None] * ncols for _ in range(nrows)]
        self._nrows = nrows
        self._ncols = ncols

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
        """
        Moves the pieces at the start location to the end location.
    
        Parameters:
            start (tuple (int, int)): initial location of piece to be moved
            end (tuple (int, int)): final location of the piece
    
        Returns:
            None
        """
        raise NotImplementedError

    def board_to_str(self) -> List[List[str]]:
        """
        Returns the board as a list of list of strings.

        Parameters:
            None
        
        Returns:
            list[list[str]]: a list of list of strings with the same dimensions
            as the board. In each row, the values in the list will be " " 
            (no piece), "B" (black king piece), "b" (black non-king piece), "R"
            (red king piece), "r" (red non-king piece).
        """
        raise NotImplementedError

    def get_num_rows(self) -> int:
        """
        Returns the number of rows in the board.

        Parameters:
            None
        
        Returns:
            int: number of rows
        """
        raise NotImplementedError

    def get_num_cols(self) -> int:
        """
        Returns the number of columns in the board.

        Parameters:
            None
        
        Returns:
            int: number of cols
        """
        raise NotImplementedError

class CheckersGame:
    """
    Class for representing a game of checkers.    
    """

    #
    # PRIVATE ATTRIBUTES
    #
    
    # board of the game
    _board: Board

    # list of locations of pieces on the board
    _black_pieces: List[Tuple[int, int]]
    _red_pieces: List[Tuple[int, int]]

    # location of piece that is in the middle of a jump
    _jumping: Optional[Tuple[int, int]]

    # winner of the game if there is one
    _winner: Optional[PieceColor]

    # True if a draw has been offered, otherwise False
    _draw_offered: bool

    #
    # PUBLIC METHODS
    #
    
    def __init__(self, nrows: int):
        """
        Constructor

        Parameters:
            nrows (int): number of rows of pieces each player begins the game
            with
        """
        self._board = Board(2 * nrows + 2, 2 * nrows * 2)
        self._black_pieces = []
        self._red_pieces = []
        self._jumping = None
        self._winner = None
        self._draw_offered = False

        self._setup()

    def __str__(self) -> str:
        """
        Returns a basic string representation of the Game object's board.

        Parameters:
            None

        Returns:
            str: basic string representation fo the Game object's board
        """
        raise NotImplementedError

    def board_to_str(self) -> List[List[str]]:
        """
        Returns the game's board as a list of list of strings.

        Parameters:
            None

        Returns:
            list[list(str)]: A list of lists with the same dimensions as the
            board. In each row, the values in the list will be " " (no piece),
            "B" (black king piece), "b" (black non-king piece), "R" (red kings
            piece), "r" (red non-king piece).
        """
        raise NotImplementedError

    def setup(self) -> None:
        """
        Creates the board of the correct size and places the pieces on the
        correct squares of the board. Black pieces will be placed on the first n
        rows of the board and red pieces will be placed on the last n rows of
        the board.

        Parameters:
            None
        
        Returns:
            None
        """
        raise NotImplementedError
    
    def move(self, color: PieceColor, start: Tuple[int, int], 
            end: Tuple[int, int]) -> None:
        """
        Player of the given color inputs a position of a piece and a location to
        move the piece to. If the given move is valid, the move will be
        executed. Otherwise, the player wll be prompted to input a different
        move.

        Parameters:
            color (PieceColor): player color
            start: the position of piece to be moved
            end (tuple(int, int)): destination position

        Raises:
            Value if index is not on the board or the selected move is invalid

        Returns:
            None 
        """
        raise NotImplementedError

    def player_valid_moves(self, color: PieceColor) -> Dict[Tuple[int, int],
                                                List[List[Tuple[int, int]]]]:
        """
        Returns all the complete valid moves (jumps or non-jump moves) for all
        the available specified colored pieces.

        Parameters:
            color (PieceColor): player's color

        Returns:
            dict{tuple(int, int): list[list[tuple(int, int)]]}: dictionary of
            all the complete valid moves the player of the given color can make
            where the keys are the coordinates of a piece that can be moved and
            the values are the list of complete valid moves the player can make
            with each piece.
        """
        raise NotImplementedError

    def piece_valid_moves(self, coord: Tuple[int, int]) -> List[List
                                                            [Tuple[int, int]]]:
        """
        Returns all the complete valid moves for the given piece.

        Parameters:
            coord (tuple(int, int)): position of the given piece

        Returns:
            list[list[tuple(int, int)]]: list of all the possible moves the
            given piece can move to
        """
        raise NotImplementedError

    def is_valid_move(self, color: PieceColor, start: Tuple[int, int],
            end: Tuple[int, int]) -> bool:
        """
        Determines if the move is a possible move at the given color's player's
        current turn. 

        Parameters:
            color: color of the player
            start: coordinates of the piece to be moved
            end: coordinates of the destination location of the move

        Returns:
            bool: returns True if the given move is valid, otherwise, returns
            False
        """
        raise NotImplementedError

    def is_valid_dest(self, start: Tuple[int, int],
                      end: Tuple[int, int]) -> bool:
        """
        Given a location of a piece on the board and a location to move the
        piece to, determines if the move is valid or not, regardless of other
        pieces.

        Parameters:
            start (tuple(int, int)): position of the piece
            end (tuple(int, int)): destination position

        Returns:
            bool: returns True if the move is valid, otherwise, returns False
        """
        raise NotImplementedError

    def turn_incomplete(self) -> bool:
        """
        Boolean value for if the turn is incomplete, meaning the player has not
        completed all possible successive jumps.

        Parameters:
            None

        Returns:
            bool: True if the turn is incomplete, otherwise returns False
        """
        raise NotImplementedError
    
    def is_draw_offered(self) -> bool:
        """
        Returns true if a draw has been offered. Otherwise, returns false/

        Parameters:
            None

        Returns:
            bool: True if a draw has been offered, otherwise returns False
        """
        raise NotImplementedError

    def end_turn(self, color: PieceColor, cmd: str) -> None:
        """
        Method for ending a player's turn. The player can choose to resign,
        offer a draw, or simply end their current turn.

        Parameters:
            color (PieceColor): current player's color
            cmd (str): the player's command to end turn, resign, or offer draw

        Returns:
            None
        """
        raise NotImplementedError
    
    def accept_draw(self, cmd: str) -> None:
        """
        Method for player to either accept or decline a draw offered by the
        other player.

        Parameters:
            cmd (str): command for accepting or declining a draw
        
        Returns:
            None
        """
        raise NotImplementedError

    def get_winner(self) -> Optional[PieceColor]:
        """
        Find the winner of the game and the color won, if it exists.

        Parameters:
            None

        Returns:
            PieceColor or None: If there is a winner, return the color. If it is
            a tie, returns the string "DRAW". Otherwise, return None.
        """
        raise NotImplementedError
    
    def evaluate(self) -> float:
        """
        Evaluates the value of the current position. The more positive the value
        the more favorable the position is for player with the black pieces. The
        more negative the value, the more favorable the position is for player 
        with the red pieces. 

        Parameters:
            None

        Returns:
            value (float): value of current position
        """
        raise NotImplementedError

    #
    # PRIVATE METHODS
    #
    
    def _piece_move_to(self, start: Tuple[int, int],
                       end: Tuple[int, int]) -> None:
        """
        Moves the piece at the given location and updates the piece's positon on
        the board.

        Parameters:
            start (tuple(int, int)): the location of the piece to be moved
            end(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        raise NotImplementedError
    
    def _piece_jump_to(self, start: Tuple[int, int],
                       end: Tuple[int, int]) -> None:
        """
        Jumps with the piece at the given location and updates the piece's
        positon on the board.

        Parameters:
            start (tuple (int, int)): the lcoation of the piece to be moved
            end(tuple(int, int)): position the peice is moving to

        Raises:
            ValueError: Jump is invalid

        Returns:
            None
        """
        raise NotImplementedError

    def _get_all_jumps(self,
                        start: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
        """"
        Given a location on the board, returns a list of all the possible
        complete jumps the piece at that location can make where the coordinates
        of each sqaure the piece jumps to during the path is stored in a list. 

        Parameters:
            start_position: position of the peice

        Returns:
            list(list(tuple(int, int))): list of moves the piece can make
        """
        raise NotImplementedError
    
    def _get_all_non_jumps(self,
                        start: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
        """
        Given a piece on the board, returns a list of positions the piece can
        non-jump move to. This does not include places the piece can move to
        with a jump since that is in the _piece_valid_jump method. It will also
        take into consideration if the piece is a king or not.

        Parameters:
            start (tuple(int, int)): location of the piece

        Returns:
            list[list[tuple(int, int)]]: all possible places the given piece can
            non-jump move to
        """
        raise NotImplementedError

    def _get_complete_jumps(self, start: Tuple[int, int], color: PieceColor,
            king: bool,
            jumped: Set[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """
        Given a position on the board, a color, king status, and a set of
        locations that have already been jumped over, returns a list of all the
        possible complete moves that can be made from the given starting
        position.

        Parameters:
            start (tuple(int, int)): row and column information of the starting
            position on the board
            color (PieceColor): given color
            king (bool): if the piece is a king (can move in both directions)
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over.

        Returns:
            list[list[tuple(int, int)]]: list of moves a piece with the given
            details can make
        """
        raise NotImplementedError

    def _get_single_jumps(self, start: Tuple[int, int], color: PieceColor,
            king: bool, jumped: Set[Tuple[int, int]]) -> Dict[Tuple[int, int],
                                                              Tuple[int, int]]:
        """
        Given a starting position on the board, a color, king status, and a set
        of locations that have already been jumped over, returns a dictionary of
        the possible single jumps a move with the given details can make. The
        keys of the dictionary are the possible locations that can be jumped to
        and the values of the dictionary are sets of locations that must be
        jumped over to reach each destination.

        Parameters:
            start (tuple(int, int)): starting location on the board
            color (PieceColor): given piece color
            king (bool): king status of the given piece
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over

        Returns:
            dict{tuple(int, int): tuple(int, int)}: dictionary storing the
            possible end locations and the locations being jumped over
        """
        raise NotImplementedError

    def _require_jump(self, color: PieceColor) -> bool:
        """
        Given a player color returns a boolean if the player must make a jump
        with his or her turn. 

        Parameters:
            color (PieceColor): player color

        Returns:
            bool: if the player must make a jump with his or her turn
        """
        raise NotImplementedError
    
    def _composition(self) -> Tuple[int, int, int, int]:
        """
        Returns the number of kings and nonking pieces each player currently has
        on the board.

        Parameters:
            None

        Returns:
            tuple (int, int, int, int): tuple of four integers; the first
            integer is the number of black king pieces on the board, the second
            integer is the number of black nonking pieces on the board, the
            third integer is the number of red king pieces on the board, and the
            fourth integer is the number of red nonking pieces on the board. 
        """
        raise NotImplementedError
    
    def _check_promote(self, color: PieceColor, coord: Tuple[int, int]) -> None:
        """
        Checks if the piece at the given position should be promoted to a king.

        Parameters:
            color (PieceColor): color of the given piece
            coord (Tuple[int, int]): position of the given piece

        Returns:
            None
        """
        raise NotImplementedError

    def _update_winner(self) -> None:
        """
        Checks if a player has won the game or the game has reached a draw.

        Parameters:
            None

        Returns:
            None
        """
        raise NotImplementedError
