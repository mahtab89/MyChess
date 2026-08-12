from game import Game
from piece import Pawn, Queen


def test_kingside_castling_through_game():
    game = Game()

    game.board.board[7][5] = None
    game.board.board[7][6] = None

    king = game.board.board[7][4]
    rook = game.board.board[7][7]

    result = game.make_move((7, 4), (7, 6))

    assert result is True

    assert game.board.board[7][6] is king
    assert game.board.board[7][5] is rook

    assert game.board.board[7][4] is None
    assert game.board.board[7][7] is None

    assert king.has_moved is True
    assert rook.has_moved is True

    assert game.current_turn == "black"


def test_queenside_castling_through_game():
    game = Game()

    # Clear squares between king and rook
    game.board.board[7][1] = None
    game.board.board[7][2] = None
    game.board.board[7][3] = None

    king = game.board.board[7][4]
    rook = game.board.board[7][0]

    result = game.make_move((7, 4), (7, 2))

    assert result is True

    assert game.board.board[7][2] is king
    assert game.board.board[7][3] is rook

    assert game.board.board[7][4] is None
    assert game.board.board[7][0] is None

    assert king.has_moved is True
    assert rook.has_moved is True

    assert game.current_turn == "black"


def test_pawn_promotion_through_game():
    game = Game()

    for row in range(8):
        for col in range(8):
            game.board.board[row][col] = None

    pawn = Pawn("white")
    game.board.board[1][4] = pawn

    game.current_turn = "white"

    result = game.make_move((1, 4), (0, 4), "queen")

    assert result is True
    assert isinstance(game.board.board[0][4], Queen)
    assert game.board.board[1][4] is None
    assert game.current_turn == "black"
