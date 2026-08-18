import pygame


class PlayerPanel:
    def __init__(self, screen, rect, theme, player_name, color):
        self.screen = screen
        self.rect = rect
        self.theme = theme
        self.player_name = player_name
        self.color = color

        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)

    def draw(self, captured_pieces=None, active=False):
        pygame.draw.rect(
            self.screen,
            self.theme["panel"],
            self.rect,
            border_radius=10,
        )

        # Active player indicator
        indicator_color = self.theme["active"] if active else self.theme["inactive"]

        pygame.draw.circle(
            self.screen,
            indicator_color,
            (self.rect.x + 18, self.rect.centery),
            7,
        )

        # Player name
        name_surface = self.font.render(
            self.player_name,
            True,
            self.theme["text"],
        )

        self.screen.blit(
            name_surface,
            (
                self.rect.x + 35,
                self.rect.y + 10,
            ),
        )

        # Captured pieces
        captured_text = "Captured: "

        if captured_pieces:
            captured_text += " ".join(captured_pieces)
        else:
            captured_text += "None"

        captured_surface = self.small_font.render(
            captured_text,
            True,
            self.theme["text_secondary"],
        )

        self.screen.blit(
            captured_surface,
            (
                self.rect.x + 35,
                self.rect.y + 45,
            ),
        )
