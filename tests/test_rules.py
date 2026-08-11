from board import Board
from piece import Bishop, King, Knight, Rook, Queen
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
