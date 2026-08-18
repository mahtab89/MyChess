from engine.board import Board
from engine.piece import Bishop, King, Knight, Pawn, Queen, Rook


def test_pawn():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    pawn = Pawn("white")
    moves = pawn.get_moves(board, (6, 4))

    assert (5, 4) in moves
    assert (4, 4) in moves


def test_rook():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    rook = Rook("white")
    moves = rook.get_moves(board, (4, 4))
    assert len(moves) == 14


def test_knight():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    knight = Knight("white")
    moves = knight.get_moves(board, (4, 4))
    assert len(moves) == 8


def test_bishop():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    bishop = Bishop("white")
    moves = bishop.get_moves(board, (4, 4))
    assert len(moves) == 13


def test_queen():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    queen = Queen("white")
    moves = queen.get_moves(board, (4, 4))
    assert len(moves) == 27


def test_king():
    board = Board()
    for row in range(8):
        for col in range(8):
            board.board[row][col] = None

    king = King("white")
    moves = king.get_moves(board, (4, 4))
    assert len(moves) == 8
