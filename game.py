from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"

    def make_move(self, start, end):
        piece = self.board.board[start[0]][start[1]]

        if piece is None:
            return False

        if piece.color != self.current_turn:
            return False

        success = self.board.move_piece(start, end)

        if not success:
            return False

        if self.current_turn == "white":
            self.current_turn = "black"
        else:
            self.current_turn = "white"

        return True
