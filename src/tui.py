from checkers import Game, Piece
#from bot import randomBot, smartBot

def print_board(board):
    """
    Prints the board to the screen

    Input: 
        board: board to print

    Returns: None
    """
    final = []
    grid = board.board_to_str()
    for r, row in enumerate(grid):
        string = ""
        for c, col in enumerate(row):
            if r % 2 == c % 2:
                string += "[L]"
            else:
                string += "[B]"
        final.append(string)
    return "\n".join(final)
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
        """