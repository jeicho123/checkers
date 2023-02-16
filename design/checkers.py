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
        self._create_new_board(self._rows)