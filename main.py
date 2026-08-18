import pygame

from ui.board_renderer import BoardRenderer
from ui.themes import THEMES
from ui.layout import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_TOP_RECT,
    BOARD_RECT,
    PLAYER_BOTTOM_RECT,
    SIDEBAR_RECT,
)


pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("MyChess")

theme = THEMES["catppuccin"]

board_renderer = BoardRenderer(
    screen,
    theme,
    BOARD_RECT,
)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(theme["background"])

    # Temporary UI areas
    pygame.draw.rect(
        screen,
        theme["background"],
        PLAYER_TOP_RECT,
    )

    pygame.draw.rect(
        screen,
        theme["background"],
        PLAYER_BOTTOM_RECT,
    )

    pygame.draw.rect(
        screen,
        theme["background"],
        SIDEBAR_RECT,
    )

    board_renderer.draw_board()

    pygame.display.flip()

pygame.quit()
