from board import Board
from piece import Bishop, Knight, Pawn, Queen, Rook
from move import Move


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


def test_pawn_promotion_with_capture_and_undo():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    pawn = Pawn("white")
    captured_rook = Rook("black")

    board.board[1][4] = pawn
    board.board[0][5] = captured_rook

    move = board.move_piece((1, 4), (0, 5), "queen")

    assert move is not None
    assert isinstance(board.board[0][5], Queen)
    assert board.board[1][4] is None

    assert move.captured_piece is captured_rook
    assert move.promotion == "queen"

    board.undo_move(move)

    assert board.board[1][4] is pawn
    assert board.board[0][5] is captured_rook
    assert pawn.has_moved is False


def test_en_passant_execution():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[3][4] = white_pawn
    board.board[3][3] = black_pawn

    last_move = Move((1, 3), (3, 3), None, False)
    last_move.piece = black_pawn

    move_history = [last_move]

    move = board.move_piece((3, 4), (2, 3), move_history=move_history)

    assert move is not None

    assert board.board[2][3] is white_pawn
    assert board.board[3][4] is None
    assert board.board[3][3] is None


def test_undo_en_passant():
    board = Board()

    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[3][4] = white_pawn
    board.board[3][3] = black_pawn

    last_move = Move((1, 3), (3, 3), None, False)
    last_move.piece = black_pawn

    move_history = [last_move]

    move = board.move_piece((3, 4), (2, 3), move_history=move_history)

    board.undo_move(move)

    assert board.board[3][4] is white_pawn
    assert board.board[3][3] is black_pawn
    assert board.board[2][3] is None
