import pygame
from ui.move_history import MoveHistory


class Sidebar:
    def __init__(self, screen, rect, theme):
        self.screen = screen
        self.rect = rect
        self.theme = theme

        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 28)

        self.padding = 15
        self.gap = 10

        self.controls_height = 190
        self.status_height = 100

        self.controls_rect = pygame.Rect(
            rect.x,
            rect.y,
            rect.width,
            self.controls_height,
        )

        self.status_rect = pygame.Rect(
            rect.x,
            rect.bottom - self.status_height,
            rect.width,
            self.status_height,
        )

        self.history_rect = pygame.Rect(
            rect.x,
            self.controls_rect.bottom + self.gap,
            rect.width,
            self.status_rect.top
            - self.controls_rect.bottom
            - (self.gap * 2),
        )

        self.move_history = MoveHistory(
            screen,
            self.history_rect,
            theme,
        )

    def draw_panel(self, rect):
        pygame.draw.rect(
            self.screen,
            self.theme["panel"],
            rect,
            border_radius=10,
        )

    def draw_title(self, text, rect):
        surface = self.title_font.render(
            text,
            True,
            self.theme["text"],
        )

        self.screen.blit(
            surface,
            (
                rect.x + self.padding,
                rect.y + self.padding,
            ),
        )

    def draw(self, current_turn="white", move_history=None):

        if move_history is None:
            move_history = []
        
        self.move_history.draw(move_history)
        
        self.draw_panel(self.controls_rect)
        self.draw_panel(self.history_rect)
        self.draw_panel(self.status_rect)

        # Controls
        self.draw_title("Controls", self.controls_rect)

        buttons = [
            "Restart",
            "Settings",
            "Exit",
        ]

        button_y = self.controls_rect.y + 50

        for text in buttons:
            button_rect = pygame.Rect(
                self.controls_rect.x + self.padding,
                button_y,
                self.controls_rect.width - self.padding * 2,
                35,
            )

            pygame.draw.rect(
                self.screen,
                self.theme["button"],
                button_rect,
                border_radius=6,
            )

            surface = self.small_font.render(
                text,
                True,
                self.theme["text"],
            )

            text_rect = surface.get_rect(
                center=button_rect.center
            )

            self.screen.blit(surface, text_rect)

            button_y += 42

        # Move history
        self.draw_title("Move History", self.history_rect)

        self.move_history.draw(move_history)

        # Status
        self.draw_title("Status", self.status_rect)

        status_text = (
            "White to move"
            if current_turn == "white"
            else "Black to move"
        )

        status_surface = self.small_font.render(
            status_text,
            True,
            self.theme["text_secondary"],
        )

        self.screen.blit(
            status_surface,
            (
                self.status_rect.x + self.padding,
                self.status_rect.y + 55,
            ),
        )
