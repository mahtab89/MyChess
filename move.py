class Move:
    def __init__(self, start, end, captured_piece=None, piece_has_moved=False):
        self.start = start
        self.end = end
        self.captured_piece = captured_piece
        self.piece_has_moved = piece_has_moved

        self.castling_rook = None
        self.castling_rook_start: tuple[int, int] | None = None
        self.castling_rook_end: tuple[int, int] | None = None
        self.castling_rook_has_moved = None
