from checkers import CheckersGame, PieceColor

def test_create_board():
    g = CheckersGame(2)
    assert len(g._black_piece_coords) == len(g._red_piece_coords) == 6

def test_valid_move_1():
    g = CheckersGame(3)
    assert g.is_valid_dest((5, 0), (4, 1))

def test_valid_moves_2():
    g = CheckersGame(3)
    assert g.is_valid_dest((5, 0), (10, 1)) is False

def test_no_pieces():
    game = CheckersGame(2)
    game.move(PieceColor.RED, (4, 1), (3, 2))
    game.move(PieceColor.RED, (3, 2), (2, 1))
    game.move(PieceColor.BLACK, (1, 2), (3, 0))
    game.move(PieceColor.RED, (5, 2), (4, 1))
    game.move(PieceColor.BLACK, (3, 0), (5, 2))
    game.move(PieceColor.RED, (5, 0), (4, 1))
    game.move(PieceColor.BLACK, (5, 2), (3, 0))
    game.move(PieceColor.RED, (4, 3), (3, 4))
    game.move(PieceColor.RED, (3, 4), (2, 3))
    game.move(PieceColor.BLACK, (1, 4), (3, 2))
    game.move(PieceColor.RED, (5, 4), (4, 3))
    game.move(PieceColor.BLACK, (3, 2), (5, 4))
    game.move(PieceColor.RED, (4, 5), (3, 4))
    game.move(PieceColor.RED, (3, 4), (2, 3))
    game.move(PieceColor.RED, (2, 3), (1, 2))
    game.move(PieceColor.BLACK, (0, 1), (2, 3))

    assert game.get_winner() == PieceColor.BLACK

def test_block_win():
    g = CheckersGame(2)
    g.move(PieceColor.RED, (4, 1), (3, 0))
    g.move(PieceColor.RED, (3, 0), (2, 1))
    g.move(PieceColor.RED, (4, 3), (3, 2))
    g.move(PieceColor.RED, (3, 2), (2, 3))
    g.move(PieceColor.RED, (4, 5), (3, 4))
    g.move(PieceColor.RED, (3, 4), (2, 5))
    g.move(PieceColor.RED, (5, 0), (4, 1))
    g.move(PieceColor.RED, (4, 1), (3, 0))
    g.move(PieceColor.RED, (5, 2), (4, 3))
    g.move(PieceColor.RED, (4, 3), (3, 2))
    g.move(PieceColor.RED, (5, 4), (4, 5))
    g.move(PieceColor.RED, (4, 5), (3, 4))

    assert g.get_winner() == PieceColor.RED

def test_move():
    g = CheckersGame(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))

    assert (g._board.get((5, 0)) is not None and
            g._board.get((5, 0)).get_color() == PieceColor.BLACK)

def test_single_jump():
    g = CheckersGame(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))
    g.move(PieceColor.RED, (7, 2), (6, 1))
    g.move(PieceColor.BLACK, (5, 0), (7, 2))

    assert (g._board.get((7, 2)) is not None and
            g._board.get((7, 2)).get_color() == PieceColor.BLACK)

def test_multijump():
    g = CheckersGame(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))
    g.move(PieceColor.RED, (7, 2), (6, 1))
    g._board.remove((9, 0))
    g.move(PieceColor.BLACK, (5, 0), (9, 0))

    assert (g._board.get((9, 0)) is not None and
            g._board.get((9, 0)).get_color() == PieceColor.BLACK)

def test_promote():
    g = CheckersGame(2)
    g.move(PieceColor.BLACK, (1, 0), (2, 1))
    g.move(PieceColor.BLACK, (2, 1), (3, 2))
    g._board.remove((0, 3))
    g.move(PieceColor.RED, (4, 3), (0, 3))

    assert g._board.get((0, 3)).is_king()