from .board import Board
from .rules import Rules


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []
        self.halfmove_clock = 0
        self.position_history = []
        self.position_history.append(self.get_position_key())

    def make_move(self, start, end, promotion=None):
        piece = self.board.board[start[0]][start[1]]

        if piece is None:
            return False

        if piece.color != self.current_turn:
            return False

        if not Rules.is_legal_move(
            self.board, start, end, self.current_turn, promotion, self.move_history
        ):
            return False

        move = self.board.move_piece(start, end, promotion, self.move_history)

        if move is None:
            return False

        self.move_history.append(move)

        if (
            piece.__class__.__name__ == "Pawn"
            or move.captured_piece is not None
            or move.en_passant
        ):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.current_turn == "white":
            self.current_turn = "black"
        else:
            self.current_turn = "white"

        self.position_history.append(self.get_position_key())

        return True

    def get_position_key(self):
        pieces = []

        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]

                if piece is None:
                    pieces.append(None)
                else:
                    pieces.append(
                        (
                            piece.__class__.__name__,
                            piece.color,
                        )
                    )

        castling_rights = (
            self._can_castle("white", "king"),
            self._can_castle("white", "queen"),
            self._can_castle("black", "king"),
            self._can_castle("black", "queen"),
        )

        en_passant_target = None

        if self.move_history:
            last_move = self.move_history[-1]

            if (
                last_move.piece is not None
                and last_move.piece.__class__.__name__ == "Pawn"
                and abs(last_move.end[0] - last_move.start[0]) == 2
            ):
                en_passant_target = (
                    (last_move.start[0] + last_move.end[0]) // 2,
                    last_move.end[1],
                )

        return (
            tuple(pieces),
            self.current_turn,
            castling_rights,
            en_passant_target,
        )

    def _can_castle(self, color, side):
        row = 7 if color == "white" else 0

        king = self.board.board[row][4]

        if (
            king is None
            or king.__class__.__name__ != "King"
            or king.color != color
            or king.has_moved
        ):
            return False

        if side == "king":
            rook = self.board.board[row][7]
        else:
            rook = self.board.board[row][0]

        return (
            rook is not None
            and rook.__class__.__name__ == "Rook"
            and rook.color == color
            and not rook.has_moved
        )

    def get_game_status(self):
        color = self.current_turn

        if Rules.is_checkmate(self.board, color, self.move_history):
            winner = "black" if color == "white" else "white"
            return f"checkmate_{winner}"

        if Rules.is_stalemate(self.board, color, self.move_history):
            return "stalemate"

        if Rules.is_insufficient_material(self.board):
            return "draw_insufficient_material"

        if Rules.is_fifty_move_draw(self.halfmove_clock):
            return "draw_fifty_move"

        if Rules.is_threefold_repetition(self.position_history):
            return "draw_threefold"

        return "playing"
