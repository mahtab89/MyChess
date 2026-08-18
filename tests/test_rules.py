from engine.board import Board
from engine.move import Move
from engine.piece import Bishop, King, Knight, Pawn, Rook, Queen
from engine.rules import Rules


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
    moves = Rules.get_castling_moves(board, (7, 4), "white")

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


def test_en_passant_available():
    board = Board()
    clear_board(board)

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[3][4] = white_pawn
    board.board[3][3] = black_pawn

    move = Move((1, 3), (3, 3), None, False)
    move.piece = black_pawn

    move_history = [move]
    moves = Rules.get_en_passant_moves(board, (3, 4), "white", move_history)

    assert (2, 3) in moves


def test_black_en_passant_available():
    board = Board()
    clear_board(board)

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[4][3] = black_pawn
    board.board[4][4] = white_pawn

    move = Move((6, 4), (4, 4), None, False)
    move.piece = white_pawn

    move_history = [move]
    moves = Rules.get_en_passant_moves(board, (4, 3), "black", move_history)

    assert (5, 4) in moves


def test_en_passant_not_available_after_other_move():
    board = Board()
    clear_board(board)

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[3][4] = white_pawn
    board.board[3][3] = black_pawn

    move = Move((2, 3), (3, 3), None, False)

    move.piece = black_pawn

    moves = Rules.get_en_passant_moves(board, (3, 4), "white", [move])

    assert (2, 3) not in moves


def test_king_vs_king_is_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[0][4] = King("black")

    assert Rules.is_insufficient_material(board) is True


def test_king_and_bishop_vs_king_is_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][2] = Bishop("white")
    board.board[0][4] = King("black")

    assert Rules.is_insufficient_material(board) is True


def test_king_and_knight_vs_king_is_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][2] = Knight("white")
    board.board[0][4] = King("black")

    assert Rules.is_insufficient_material(board) is True


def test_king_and_rook_vs_king_is_not_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][2] = Rook("white")
    board.board[0][4] = King("black")

    assert Rules.is_insufficient_material(board) is False


def test_same_color_bishops_are_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][2] = King("white")
    board.board[6][3] = Bishop("white")

    board.board[0][5] = King("black")
    board.board[1][2] = Bishop("black")

    assert Rules.is_insufficient_material(board) is True


def test_opposite_color_bishops_are_not_insufficient_material():
    board = Board()
    clear_board(board)

    board.board[7][2] = King("white")
    board.board[6][3] = Bishop("white")

    board.board[0][5] = King("black")
    board.board[1][3] = Bishop("black")

    assert Rules.is_insufficient_material(board) is False


def test_fifty_move_rule_not_reached():
    assert Rules.is_fifty_move_draw(99) is False


def test_fifty_move_rule_reached():
    assert Rules.is_fifty_move_draw(100) is True


def test_fifty_move_rule_above_limit():
    assert Rules.is_fifty_move_draw(120) is True


def test_threefold_repetition_not_reached():
    position = ("position", "white")

    history = [
        position,
        ("other", "black"),
        position,
    ]

    assert Rules.is_threefold_repetition(history) is False


def test_threefold_repetition_reached():
    position = ("position", "white")

    history = [
        position,
        ("other", "black"),
        position,
        ("another", "white"),
        position,
    ]

    assert Rules.is_threefold_repetition(history) is True


def test_threefold_repetition_uses_current_position():
    position = ("position", "white")

    history = [
        ("other", "black"),
        position,
        ("different", "white"),
    ]

    assert Rules.is_threefold_repetition(history) is False


def test_get_legal_moves_includes_promotion():
    board = Board()
    clear_board(board)

    board.board[1][4] = Pawn("white")

    moves = Rules.get_legal_moves(board, (1, 4), "white")

    assert (0, 4) in moves


def test_get_legal_moves_includes_en_passant():
    board = Board()
    clear_board(board)

    white_pawn = Pawn("white")
    black_pawn = Pawn("black")

    board.board[3][4] = white_pawn
    board.board[3][3] = black_pawn

    move = Move((1, 3), (3, 3), None, False)
    move.piece = black_pawn

    move_history = [move]

    moves = Rules.get_legal_moves(board, (3, 4), "white", move_history)

    assert (2, 3) in moves


def test_cannot_castle_with_opponent_rook():
    board = Board()
    clear_board(board)

    board.board[7][4] = King("white")
    board.board[7][7] = Rook("black")

    moves = Rules.get_castling_moves(board, (7, 4), "white")

    assert (7, 6) not in moves


def test_en_passant_not_available_with_same_color_pawn():
    board = Board()
    clear_board(board)

    white_pawn = Pawn("white")
    another_white_pawn = Pawn("white")

    board.board[3][4] = white_pawn
    board.board[3][3] = another_white_pawn

    last_move = Move((1, 3), (3, 3), None, False)
    last_move.piece = another_white_pawn

    moves = Rules.get_en_passant_moves(board, (3, 4), "white", [last_move])

    assert (2, 3) not in moves
