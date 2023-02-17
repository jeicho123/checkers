# Milestone 1 - Design
class Game:
    """
    Class for representing the board and rules of the game.

    Examples:
    1. Create new Checkers Board

        board = Game(rows)

    2. Check whether a given move is legal

        end_position in board._player_valid_moves(color)[start_position]

    3. Obtain all valid moves of a piece:

        if board._piece_valid_jumps(start_position, color):
            return board._piece_valid_jumps(start_position, color)
        else:
            return board._piece_valid_moves(start_position, color)

    4. List of all possible moves a player can make

        board._player_valid_moves(color)

    5. Check whether there's a winner and who

        board.get_winner()
    """
    def __init__(self, rows):
        """
            Constructor

        Parameters: 
            rows (int): the number of rows of pieces each player begins the game
            with
        """
        # int: number of rows of pieces each player begins with
        self._rows = rows

        # int: width of the game board
        self._width = 2 * rows + 2

        # int: height of the game board
        self._height = 2 * rows + 2

        # list[list[Piece]]: 2-dimensional list for storing the pieces
        self._board = []

        # list[Piece]: list of red pieces on the board
        self._red_pieces = []

        # list[Piece]: list of black pieces on the board
        self._black_pieces = []
        self.reset_board()

    # Public Methods

    def reset_board(self):
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
        
    def move(self, start_position, end_position):
        """
        User inputs a position of a piece and a location to move the piece to.
        If the given move is valid, the move will be executed. Otherwise, the
        player wll be prompted to input a different move.

        Parameters:
            start_position (tuple(int, int)): position of the piece to be moved
            end_position (tuple(int, int)): destination position

        Returns:
            None
        """
        raise NotImplementedError

    def get_winner(self):
        """
        Find the winner of the game and the color won, if it exists.

        Parameters:
            None

        Returns:
            str or None: If there is a winner, return the color. Otherwise,
            return None.
        """
        raise NotImplementedError

    def resign(self, color):
        """
        Player of the given color resigns; the other player is the winner.

        Parameters:
            color (str): color of the resigning player

        Returns:
            None
        """
        raise NotImplementedError

    def offer_draw(self, color):
        """
        Player of the given color offers a draw. The other player can choose to
        either accept or decline the draw.

        Parameters:
            color (str): color of the player offering a draw

        Returns:
            None
        """
        raise NotImplementedError

    # Private Methods

    def _piece_valid_jumps(self, start_position):
        """
        Given a position on the board, returns a list of positions the piece at
        the given position can jump to. It will also take into consideration if
        the piece is a king or not.

        Parameters: 
            start_position (tuple(int, int)): the position of the given piece
        
        Returns:
            list[tuple(int, int)]: all possible places the given piece can jump
            to in one jump
        """
        raise NotImplementedError

    def _piece_valid_moves(self, start_position):
        """
        Given a position on the board, returns a list of positions the piece at
        the given position can non-jump move to. This does not include places
        the piece can move to with a jump since that is in the _piece_valid_jump
        method. It will also take into consideration if the piece is a king or
        not.

        Parameters:
            start_position (tuple(int, int)): the position of the given piece

        Returns:
            list[tuple(int, int)]: all possible places the given piece can move
            to
        """
        raise NotImplementedError

    def _player_valid_moves(self, color):
        """
        Returns all the valid moves (jumps or non-jump moves) for all the
        available specified colored pieces.

        Parameters:
            color (str): player's color

        Returns:
            dict{piece: list[tuple(int, int)]}: dictionary of all the valid
            jumps or moves the player of the given color can make
        """
        raise NotImplementedError

    def _remove(self, position):
        """
        Removes the piece at the given position.

        Parameters:
            position (tuple): the position of the given piece to be removed

        Returns:
            Piece: the piece that was removed
        """
        raise NotImplementedError

    def _piece_move_to(self, start_position, end_position):
        """
        Moves the given piece and updates the piece's positon on the board.

        Parameters:
            start_position (tuple(int, int)): position of the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        raise NotImplementedError

    def _piece_jump_to(self, start_position, end_position):
        """
        Jumps with the given piece and updates the piece's positon on the board.

        Parameters:
            start_position (tuple(int, int)): position of the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        raise NotImplementedError

    def _become_king(self, start_position):
        """
        Updates the Piece to become a king.

        Parameters:
            start_position (tuple(int, int)): position of the piece to become a
            king

        Returns:
            None
        """

class Piece:
    """
    Class for representing a piece
    """
    def __init__(self, row, col, color, king=False):
        """
        Constructor

        Parameters:
            row (int): the row number of the piece
            col (int): the column number of the piece
            color (str): the color of the piece
            king (bool): if the piece is a king
        """
        # tuple (int, int): coordinates of the piece
        self._coord = (row, col)

        # str: color of the piece
        self._color = color

        # bool: if the piece is a king
        self._king = king

    # Public methods
    def get_color(self):
        """
        Returns the color of the piece.

        Parameters:
            None

        Returns:
            str: color of the piece
        """
        raise NotImplementedError

    def get_coord(self):
        """
        Returns the coordinates of the piece.

        Parameters:
            None

        Returns
            tuple(int, int): coordinates of the piece
        """
        raise NotImplementedError

    def is_king(self):
        """
        Returns if the piece is a king.

        Parameters:
            None

        Returns:
            bool: if the given piece is a king
        """
        raise NotImplementedError