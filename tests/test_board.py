from board import Board


def test_board_initial_pos():
    board = Board()

    assert board.board[0][0].color == "black"
    assert board.board[0][4].color == "black"

    assert board.board[7][0].color == "white"
    assert board.board[7][4].color == "white"

    assert board.board[2][2] is None


def test_move_piece():
    board = Board()
    move = board.move_piece((6, 4), (4, 4))

    assert move is not None
    assert board.board[6][4] is None
    assert board.board[4][4] is not None


def test_undo_move():
    board = Board()
    move = board.move_piece((6, 4), (4, 4))

    board.undo_move(move)

    assert board.board[6][4] is not None
    assert board.board[4][4] is None


def test_has_moved():
    board = Board()
    piece = board.board[6][4]

    assert piece.has_moved is False

    move = board.move_piece((6, 4), (4, 4))
    assert piece.has_moved is True

    board.undo_move(move)
    assert piece.has_moved is False
