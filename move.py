class Move:
    def __init__(self, start, end, captured_piece=None):
        self.start = start
        self.end = end
        self.captured_piece = captured_piece
