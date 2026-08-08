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
