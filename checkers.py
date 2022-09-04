# pylint: disable=no-member

import sys
import pygame
from utils import FontManager

pygame.init()

BOARD_OFFSET = 30
BOARD_SIZE = 640
width, height = 1200, BOARD_SIZE + BOARD_OFFSET * 2
pygame.display.set_caption("Checker AI")
screen = pygame.display.set_mode((width, height))
CELL_SIZE = BOARD_SIZE // 8

background = pygame.Surface((BOARD_SIZE, BOARD_SIZE))

for file in range(8):
    for rank in range(8):
        is_light = (file + rank) % 2 == 0
        color = pygame.Color("#FFFFFF") if is_light else pygame.Color("#183037")
        pygame.draw.rect(
            background,
            color,
            (file * CELL_SIZE, rank * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

BACKGROUND_BORDER_WIDTH = 20
background_rect = background.get_rect(
    topleft=(
        BOARD_OFFSET - BACKGROUND_BORDER_WIDTH,
        BOARD_OFFSET - BACKGROUND_BORDER_WIDTH,
    )
)
background_rect.width += BACKGROUND_BORDER_WIDTH * 2
background_rect.height += BACKGROUND_BORDER_WIDTH * 2

font_manager = FontManager()
font_manager.create_font("./assets/fonts/FiraCode-Bold.ttf", 40)
font_manager.get_font(("./assets/fonts/FiraCode-Bold.ttf", 40)).set_underline(True)

title_text = font_manager.create_text(
    ("./assets/fonts/FiraCode-Bold.ttf", 40), "Checker AI", (24, 48, 55)
)
title_text_rect = title_text.get_rect(
    center=(background_rect.right + ((width - background_rect.right) / 2), 40)
)

clock = pygame.time.Clock()

while True:
    screen.fill(pygame.Color("#F4E7C6"))
    pygame.draw.rect(screen, pygame.Color("#DCCFAE"), background_rect, border_radius=10)
    screen.blit(background, (BOARD_OFFSET, BOARD_OFFSET))
    screen.blit(title_text, title_text_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
