from board import Board

board = Board()

for row in board.board:
    for piece in row:
        if piece is None:
            print(".", end=" ")
        else:
            print(type(piece).__name__[0], end=" ")

    print()

from piece import Rook

rook = Rook("black")
moves = rook.get_moves((4, 4))
print(moves)
