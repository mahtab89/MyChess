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

    def move_piece(self, start, end, promotion=None):
        piece = self.board[start[0]][start[1]]

        if piece is None:
            return None

        if (
            piece.__class__.__name__ == "Pawn"
            and end[0] in (0, 7)
            and promotion is None
        ):
            return None

        captured_piece = self.board[end[0]][end[1]]
        piece_has_moved = piece.has_moved

        move = Move(start, end, captured_piece, piece_has_moved)

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        piece.has_moved = True

        # promotion move rules
        if piece.__class__.__name__ == "Pawn" and end[0] in (0, 7):
            promoted_piece = self.create_promoted_piece(piece.color, promotion)

            if promoted_piece is not None:
                move.promotion = promotion
                move.promoted_piece = promoted_piece
                move.promotion_original_piece = piece

                self.board[end[0]][end[1]] = promoted_piece

        # castling move rules
        is_castling = piece.__class__.__name__ == "King" and abs(end[1] - start[1]) == 2

        if is_castling:
            row = start[0]

            if end[1] > start[1]:
                rook_start = (row, 7)
                rook_end = (row, 5)
            else:
                rook_start = (row, 0)
                rook_end = (row, 3)

            rook = self.board[rook_start[0]][rook_start[1]]

            move.castling_rook = rook
            move.castling_rook_start = rook_start
            move.castling_rook_end = rook_end
            move.castling_rook_has_moved = rook.has_moved

            self.board[rook_end[0]][rook_end[1]] = rook
            self.board[rook_start[0]][rook_start[1]] = None

            rook.has_moved = True

        return move

    def undo_move(self, move):
        piece = self.board[move.end[0]][move.end[1]]

        self.board[move.start[0]][move.start[1]] = piece
        self.board[move.end[0]][move.end[1]] = move.captured_piece

        piece.has_moved = move.piece_has_moved

        if move.promotion is not None:
            self.board[move.start[0]][move.start[1]] = move.promotion_original_piece
            move.promotion_original_piece.has_moved = move.piece_has_moved

        if move.castling_rook is not None:
            rook = move.castling_rook

            self.board[move.castling_rook_start[0]][move.castling_rook_start[1]] = rook
            self.board[move.castling_rook_end[0]][move.castling_rook_end[1]] = None

            rook.has_moved = move.castling_rook_has_moved

    def create_promoted_piece(self, color, promotion):
        if promotion == "queen":
            return Queen(color)

        if promotion == "rook":
            return Rook(color)

        if promotion == "bishop":
            return Bishop(color)

        if promotion == "knight":
            return Knight(color)

        return None
