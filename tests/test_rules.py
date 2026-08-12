from board import Board
from piece import Bishop, King, Knight, Pawn, Rook, Queen
from rules import Rules


def clear_board(board):
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None


def test_find_king():
    board = Board()

    assert Rules.find_king(board, "white") == (7, 4)
    assert Rules.find_king(board, "black") == (0, 4)


def test_no_check():
    board = Board()

    assert Rules.is_in_check(board, "white") is False
    assert Rules.is_in_check(board, "black") is False


def test_rook_check():
    board = Board()
    clear_board(board)

    board.board[4][4] = King("white")
    board.board[4][0] = Rook("black")

    assert Rules.is_in_check(board, "white") is True


def test_blocked_rook():
    board = Board()
    clear_board(board)

    board.board[4][4] = King("white")
    board.board[4][0] = Rook("black")
    board.board[4][2] = Rook("white")

    assert Rules.is_in_check(board, "white") is False


def test_knight_check():
    board = Board()
    clear_board(board)

    board.board[4][4] = King("white")
    board.board[2][3] = Knight("black")

    assert Rules.is_in_check(board, "white") is True


def test_illegal_move_exposing_king():
    board = Board()
    clear_board(board)

    board.board[4][4] = King("white")
    board.board[4][3] = Bishop("white")
    board.board[4][0] = Rook("black")

    assert Rules.is_legal_move(board, (4, 3), (3, 2), "white") is False


def test_not_checkmate_at_start():
    board = Board()

    assert Rules.is_checkmate(board, "white") is False
    assert Rules.is_checkmate(board, "black") is False


def test_checkmate():
    board = Board()
    clear_board(board)

    board.board[0][0] = King("black")
    board.board[1][1] = Queen("white")
    board.board[2][2] = King("white")

    assert Rules.is_checkmate(board, "black") is True


def test_check_not_checkmate():
    board = Board()
    clear_board(board)

    board.board[0][0] = King("black")
    board.board[0][7] = Rook("white")
    board.board[7][7] = King("white")

    assert Rules.is_in_check(board, "black") is True
    assert Rules.is_checkmate(board, "black") is False


def test_not_stalemate_at_start():
    board = Board()

    assert Rules.is_stalemate(board, "white") is False
    assert Rules.is_stalemate(board, "black") is False


def test_stalemate():
    board = Board()
    clear_board(board)

    board.board[0][0] = King("black")
    board.board[1][2] = Queen("white")
    board.board[2][2] = King("white")

    assert Rules.is_in_check(board, "black") is False
    assert Rules.is_stalemate(board, "black") is True


def test_checkmate_not_stalemate():
    board = Board()
    clear_board(board)

    board.board[0][0] = King("black")
    board.board[1][1] = Queen("white")
    board.board[2][2] = King("white")

    assert Rules.is_checkmate(board, "black") is True
    assert Rules.is_stalemate(board, "black") is False


def setup_castling_board():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][7] = Rook("white")

    return board


def test_kingside_castling_available():
    board = setup_castling_board()

    moves = Rules.get_castling_moves(board, (7, 4), "white")
    assert (7, 6) in moves


def test_queenside_castling_available():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][0] = Rook("white")

    moves = Rules.get_castling_moves(board, (7, 4), "white")
    assert (7, 2) in moves


def test_castling_not_allowed_if_king_has_moved():
    board = setup_castling_board()

    board.board[7][4].has_moved = True
    moves = Rules.get_castling_moves(board, (7, 4), "white")

    assert (7, 6) not in moves


def test_castling_not_allowed_if_rook_has_moved():
    board = setup_castling_board()

    board.board[7][7].has_moved = True
    moves = Rules.get_castling_moves(board, (7, 4), "white")

    assert (7, 6) not in moves


def test_castling_blocked():
    board = setup_castling_board()

    board.board[7][5] = Knight("white")
    moves = Rules.get_castling_moves(board, (7, 4), "white")

    assert (7, 6) not in moves


def test_cannot_castle_if_in_check():
    board = setup_castling_board()

    board.board[0][4] = Rook("black")
    moves = Rules.get_castling_moves(board, (7, 4), "white")

    assert (7, 6) not in moves


def test_cannot_castle_through_check():
    board = setup_castling_board()

    board.board[0][5] = Rook("black")
    moves = Rules.get_castling_moves(board, (7, 6), "white")

    assert (7, 6) not in moves


def test_kingside_castling_move():
    board = Board()

    board.board[7][5] = None
    board.board[7][6] = None

    king = board.board[7][4]
    rook = board.board[7][7]

    king.has_moved = False
    rook.has_moved = False

    move = board.move_piece((7, 4), (7, 6))
    assert move is not None

    assert board.board[7][6] is king
    assert board.board[7][4] is None

    assert board.board[7][5] is rook
    assert board.board[7][7] is None

    assert king.has_moved is True
    assert rook.has_moved is True


def test_undo_kingside_castle():
    board = Board()

    board.board[7][5] = None
    board.board[7][6] = None

    king = board.board[7][4]
    rook = board.board[7][7]

    move = board.move_piece((7, 4), (7, 6))

    board.undo_move(move)

    assert board.board[7][4] is king
    assert board.board[7][7] is rook

    assert board.board[7][5] is None
    assert board.board[7][6] is None

    assert king.has_moved is False
    assert rook.has_moved is False


def test_promotion_requires_choice_in_rules():
    board = Board()
    clear_board(board)

    board.board[1][4] = Pawn("white")

    assert Rules.is_legal_move(board, (1, 4), (0, 4), "white") is False


def test_promotion_queen_is_legal():
    board = Board()
    clear_board(board)

    board.board[1][4] = Pawn("white")

    assert Rules.is_legal_move(board, (1, 4), (0, 4), "white", "queen") is True


def test_all_promotion_choice_is_legal():
    for promotion in ("queen", "rook", "bishop", "knight"):
        board = Board()
        clear_board(board)

        board.board[1][4] = Pawn("white")

        assert Rules.is_legal_move(board, (1, 4), (0, 4), "white", promotion) is True
