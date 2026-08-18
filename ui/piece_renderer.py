import os

import pygame


class PieceRenderer:
    def __init__(self, screen, board_rect):
        self.screen = screen
        self.board_rect = board_rect
        self.square_size = board_rect.width // 8

        self.pieces = {}

        self.load_pieces()

    def load_pieces(self):
        pieces_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "pieces",
        )

        piece_names = [
            "bb",
            "bk",
            "bn",
            "bp",
            "bq",
            "br",
            "wb",
            "wk",
            "wn",
            "wp",
            "wq",
            "wr",
        ]

        for name in piece_names:
            path = os.path.join(
                pieces_path,
                f"{name}.png",
            )

            image = pygame.image.load(path).convert_alpha()

            image = pygame.transform.smoothscale(
                image,
                (
                    self.square_size,
                    self.square_size,
                ),
            )

            self.pieces[name] = image

    def draw_piece(self, piece, row, col):
        color_prefix = "w" if piece.color == "white" else "b"

        piece_map = {
            "Pawn": "p",
            "Knight": "n",
            "Bishop": "b",
            "Rook": "r",
            "Queen": "q",
            "King": "k",
        }

        piece_type = piece.__class__.__name__
        piece_name = color_prefix + piece_map[piece_type]

        image = self.pieces[piece_name]

        x = self.board_rect.x + col * self.square_size
        y = self.board_rect.y + row * self.square_size

        self.screen.blit(image, (x, y))

    def draw(self, board):
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None:
                    self.draw_piece(piece, row, col)
