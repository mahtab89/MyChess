from move import Move
from piece import Bishop, King, Knight, Pawn, Queen, Rook


class Board:
    def __init__(self):
        self.board = []

        for row in range(8):
            self.board.append([None] * 8)

        self.initialize()

    def initialize(self):
        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        front_row = [Pawn] * 8

        for col in range(8):
            self.board[0][col] = back_row[col]("black")
            self.board[1][col] = front_row[col]("black")

        for col in range(8):
            self.board[6][col] = front_row[col]("white")
            self.board[7][col] = back_row[col]("white")

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]

        if piece is None:
            return None

        possible_moves = piece.get_moves(self, start)

        if end not in possible_moves:
            return None

        captured_piece = self.board[end[0]][end[1]]

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        return Move(start, end, captured_piece)
