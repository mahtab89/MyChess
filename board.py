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

    def move_piece(self, start, end, promotion=None, move_history=None):
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

        # en passant rules
        is_en_passant = False
        en_passant_captured_piece = None
        en_passant_captured_position = None

        if (
            piece.__class__.__name__ == "Pawn"
            and move_history
            and captured_piece is None
            and abs(end[1] - start[1]) == 1
            and end[0] != start[0]
        ):
            last_move = move_history[-1]

            if (
                last_move.piece is not None
                and last_move.piece.__class__.__name__ == "Pawn"
                and last_move.piece.color != piece.color
                and abs(last_move.end[0] - last_move.start[0]) == 2
                and last_move.end == (start[0], end[1])
            ):
                is_en_passant = True
                en_passant_captured_position = last_move.end
                en_passant_captured_piece = self.board[last_move.end[0]][
                    last_move.end[1]
                ]

        move = Move(start, end, captured_piece, piece_has_moved)
        move.piece = piece

        move.en_passant = is_en_passant
        move.en_passant_captured_piece = en_passant_captured_piece
        move.en_passant_captured_position = en_passant_captured_position

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        piece.has_moved = True

        if is_en_passant and en_passant_captured_position is not None:
            captured_row, captured_col = en_passant_captured_position

            self.board[captured_row][captured_col] = None

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

        if move.en_passant and move.en_passant_captured_position is not None:
            row, col = move.en_passant_captured_position
            self.board[row][col] = move.en_passant_captured_piece

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
