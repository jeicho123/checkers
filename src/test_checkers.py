from checkers import Game
from checkers import PieceColor

def test_create_board():
    g = Game(2)
    assert len(g._black_pieces) == len(g._red_pieces) == 6

def test_valid_moves1():
    g = Game(3)
    assert g.is_valid((5, 0), (4, 1))

def test_valid_moves2():
    g = Game(3)
    assert g.is_valid((5, 0), (10, 1)) is False

def test_player_valid_moves():
    g = Game(2)
    g._remove((0, 1))
    g._remove((0, 3))
    g._remove((0, 5))
    g._remove((1, 0))
    g._remove((1, 2))
    g._remove((1, 4))
    
    assert g.player_valid_moves(PieceColor.BLACK) == {}

def test_block_win():
    g = Game(2)
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
    g = Game(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))

    assert (g._get((5, 0)) is not None and
            g._get((5, 0)).get_color() == PieceColor.BLACK)

def test_single_jump():
    g = Game(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))
    g.move(PieceColor.RED, (7, 2), (6, 1))
    g.move(PieceColor.BLACK, (5, 0), (7, 2))

    assert (g._get((7, 2)) is not None and
            g._get((7, 2)).get_color() == PieceColor.BLACK)

def test_multijump():
    g = Game(5)
    g.move(PieceColor.BLACK, (4, 1), (5, 0))
    g.move(PieceColor.RED, (7, 2), (6, 1))
    g._remove((9, 0))
    g.move(PieceColor.BLACK, (5, 0), (9, 0))

    assert (g._get((9, 0)) is not None and
            g._get((9, 0)).get_color() == PieceColor.BLACK)

def test_promote():
    g = Game(2)
    g.move(PieceColor.BLACK, (1, 0), (2, 1))
    g.move(PieceColor.BLACK, (2, 1), (3, 2))
    g._remove((0, 3))
    g.move(PieceColor.RED, (4, 3), (0, 3))

    assert g._get((0, 3)).is_king()