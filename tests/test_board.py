from board import Board
from piece import Bishop, Knight, Pawn, Queen, Rook


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


def test_pawn_promotion_to_queen():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    pawn = Pawn("white")
    board.board[1][4] = pawn

    move = board.move_piece((1, 4), (0, 4), "queen")

    assert move is not None
    assert isinstance(board.board[0][4], Queen)
    assert board.board[1][4] is None


def test_pawn_promotion_choices():
    for promotion, piece_type in [
        ("queen", Queen),
        ("rook", Rook),
        ("bishop", Bishop),
        ("knight", Knight),
    ]:
        board = Board()

        for row in range(8):
            for col in range(8):
                board.board[row][col] = None

        board.board[1][4] = Pawn("white")
        board.move_piece((1, 4), (0, 4), promotion)

        assert isinstance(board.board[0][4], piece_type)


def test_promotion_requires_choices():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = Pawn("white")

    move = board.move_piece((1, 4), (0, 4))

    assert move is None


def test_undo_pawn_promotion():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    pawn = Pawn("white")
    board.board[1][4] = pawn

    move = board.move_piece((1, 4), (0, 4), "queen")

    assert isinstance(board.board[0][4], Queen)
    board.undo_move(move)

    assert board.board[1][4] is pawn
    assert board.board[0][4] is None
    assert pawn.has_moved is False
