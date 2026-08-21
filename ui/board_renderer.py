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

    def draw_highlights(self, selected_position, legal_moves):
        if selected_position is not None:
            row, col = selected_position

            x = self.board_rect.x + col * self.square_size
            y = self.board_rect.y + row * self.square_size

            pygame.draw.rect(
                self.screen,
                (120, 180, 120),
                (
                    x,
                    y,
                    self.square_size,
                    self.square_size,
                ),
                width=5,
            )

        for row, col in legal_moves:
            center_x = (
                self.board_rect.x
                + col * self.square_size
                + self.square_size // 2
            )

            center_y = (
                self.board_rect.y
                + row * self.square_size
                + self.square_size // 2
            )

            pygame.draw.circle(
                self.screen,
                (120, 180, 120),
                (center_x, center_y),
                10,
            )
