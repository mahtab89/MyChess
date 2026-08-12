from board import Board
from rules import Rules


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []

    def make_move(self, start, end, promotion=None):
        piece = self.board.board[start[0]][start[1]]

        if piece is None:
            return False

        if piece.color != self.current_turn:
            return False

        if not Rules.is_legal_move(
            self.board, start, end, self.current_turn, promotion
        ):
            return False

        move = self.board.move_piece(start, end, promotion)

        if move is None:
            return False

        self.move_history.append(move)

        if self.current_turn == "white":
            self.current_turn = "black"
        else:
            self.current_turn = "white"

        return True
