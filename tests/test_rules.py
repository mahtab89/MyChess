from board import Board
from piece import Bishop, King, Knight, Rook
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
