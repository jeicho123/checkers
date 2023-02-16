# Milestone 1 - Design
class Game:
    """
    Class for representing the board and rules of the game.
    """
    def __init__(self, rows):
        """
            Constructor

        Parameters: 
            rows (int): the number of rows of pieces each player begins the game
            with
        """

        self._rows = rows   # number of rows of pieces each player begins with
        self._width = 2 * rows + 2  # width of the game board
        self._height = 2 * rows + 2 # height of the game board
        self._board = []    # 2D array for storing the pieces
        self._red_pieces = []   # list of red pieces on the board
        self._black_pieces = [] # list of black pieces on the board
        self._create_new_board()

    def create_new_board(self):
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

        Input:
            None

        Returns:
            Optional[str]: If there is a winner, return the color. Otherwise,
            return None.
        """