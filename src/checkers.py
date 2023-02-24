"""
Classes for implementing a checkers game with varying board sizes
(supports 6x6 up to 20x20).

Examples:
    1. Create new Checkers Board

        board = Game(rows)

    2. Check whether a given move is legal

        board.is_valid(start_position, end_position)

    3. Obtain all valid moves of a piece:

        board.piece_all_valid(position)

    4. List of all possible moves a player can make

        board.player_valid_moves(color)

    5. Check whether there's a winner and who

        board.get_winner()
"""
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK"])
"""
Enum type for representing piece colors.
"""

class Game:
    """
    Class for representing the board and rules of the game.
    """
    def __init__(self, rows):
        """
            Constructor

            Parameters: 
                rows (int): the number of rows of pieces each player begins the
                game with
        """
        # int: number of rows of pieces each player begins with
        self._rows = rows

        # int: width and height of the game board
        self._width = 2 * rows + 2
        self._height = 2 * rows + 2

        # list[list[Piece]]: 2-dimensional list for storing the pieces
        self._board = []

        # list[Piece]: lists of pieces on the board
        self._red_pieces = []
        self._black_pieces = []

        # piece that is in the middle of a jump
        self._jumping = None

        # winner of the game if there is one
        self._winner = None

        # True if a draw has been offered, otherwise False
        self.draw_offered = False

        self.reset_board()

    #
    # PUBLIC METHODS
    #

    def __str__(self):
        """
        Returns a basic text representation of the Game object's board.

        Parameters:
            None

        Returns:
            str: basic text representation fo the Game object's board
        """
        string = []
        for row in self._board:
            text = ""
            for s in row:
                if s is None:
                    text += "_"
                elif s.get_color() == PieceColor.RED and s.is_king():
                    text += "R"
                elif s.get_color() == PieceColor.RED and not s.is_king():
                    text += "r"
                elif s.get_color() == PieceColor.BLACK and s.is_king():
                    text += "B"
                else:
                    text += "b"
            string.append(text)
        return "\n".join(string)

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
        # reset instance variables
        self._board = []
        self._red_pieces = []
        self._black_pieces = []
        self._jumping = None
        self._winner = None
        self.draw_offered = False

        # reset game board
        for r in range(self._height):
            row = []
            for c in range(self._width):
                if r < self._rows:
                    if r % 2 == c % 2:
                        row.append(None)
                    else:
                        piece = Piece(row=r, col=c, color=PieceColor.BLACK)
                        row.append(piece)
                        self._black_pieces.append(piece)
                elif r >= self._height - self._rows:
                    if r % 2 == c % 2:
                        row.append(None)
                    else:
                        piece = Piece(row=r, col=c,color=PieceColor.RED)
                        row.append(piece)
                        self._red_pieces.append(piece)
                else:
                    row.append(None)
            self._board.append(row)

    def player_valid_moves(self, color):
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
        all_moves = {}
        if self.turn_incomplete() and self._jumping.get_color() == color:
            all_moves[self._jumping] = self._piece_valid_jumps(self._jumping)
            return all_moves

        if color == PieceColor.BLACK:
            player_pieces = self._black_pieces
        else:
            player_pieces = self._red_pieces

        if self._require_jump(color):   # player must jump
            for piece in player_pieces:
                if self._piece_valid_jumps(piece.get_coord()):
                    all_moves[piece.get_coord()] = self._piece_valid_jumps(
                            piece.get_coord())
        else:   # player cannot jump
            for piece in player_pieces:
                if self._piece_valid_moves(piece.get_coord()):
                    all_moves[piece.get_coord()] = self._piece_valid_moves(
                            piece.get_coord())
        return all_moves

    def piece_all_valid(self, start_position):
        """
        Returns all the complete valid moves for the given piece.

        Parameters:
            start_position (tuple(int, int)): position of the given piece

        Returns:
            list[list[tuple(int, int)]]: list of all the possible moves the
            given piece can move to
        """
        if self._piece_valid_jumps(start_position):  # piece has valid jumps
            return self._piece_valid_jumps(start_position)
        else:   # piece has no valid jumps
            return self._piece_valid_moves(start_position)
        
    def move(self, color, start_position, end_position):
        """
        Player of the given color inputs a position of a piece and a location to
        move the piece to. If the given move is valid, the move will be
        executed. Otherwise, the player wll be prompted to input a different
        move.

        Parameters:
            color (PieceColor): player color
            start_position: the position of piece to be moved
            end_position (tuple(int, int)): destination position

        Returns:
            None

        Raises:
            IndexError: if index is not on the board
            ValueError: selected move is invalid
        """
        print()
        print(self)
        print(color, start_position, end_position)
        print()
        if not self.valid_move(color, start_position, end_position):
            
            print(color, start_position, end_position)
            raise ValueError
        piece = self._get(start_position)

        if self._require_jump(color): # jumping move
            for move in self.piece_all_valid(start_position):
                if end_position in move:
                    if end_position == move[-1]:    # complete jumping move
                        self._jumping = None
                    else:   # incomplete jumping move
                        self._jumping = piece

                    for step in move[: move.index(end_position) + 1]:
                        self._piece_jump_to(piece, step)

        else:   #non-jump move
            self._piece_move_to(piece, end_position)
            self._jumping = None
        # check for promotion
        self._check_promote(piece)

        # update winner
        if color == PieceColor.BLACK and self.player_valid_moves(
                PieceColor.RED) == {}:
            self._winner == PieceColor.BLACK
        elif color == PieceColor.RED and self.player_valid_moves(
                PieceColor.BLACK)  == {}:
            self._winner = PieceColor.RED
        print()
        print(self)
        print()

    def turn_incomplete(self):
        """
        Boolean value for if the turn is incomplete, meaning the player has not
        completed all possible successive jumps.

        Parameters:
            None

        Returns:
            bool: True if the turn is incomplete, otherwise returns False
        """
        return self._jumping is not None

    def end_turn(self, color, cmd):
        """
        Method for ending a player's turn. The player can choose to resign,
        offer a draw, or simply end their current turn.

        Parameters:
            color (PieceColor): current player's color
            cmd (str): the player's command to end turn, resign, or offer draw

        Returns:
            None
        """
        if cmd == "End Turn":   
            pass
        elif cmd == "Resign":
            self.resign(color)
        elif cmd == "Offer Draw":
            self.offer_draw()

    def valid_move(self, color, start_position, end_position):
        """
        Determines if the move is a possible move at the given color's player's
        current turn. 

        Parameters:
            color: color of the player
            start_position: coordinates of the piece to be moved
            end_position: coordinates of the destination location of the move

        Returns:
            bool: returns True if the given move is valid, otherwise, returns
            False
        """
        return (start_position in self.player_valid_moves(color) and
                self.is_valid(start_position, end_position))

    def is_valid(self, start_position, end_position):
        """
        Given a location of a piece on the board and a location to move the
        piece to, determines if the move is valid or not, regardless of other
        pieces.

        Parameters:
            start_position (tuple(int, int)): position of the piece
            end_position (tuple(int, int)): destination position

        Returns:
            bool: returns True if the move is valid, otherwise, returns False
        """
        for moves in self.piece_all_valid(start_position):
            if moves[-1] == end_position:   # end_position is the last move
                return True
        return False

    def get_winner(self):
        """
        Find the winner of the game and the color won, if it exists.

        Parameters:
            None

        Returns:
            Piece or str or None: If there is a winner, return the color. If it
            is a tie, returns the string "DRAW". Otherwise, return None.
        """
        return self._winner

    def resign(self, color):
        """
        Player of the given color resigns; the other player is the winner.

        Parameters:
            color (PieceColor): color of the resigning player

        Returns:
            None
        """
        if color == PieceColor.BLACK:
            self._winner = PieceColor.RED
        elif color == PieceColor.RED:
            self._winner = PieceColor.BLACK

    def offer_draw(self):
        """
        Player offers a draw. The other player can choose to either accept or
        decline the draw.

        Parameters:
            None

        Returns:
            None
        """
        self.draw_offered = True

    def accept_draw(self, cmd):
        """
        Method for player to either accept or decline a draw offered by the
        other player.

        Parameters:
            cmd (str): command for accepting or declining a draw
        
        Returns:
            None
        """
        if cmd == "Accept":
            self._winner = "DRAW"
        elif cmd == "Decline":
            self.draw_offered = False

    def composition(self, color):
        """
        Given a player's color, returns the number of kings and nonking pieces
        the player currently has on the board.

        Parameters:
            color (PieceColor): given player color

        Returns:
            tuple (int, int): tuple of two integers; the first integer is the
            number of king pieces the player has, the second integer is the
            number of nonking pieces the player has
        """
        king, nonking = 0, 0
        if color == PieceColor.BLACK:
            for piece in self._black_pieces:
                if piece.is_king():
                    king += 1
                else:
                    nonking += 1
        elif color == PieceColor.RED:
            for piece in self._red_pieces:
                if piece.is_king():
                    king += 1
                else:
                    nonking += 1
        return king, nonking
    
    def evaluate(self):
        """
        Evaluates the value of the current position. The more positive the value
        the more favorable the position is for player with the black pieces. The
        more negative the value, the more favorable the position is for player 
        with the red pieces. 

        Parameters:
            None

        Returns:
            value (int): value of current position
        """
        black_king, black_nonking = self.composition(PieceColor.BLACK)
        red_king, red_nonking = self.composition(PieceColor.RED)
        value = (black_nonking - red_nonking) + (0.5 * black_king - 
                                                0.5 * red_king)
        return value

    def board_to_str(self):
        """
        Returns the board as a list of list of strings.

        Parameters:
            None

        Returns:
            list[list(str)]: A list of lists with the same dimensions as the
            board. In each row, the values in the list will be " " (no piece),
            "B" (black king piece), "b" (black non-king piece), "R" (red kings
            piece), "r" (red non-king piece).
        """
        grid = []
        for row in self._board:
            new_row = []
            for square in row:
                if square is None:
                    new_row.append(" ")
                else:
                    if square.get_color() == PieceColor.BLACK:
                        if square.is_king():
                            new_row.append("B")
                        else:
                            new_row.append("b")
                    else:
                        if square.is_king():
                            new_row.append("R")
                        else:
                            new_row.append("r")
            grid.append(new_row)
        return grid

    #
    # PRIVATE METHODS
    #

    def _get(self, position):
        """
        Returns the piece at the given position on the board.

        Parameters:
            position (tuple(int, int)): position on the board

        Returns:
            Piece: Piece object at that location on the board
        """
        row, col = position
        if not 0 <= row < self._height:
            raise IndexError
        if not 0 <= col < self._width:
            raise IndexError
        return self._board[row][col]

    def _require_jump(self, color):
        """
        Given a player color returns a boolean if the player must make a jump
        with his or her turn. 

        Parameters:
            color (PieceColor): player color

        Returns:
            bool: if the player must make a jump with his or her turn
        """
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

    def _piece_valid_jumps(self, start_position):
        """"
        Given a location on the board, returns a list of all the possible
        complete jumps the piece at that location can make where the coordinates
        of each sqaure the piece jumps to during the path is stored in a list. 

        Parameters:
            start_position: position of the peice

        Returns:
            list(list(tuple(int, int))): list of moves the piece can make
        """
        piece = self._get(start_position)
        return self._get_jumps(start_position, piece.get_color(), 
                piece.is_king())
    
    def _get_jumps(self, start_position, color, king, jumped=set()):
        """
        Given a position on the board, a color, king status, and a set of
        locations that have already been jumped over, returns a list of all the
        possible complete moves that can be made from the given starting
        position.

        Parameters:
            start_position (tuple(int, int)): row and column information of the
                starting position on the board
            color (PieceColor): given color
            king (bool): if the piece is a king (can move in both directions)
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over.

        Returns:
            list[list[tuple(int, int)]]: list of moves a piece with the given
            details can make
        """
        if self._single_jumps(start_position, color, king, jumped) == {}:
            return []
        else:
            paths = []
            for pos, gap in self._single_jumps(start_position, color, king,
                    jumped).items():
                sub_paths = self._get_jumps(pos, color, king, jumped | {gap})
                if sub_paths == []:
                    paths.append([pos])
                else:
                    for sub_path in sub_paths:
                        paths.append([pos] + sub_path)
            return paths

    def _single_jumps(self, start_position, color, king, jumped):
        """
        Given a starting position on the board, a color, king status, and a set
        of locations that have already been jumped over, returns a dictionary of
        the possible single jumps a move with the given details can make. The
        keys of the dictionary are the possible locations that can be jumped to
        and the values of the dictionary are sets of locations that must be
        jumped over to reach each destination.

        Parameters:
            start_position (tuple(int, int)): starting location on the board
            color (PieceColor): given piece color
            king (bool): king status of the given piece
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over

        Returns:
            dict{tuple(int, int): tuple(int, int)}: dictionary storing the
            possible end locations and the locations being jumped over
        """
        row, col = start_position
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

    def _piece_valid_moves(self, start_position):
        """
        Given a piece on the board, returns a list of positions the piece can
        non-jump move to. This does not include places the piece can move to
        with a jump since that is in the _piece_valid_jump method. It will also
        take into consideration if the piece is a king or not.

        Parameters:
            start_position (tuple(int, int)): location of the piece

        Returns:
            list[list[tuple(int, int)]]: all possible places the given piece can
            non-jump move to
        """
        valid_moves = []
        row, col = start_position
        piece = self._get(start_position)

        if piece.get_color() == PieceColor.BLACK or piece.is_king():
            try:
                dest = (row + 1, col + 1)
                if self._get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

            try:
                dest = (row + 1, col - 1)
                if self._get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

        if piece.get_color() == PieceColor.RED or piece.is_king():
            try:
                dest = (row - 1, col + 1)
                if self._get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

            try:
                dest = (row - 1, col - 1)
                if self._get(dest) is None:
                    valid_moves.append([dest])
            except IndexError:
                pass

        return valid_moves

    def _remove(self, position):
        """
        Removes the piece at the given position.

        Parameters:
            position (tuple): the position of the given piece to be removed

        Returns:
            None
        """
        row, col = position
        if not isinstance(self._get(position), Piece):
            raise ValueError

        removed = self._get(position)
        self._board[row][col] = None
        if removed.get_color() == PieceColor.BLACK:
            self._black_pieces.remove(removed)
        else:
            self._red_pieces.remove(removed)

    def _piece_move_to(self, piece, end_position):
        """
        Moves the given piece and updates the piece's positon on the board.

        Parameters:
            piece (Piece): the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        start_row, start_col = piece.get_coord()
        end_row, end_col = end_position

        self._board[start_row][start_col] = None
        self._board[end_row][end_col] = piece
        piece.set_coord(end_position)

    def _piece_jump_to(self, piece, end_position):
        """
        Jumps with the given piece and updates the piece's positon on the board.

        Parameters:
            piece (Piece): the piece to be moved
            end_position(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        start_row, start_col = piece.get_coord()
        end_row, end_col = end_position
        jump_over = (int((start_row + end_row) / 2), 
                int((start_col  + end_col) / 2))

        self._piece_move_to(piece, end_position)
        self._remove(jump_over)

    def _check_promote(self, piece):
        """
        Checks if the given Piece must be promoted to a king.

        Parameters:
            piece (Piece): the piece to become a king

        Returns:
            None
        """
        row, _ = piece.get_coord()
        color = piece.get_color()
        if row == 0 and color == PieceColor.RED:
            piece.promote()
        elif row == self._height - 1 and color == PieceColor.BLACK:
            piece.promote()

class Piece:
    """
    Class for representing a piece
    """
    def __init__(self, row, col, color):
        """
        Constructor

        Parameters:
            row (int): the row number of the piece
            col (int): the column number of the piece
            color (PieceColor): the color of the piece
            king (bool): if the piece is a king
        """
        # tuple (int, int): coordinates of the piece
        self._coord = (row, col)

        # PieceColor: color of the piece
        self._color = color

        # bool: if the piece is a king
        self._king = False

    # Public methods
    def get_color(self):
        """
        Returns the color of the piece.

        Parameters:
            None

        Returns:
            PieceColor: color of the piece
        """
        return self._color

    def get_coord(self):
        """
        Returns the coordinates of the piece.

        Parameters:
            None

        Returns:
            tuple(int, int): coordinates of the piece
        """
        return self._coord

    def set_coord(self, new_coord):
        """
        Sets the coordinates of the piece to the new set of coordinates.

        Parameters:
            new_coord (tuple(int, int)): new coordinates of piece

        Returns:
            None
        """
        self._coord = new_coord

    def promote(self):
        """
        Promotes the given piece to become a king.

        Parameters:
            None

        Returns:
            None
        """
        self._king = True

    def is_king(self):
        """
        Returns if the piece is a king.

        Parameters:
            None

        Returns:
            bool: if the given piece is a king
        """
        return self._king
