class Piece:
    def __init__(self, color):
        self.color = color

    def get_sliding_moves(self, board, position, directions):
        pass


class Pawn(Piece):
    pass


class Rook(Piece):
    def get_moves(self, position):
        row, col = position

        return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class King(Piece):
    pass
