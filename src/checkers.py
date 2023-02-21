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

        self._jumping = None
        self._winner = None
        self.draw_offered = False

    # Public Methods

    def print(self):
        for row in self._board:
            text = ""
            for s in row:
                if s is None:
                    text += "_"
                else:
                    text += s.get_color()[0]
            print(text)

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
        self._board = []
        self._red_pieces = []
        self._black_pieces = []
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
            dict{tuple(int, int): list[list[tuple(int, int)]]}: dictionary of all the
            valid jumps or moves the player of the given color can make
        """
        all_moves = {}
        if self._jumping is not None:
            all_moves[self._jumping] = self._piece_valid_jumps(self._jumping)
            return all_moves

        if color == "BLACK":
            player_pieces = self._black_pieces
        else:
            player_pieces = self._red_pieces

        if self._require_jump(color):
            for piece in player_pieces:
                if self._piece_valid_jumps(piece) != [[]]:
                    all_moves[piece] = self._piece_valid_jumps(piece)
        else:
            for piece in player_pieces:
                if self._piece_valid_moves(piece) != []:
                    all_moves[piece] = self._piece_valid_moves(piece)
        return all_moves

    def piece_all_valid(self, piece):
        """
        Returns all the valid moves for the given piece.

        Parameters:
            piece (Piece): the given piece

        Returns:
            list[list[tuple(int, int)]]: list of all the possible moves the given piece can
            move to
        """
        if self._piece_valid_jumps(piece) != [[]]:
            return self._piece_valid_jumps(piece)
        else:
            return self._piece_valid_moves(piece)
        
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
        piece = self._get(start_position)
        if (piece is None
                or piece not in self.player_valid_moves(piece.get_color())):
            raise ValueError

        if self.is_valid(piece, end_position):  # complete move
            if self._require_jump(piece.get_color()): # jumping move
                for move in self.player_valid_moves(piece.get_color())[piece]:
                    if move[-1] == end_position:
                        for step in move:
                            self._piece_jump_to(piece, step)
                            self._jumping = None
            else: # non-jumping move
                self._piece_move_to(piece, end_position)
            
            row, _ = end_position
            if piece.get_color() == "BLACK" and row == self._height - 1:
                self._become_king(piece)
            elif piece.get_color() == "RED" and row == 0:
                self._become_king(piece)

        else:   # incomplete jumping moves
            for move in self.player_valid_moves(piece.get_color())[piece]:
                if end_position in move:
                    for step in move[: move.index(end_position)+1]:
                        if self._require_jump(piece.get_color()):
                            self._piece_jump_to(piece, step)
                            self._jumping = piece

    def end_turn(self, color, cmd):
        if cmd == "End Turn":
            pass
        elif cmd == "Resign":
            self.resign(color)
        elif cmd == "Offer Draw":
            self.offer_draw(color)

    def is_valid(self, piece, end_position):
        """
        Given a piece on the board and a location to move the piece to,
        determines if the move is valid or not.

        Parameters:
            piece (Piece): piece to be moved
            end_position (tuple(int, int)): destination position
        """
        for moves in self.piece_all_valid(piece):
            if moves[-1] == end_position:
                return True
        return False

    def get_winner(self):
        """
        Find the winner of the game and the color won, if it exists.

        Parameters:
            None

        Returns:
            str or None: If there is a winner, return the color. Otherwise,
            return None.
        """
        return self._winner

    def resign(self, color):
        """
        Player of the given color resigns; the other player is the winner.

        Parameters:
            color (str): color of the resigning player

        Returns:
            None
        """
        if color == "BLACK":
            self._winner = "RED"
        elif color == "RED":
            self._winner = "BLACK"

    def offer_draw(self, color):
        """
        Player of the given color offers a draw. The other player can choose to
        either accept or decline the draw.

        Parameters:
            color (str): color of the player offering a draw

        Returns:
            None
        """
        self.draw_offered = True

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
            color (str): player color

        Returns:
            bool: if the player must make a jump with his or her turn
        """
        if self._jumping is not None:
            return True

        if color == "BLACK":
            pieces = self._black_pieces
        else:
            pieces = self._red_pieces

        for piece in pieces:
            if self._piece_valid_jumps(piece) != [[]]:
                return True
        return False

    def _piece_valid_jumps(self, piece):
        """"
        Given a piece on the board, returns a list of all the possible complete
        jumps a piece can make where the coordinates of each sqaure the piece
        jumps to during the path is stored in a list. 

        Parameters:
            piece (Piece): given peice

        Returns:
            list(list(tuple(int, int))): list of paths the piece can take
        """
        return self._get_jumps(piece.get_coord(), piece.get_color(), piece.is_king())
    
    def _get_jumps(self, start_position, color, king):
        if self._single_jumps(start_position, color, king) == []:
            return [[]]
        else:
            paths = []
            for pos in self._single_jumps(start_position, color, king):
                paths += [[pos] + sub_path for sub_path in self._get_jumps(pos, color, king)]
            return paths

    def _single_jumps(self, start_position, color, king):
        row, col = start_position
        valid = []

        if color == "BLACK":
            try:
                if (self._get((row + 2, col + 2)) is None
                        and self._get((row + 1, col + 1)) is not None
                        and self._get((row + 1, col + 1)).get_color() == "RED"):
                    valid.append((row + 2, col + 2))
            except IndexError:
                pass

            try:
                if (self._get((row + 2, col - 2)) is None
                        and self._get((row + 1, col - 1)) is not None
                        and self._get((row + 1, col - 1)).get_color() == "RED"):
                    valid.append((row + 2, col - 2))
            except IndexError:
                pass
            
            if king:
                try:
                    if (self._get((row - 2, col + 2)) is None
                            and self._get((row - 1, col + 1)) is not None
                            and self._get((row - 1, col + 1)).get_color() == "RED"):
                        valid.append((row - 2, col + 2))
                except IndexError:
                    pass
                
                try:
                    if (self._get((row - 2, col - 2)) is None
                            and self._get((row - 1, col - 1)) is not None
                            and self._get((row - 1, col - 1)).get_color() == "RED"):
                        valid.append((row - 2, col - 2))
                except IndexError:
                    pass

        if color == "RED":
            try:
                if (self._get((row - 2, col + 2)) is None
                        and self._get((row - 1, col + 1)) is not None
                        and self._get((row - 1, col + 1)).get_color() == "BLACK"):
                    valid.append((row - 2, col + 2))
            except IndexError:
                pass

            try:
                if (self._get((row - 2, col - 2)) is None
                        and self._get((row - 1, col - 1)) is not None
                        and self._get((row - 1, col - 1)).get_color() == "BLACK"):
                    valid.append((row - 2, col - 2))
            except IndexError:
                pass

            if king:
                try:
                    if (self._get((row + 2, col + 2)) is None
                            and self._get((row + 1, col + 1)) is not None
                            and self._get((row + 1, col + 1)).get_color() == "BLACK"):
                        valid.append((row + 2, col + 2))
                except IndexError:
                    pass

                try:
                    if (self._get((row + 2, col - 2)) is None
                            and self._get((row + 1, col - 1)) is not None
                            and self._get((row + 1, col - 1)).get_color() == "BLACK"):
                        valid.append((row + 2, col - 2))
                except IndexError:
                    pass
        
        return valid

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
        valid_moves = []
        row, col = piece.get_coord()

        if piece.get_color() == "BLACK":
            try:
                if self._get((row + 1, col + 1)) is None:
                    valid_moves.append([(row + 1, col + 1)])
            except IndexError:
                pass

            try:
                if self._get((row + 1, col - 1)) is None:
                    valid_moves.append([(row + 1, col - 1)])
            except IndexError:
                pass

            if piece.is_king():
                try:
                    if self._get((row - 1, col + 1)) is None:
                        valid_moves.append([(row - 1, col + 1)])
                except IndexError:
                    pass

                try:
                    if self._get((row - 1, col - 1)) is None:
                        valid_moves.append([(row - 1, col - 1)])
                except IndexError:
                    pass

        if piece.get_color() == "RED":
            try:
                if self._get((row - 1, col + 1)) is None:
                    valid_moves.append([(row - 1, col + 1)])
            except IndexError:
                pass

            try:
                if self._get((row - 1, col - 1)) is None:
                    valid_moves.append([(row - 1, col - 1)])
            except IndexError:
                pass

            if piece.is_king():
                try:
                    if self._get((row + 1, col + 1)) is None:
                        valid_moves.append([(row - 1, col + 1)])
                except IndexError:
                    pass

                try:
                    if self._get((row + 1, col - 1)) is None:
                        valid_moves.append([(row - 1, col - 1)])
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
        assert isinstance(self._get(position), Piece)

        removed = self._get(position)
        self._board[row][col] = None
        if removed.get_color() == "BLACK":
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
        captured_position = int((start_row + end_row) / 2), int((start_col  + end_col) / 2)

        self._board[start_row][start_col] = None
        self._board[end_row][end_col] = piece
        piece.set_coord(end_position)
        self._remove(captured_position)

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
    def __init__(self, row, col, color):
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
        self._king = False

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

    def is_king(self):
        """
        Returns if the piece is a king.

        Parameters:
            None

        Returns:
            bool: if the given piece is a king
        """
        return self._king