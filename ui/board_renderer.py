import pygame


class BoardRenderer:
    def __init__(self, screen, theme, board_rect):
        self.screen = screen
        self.board_rect = board_rect

        self.square_size = board_rect.width // 8

        self.light_square = theme["light_square"]
        self.dark_square = theme["dark_square"]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square

                x = self.board_rect.x + col * self.square_size
                y = self.board_rect.y + row * self.square_size

                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        x,
                        y,
                        self.square_size,
                        self.square_size,
                    ),
                )
