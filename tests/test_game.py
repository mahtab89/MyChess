from game import Game


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
