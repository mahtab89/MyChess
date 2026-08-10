from board import Board
from piece import King, Rook, Bishop
from rules import Rules


board = Board()

for row in range(8):
    for col in range(8):
        board.board[row][col] = None

board.board[4][4] = King("white")
board.board[4][3] = Bishop("white")
board.board[4][0] = Rook("black")


moves = Rules.get_legal_moves(board, (4, 3), "white")

print(moves)
