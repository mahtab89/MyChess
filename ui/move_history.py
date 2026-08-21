import pygame


class MoveHistory:
    def __init__(self, screen, rect, theme):
        self.screen = screen
        self.rect = rect
        self.theme = theme

        self.font = pygame.font.Font(None, 23)
        self.padding = 15
        self.line_height = 28

    @staticmethod
    def square_to_notation(position):
        row, col = position

        files = "abcdefgh"
        file = files[col]
        rank = 8 - row

        return f"{file}{rank}"

    def format_move(self, move):
        start = self.square_to_notation(move.start)
        end = self.square_to_notation(move.end)

        return f"{start} → {end}"

    def draw(self, move_history):
        if not move_history:
            surface = self.font.render(
                "No moves yet",
                True,
                self.theme["text_secondary"],
            )

            self.screen.blit(
                surface,
                (
                    self.rect.x + self.padding,
                    self.rect.y + 55,
                ),
            )

            return

        visible_height = self.rect.height - 70
        max_moves = visible_height // self.line_height

        # Show the most recent moves if the history becomes long.
        visible_moves = move_history[-max_moves:]

        start_y = self.rect.y + 55

        for index, move in enumerate(visible_moves):
            actual_index = (
                len(move_history)
                - len(visible_moves)
                + index
            )

            move_number = actual_index // 2 + 1
            notation = self.format_move(move)

            if actual_index % 2 == 0:
                text = f"{move_number}. {notation}"
            else:
                text = f"    {notation}"

            surface = self.font.render(
                text,
                True,
                self.theme["text_secondary"],
            )

            self.screen.blit(
                surface,
                (
                    self.rect.x + self.padding,
                    start_y + index * self.line_height,
                ),
            )
