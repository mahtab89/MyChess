from .piece import Piece


class Move:
    def __init__(self, start, end, captured_piece=None, piece_has_moved=False):
        self.start = start
        self.end = end
        self.piece: Piece | None = None
        self.captured_piece = captured_piece
        self.piece_has_moved = piece_has_moved

        self.castling_rook = None
        self.castling_rook_start: tuple[int, int] | None = None
        self.castling_rook_end: tuple[int, int] | None = None
        self.castling_rook_has_moved = None

        self.promotion: str | None = None
        self.promoted_piece: Piece | None = None
        self.promotion_original_piece: Piece | None = None

        self.en_passant = False
        self.en_passant_captured_piece: Piece | None = None
        self.en_passant_captured_position: tuple[int, int] | None = None
