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


def piece_img(number: int):
    """Gets the Image for a piece
    based on the piece value

    Args:
        number (int): the piece value
    Raises:
        ValueError: when the number is 0

    Returns:
        pygame.surface.Surface: the piece image
    """
    img = RED_PIECE if number > 0 else BLUE_PIECE
    if number == 0:
        raise ValueError("Number must not be zero!!")
    return img


clock = pygame.time.Clock()
active_index: int | None = None
active_piece: int = 0
board = Board()

while True:
    mx, my = pygame.mouse.get_pos()
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = mx - BOARD_OFFSET
            y = my - BOARD_OFFSET

            is_x_okay = 0 <= x <= BOARD_SIZE
            is_y_okay = 0 <= y <= BOARD_SIZE

            index = (y // CELL_SIZE) * 8 + (x // CELL_SIZE)

            if 0 <= index < 64 and is_x_okay and is_y_okay:
                active_piece = board.piece(index)
                active_index = index

        if event.type == pygame.MOUSEBUTTONUP:
            if active_index is not None:
                x = mx - BOARD_OFFSET
                y = my - BOARD_OFFSET

                is_x_okay = 0 <= x <= BOARD_SIZE
                is_y_okay = 0 <= y <= BOARD_SIZE

                index = (y // CELL_SIZE) * 8 + (x // CELL_SIZE)

                if (
                    0 <= index < 64
                    and is_x_okay
                    and is_y_okay
                    and board.piece(index) == 0
                ):
                    board.move(active_index, index)

                active_index = None

    pieces = board.all_pieces

    for (piece, index) in pieces:
        if index == active_index:
            continue

        i = (index % 8) + 0.5
        j = (index // 8) + 0.5

        x = BOARD_OFFSET + i * CELL_SIZE
        y = BOARD_OFFSET + j * CELL_SIZE

        img = piece_img(piece)
        x -= img.get_width() / 2
        y -= img.get_height() / 2

        screen.blit(img, (x, y))

    if active_index is not None:
        img = piece_img(active_piece)
        x = mx - img.get_width() / 2
        y = my - img.get_height() / 2
        screen.blit(img, (x, y))

    pygame.display.update()
    clock.tick(60)
