import pygame

from engine.rules import Rules


class InputHandler:
    def __init__(self, game, board_rect):
        self.game = game
        self.board_rect = board_rect
        self.square_size = board_rect.width // 8

        self.selected_position = None
        self.legal_moves = []

    def screen_to_board(self, position):
        x, y = position

        if not self.board_rect.collidepoint(x, y):
            return None

        col = (x - self.board_rect.x) // self.square_size
        row = (y - self.board_rect.y) // self.square_size

        return row, col

    def handle_click(self, position):
        board_position = self.screen_to_board(position)

        if board_position is None:
            return

        row, col = board_position
        piece = self.game.board.board[row][col]

        # No piece selected yet
        if self.selected_position is None:
            if piece is None:
                return

            if piece.color != self.game.current_turn:
                return

            self.selected_position = board_position

            self.legal_moves = Rules.get_legal_moves(
                self.game.board,
                board_position,
                self.game.current_turn,
            )

            return

        # Clicking the selected piece again → deselect
        if board_position == self.selected_position:
            self.clear_selection()
            return

        # Try to make the move
        if board_position in self.legal_moves:
            success = self.game.make_move(
                self.selected_position,
                board_position,
            )

            if success:
                self.clear_selection()
                return

        # Clicking another friendly piece → select it instead
        if piece is not None and piece.color == self.game.current_turn:
            self.selected_position = board_position

            self.legal_moves = Rules.get_legal_moves(
                self.game.board,
                board_position,
                self.game.current_turn,
            )

            return

        self.clear_selection()

    def clear_selection(self):
        self.selected_position = None
        self.legal_moves = []
