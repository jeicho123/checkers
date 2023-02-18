class Game:
    """
    Class for representing the board and rules of the game.

    Examples:
    1. Create new Checkers Board

        board = Game(rows)

    2. Check whether a given move is legal

        board.is_valid(piece, end_position)

    3. Obtain all valid moves of a piece:

        board.piece_all_valid(piece)

    4. List of all possible moves a player can make

        board.player_valid_moves(color)

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
        for r in range(self._height):
            row = []
            for c in range(self._width):
                if r < self._rows:
                    if r % 2 == c % 2:
                        row.append(None)
                    else:
                        piece = Piece(row=r, col=c, color="BLACK")
                        row.append(piece)
                        self._black_pieces.append(piece)
                elif r >= self._height - self._rows:
                    if r % 2 == c % 2:
                        row.append(None)
                    else:
                        piece = Piece(row=r, col=c,color="RED")
                        row.append(piece)
                        self._red_pieces.append(piece)
                else:
                    row.append(None)
            self._board.append(row)

    def player_valid_moves(self, color):
        """
        Returns all the valid moves (jumps or non-jump moves) for all the
        available specified colored pieces.

        Parameters:
            color (str): player's color

        Returns:
            dict{tuple(int, int): list[tuple(int, int)]}: dictionary of all the
            valid jumps or moves the player of the given color can make
        """
        raise NotImplementedError

    def piece_all_valid(self, piece):
        """
        Returns all the valid moves for the given piece.

        Parameters:
            piece (Piece): the given piece

        Returns:
            list[tuple(int, int)]: list of all the positions the given piece can
            move to
        """
        raise NotImplementedError
        
    def move(self, start_position, end_position):
        """
        User inputs a position of a piece and a location to move the piece to.
        If the given move is valid, the move will be executed. Otherwise, the
        player wll be prompted to input a different move.

        Parameters:
            start_position: the position of piece to be moved
            end_position (tuple(int, int)): destination position

        Returns:
            None
        """
        raise NotImplementedError

    def is_valid(self, piece, end_position):
        """
        Given a piece on the board and a location to move the piece to,
        determines if the move is valid or not.

        Parameters:
            piece (Piece): piece to be moved
            end_position (tuple(int, int)): destination position
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

    def _get(self, position):
        """
        Returns the piece at the given position on the board.

        Parameters:
            position (tuple(int, int)): position on the board

        Returns:
            Piece: Piece object at that location on the board
        """
        row, col = position
        return self._board[row][col]

    def _require_jump(self, color):
        """
        Given a player color returns a boolean if the player must make a jump
        with his or her turn. 

        Parameters:
            color (str): player color

        Returns:
            bool: if the player must make a jump with his or her turn
        """
        raise NotImplementedError

    def _piece_valid_jumps(self, piece):
        """
        Given a piece on the board, returns a list of positions the piece at can
        jump to. It will also take into consideration if the piece is a king or
        not.

        Parameters: 
            piece (Piece): the given piece
        
        Returns:
            list[tuple(int, int)]: all possible places the given piece can jump
            to in one jump
        """
        row, col = piece.get_coord()
        valid_jumps = []

        if piece.get_color() == "BLACK":

        

    def _piece_valid_moves(self, piece):
        """
        Given a piece on the board, returns a list of positions the piece can
        non-jump move to. This does not include places the piece can move to
        with a jump since that is in the _piece_valid_jump method. It will also
        take into consideration if the piece is a king or not.

        Parameters:
            piece (Piece): the given piece

        Returns:
            list[tuple(int, int)]: all possible places the given piece can move
            to
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
        row, col = positon
        assert isinstance(self._board[row][col], Piece)

        removed = self._get((row, col))
        self._board[row][col] = None
        if removed.get_color() == "BLACK":
            self._black_pieces.remove(removed)
        else:
            self._red_piece.remove(removed)

        return removed
        

    def _piece_move_to(self, piece, end_position):
        """
        Moves the given piece and updates the piece's positon on the board.

        Parameters:
            piece (Piece): the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        raise NotImplementedError

    def _piece_jump_to(self, piece, end_position):
        """
        Jumps with the given piece and updates the piece's positon on the board.

        Parameters:
            piece (Piece): the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        raise NotImplementedError

    def _become_king(self, piece):
        """
        Updates the Piece to become a king.

        Parameters:
            piece (Piece): the piece to become a king

        Returns:
            None
        """
        piece._king = True 

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
        return self._color

    def get_coord(self):
        """
        Returns the coordinates of the piece.

        Parameters:
            None

        Returns
            tuple(int, int): coordinates of the piece
        """
        return self._coord

    def is_king(self):
        """
        Returns if the piece is a king.

        Parameters:
            None

        Returns:
            bool: if the given piece is a king
        """
        return self._king