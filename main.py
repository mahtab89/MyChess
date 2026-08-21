import pygame
from engine.game import Game
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
from ui.player_panel import PlayerPanel
from ui.piece_renderer import PieceRenderer
from ui.sidebar import Sidebar

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("MyChess")

game = Game()
theme = THEMES["catppuccin"]

board_renderer = BoardRenderer(
    screen,
    theme,
    BOARD_RECT,
)
black_panel = PlayerPanel(
    screen,
    PLAYER_TOP_RECT,
    theme,
    "Black Player",
    "black",
)

white_panel = PlayerPanel(
    screen,
    PLAYER_BOTTOM_RECT,
    theme,
    "White Player",
    "white",
)

piece_renderer = PieceRenderer(
    screen,
    BOARD_RECT,
)

sidebar = Sidebar(
    screen,
    SIDEBAR_RECT,
    theme,
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
    black_panel.draw(
        captured_pieces=[],
        active=game.current_turn == "black",
    )

    white_panel.draw(
        captured_pieces=[],
        active=game.current_turn == "white",
    )

    board_renderer.draw_board()
    
    piece_renderer.draw(game.board)

    sidebar.draw(game.current_turn)

    pygame.display.flip()

pygame.quit()
