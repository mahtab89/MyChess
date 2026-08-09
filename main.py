from board import Board
from piece import King, Knight
from rules import Rules

board = Board()

for row in range(8):
    for col in range(8):
        board.board[row][col] = None

board.board[4][4] = King("white")
board.board[2][3] = Knight("black")

print("White in check:", Rules.is_in_check(board, "white"))
