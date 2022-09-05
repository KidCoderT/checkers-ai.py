# pylint: disable=no-member

import sys
import pygame
import kct_pygame_tools as kpt
from src.board import Board

pygame.init()

BOARD_OFFSET = 30
BOARD_SIZE = 640
CELL_SIZE = BOARD_SIZE // 8
BOARD_BORDER_THICKNESS = 20

width, height = 1200, BOARD_SIZE + BOARD_OFFSET * 2
pygame.display.set_caption("Checker AI")
screen = pygame.display.set_mode((width, height))

background = pygame.Surface((width, height))
background.fill(pygame.Color("#F4E7C6"))

pygame.draw.rect(
    background,
    pygame.Color("#DCCFAE"),
    (
        BOARD_OFFSET - BOARD_BORDER_THICKNESS,
        BOARD_OFFSET - BOARD_BORDER_THICKNESS,
        BOARD_SIZE + BOARD_BORDER_THICKNESS * 2,
        BOARD_SIZE + BOARD_BORDER_THICKNESS * 2,
    ),
    border_radius=10,
)

for file in range(8):
    for rank in range(8):
        is_light = (file + rank) % 2 == 0
        color = pygame.Color("#FFFFFF") if is_light else pygame.Color("#183037")
        pygame.draw.rect(
            background,
            color,
            (
                file * CELL_SIZE + BOARD_OFFSET,
                rank * CELL_SIZE + BOARD_OFFSET,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

info_box_rect = pygame.Rect(
    BOARD_OFFSET + BOARD_BORDER_THICKNESS + BOARD_SIZE + 10,
    10,
    490,
    BOARD_SIZE + BOARD_BORDER_THICKNESS * 2,
)

pygame.draw.rect(
    background,
    pygame.Color("#FEF1D0"),
    info_box_rect,
    border_radius=10,
)

info_box = pygame.image.load("./assets/images/info_section.png")
background.blit(info_box, info_box_rect.topleft)

PIECES_SCALE_FACTOR = 0.4
RED_PIECE = kpt.load_and_scale("./assets/images/red.png", PIECES_SCALE_FACTOR)
BLUE_PIECE = kpt.load_and_scale("./assets/images/blue.png", PIECES_SCALE_FACTOR)
PIECE_HALF_WIDTH = RED_PIECE.get_width() / 2
PIECE_HALF_HEIGHT = RED_PIECE.get_height() / 2

clock = pygame.time.Clock()
board = Board()

while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    red_indices, blue_indices = board.all_pieces

    for index in red_indices:
        i = (index % 8) + 0.5
        j = (index // 8) + 0.5

        x = BOARD_OFFSET + i * CELL_SIZE - PIECE_HALF_WIDTH
        y = BOARD_OFFSET + j * CELL_SIZE - PIECE_HALF_HEIGHT

        screen.blit(RED_PIECE, (x, y))

    for index in blue_indices:
        i = (index % 8) + 0.5
        j = (index // 8) + 0.5

        x = BOARD_OFFSET + i * CELL_SIZE - PIECE_HALF_WIDTH
        y = BOARD_OFFSET + j * CELL_SIZE - PIECE_HALF_HEIGHT

        screen.blit(BLUE_PIECE, (x, y))

    pygame.display.update()
    clock.tick(60)
