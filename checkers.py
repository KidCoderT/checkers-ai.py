# pylint: disable=no-member, not-an-iterable, invalid-name

import sys
import pygame
import kct_pygame_tools as kpt
from src.game import Game

num_pass, num_fail = pygame.init()

if num_fail > 0:
    print("There is some Error with pygame!")
    sys.exit()

BOARD_OFFSET = 30
BOARD_SIZE = 640
CELL_SIZE = BOARD_SIZE // 8
BOARD_BORDER_THICKNESS = 20

width, height = 1200, BOARD_SIZE + BOARD_OFFSET * 2
pygame.display.set_caption("Checker AI")
screen = pygame.display.set_mode((width, height))

BG_COLOR = pygame.Color("#F4E7C6")
background = pygame.Surface((width, height))
background.fill(BG_COLOR)

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

MOVE_SQUARE = pygame.Surface((CELL_SIZE, CELL_SIZE))
MOVE_SQUARE.fill((255, 255, 255))
MOVE_SQUARE.set_alpha(50)


def get_piece_image(piece_value: int):
    """Gets the Image for a piece
    based on the piece value

    Args:
        piece_value (int): the piece value
    Raises:
        ValueError: when the piece_value is 0

    Returns:
        pygame.surface.Surface: the piece image
    """
    image = RED_PIECE if piece_value < 0 else BLUE_PIECE
    if piece_value == 0:
        raise ValueError("piece_value must not be zero!!")
    return image


clock = pygame.time.Clock()
active_index: int | None = None
active_piece: int = 0
game = Game(True)
should_inverse_board = game.blue is None and game.red is not None

last_move_notation = None

while True:
    mx, my = pygame.mouse.get_pos()
    screen.fill(BG_COLOR)
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

            if should_inverse_board:
                index = (7 - (y // CELL_SIZE)) * 8 + (7 - (x // CELL_SIZE))

            if 0 <= index < 64 and is_x_okay and is_y_okay:

                piece = game.board.piece(index)
                if piece != 0:

                    if piece in game.board.current_side.value and (
                        piece < 0
                        and game.red is not None
                        or piece > 0
                        and game.blue is not None
                    ):
                        active_piece = game.board.piece(index)
                        active_index = index
                # else:
                #     screen_shake(500)

        if event.type == pygame.MOUSEBUTTONUP:
            if active_index is not None:
                x = mx - BOARD_OFFSET
                y = my - BOARD_OFFSET

                is_x_okay = 0 <= x <= BOARD_SIZE
                is_y_okay = 0 <= y <= BOARD_SIZE

                index = (y // CELL_SIZE) * 8 + (x // CELL_SIZE)

                if should_inverse_board:
                    index = (7 - (y // CELL_SIZE)) * 8 + (7 - (x // CELL_SIZE))

                if active_index != index:
                    if (
                        0 <= index < 64
                        and is_x_okay
                        and is_y_okay
                        and game.board.get_notation(index) is not None
                        and game.board.piece(index) == 0
                    ):
                        try:
                            move_index = game.find_move_index(active_index, index)
                            game.play_move(move_index)
                            color = "r" if game.board.piece(index) < 1 else "b"
                            last_move_notation = color = str(
                                game.board.get_notation(index)
                            )
                        except ValueError:
                            pass

                active_index = None

    last_move = game.board.last_move
    pieces = game.board.all_pieces

    if last_move is not None:

        for index in last_move:
            i = index % 8
            j = index // 8

            if should_inverse_board:
                i = 7 - i
                j = 7 - j

            x = BOARD_OFFSET + i * CELL_SIZE
            y = BOARD_OFFSET + j * CELL_SIZE

            screen.blit(MOVE_SQUARE, (x, y))

    for (piece, index) in pieces:
        if index == active_index:
            continue

        i = (index % 8) + 0.5
        j = (index // 8) + 0.5

        if should_inverse_board:
            i = 8 - i
            j = 8 - j

        x = BOARD_OFFSET + i * CELL_SIZE
        y = BOARD_OFFSET + j * CELL_SIZE

        piece_image = get_piece_image(piece)
        x -= piece_image.get_width() / 2
        y -= piece_image.get_height() / 2

        if abs(piece) % 2 != 0:
            screen.blit(piece_image, (x, y))
        else:
            screen.blit(piece_image, (x, y + 3))
            screen.blit(piece_image, (x, y - 3))

    if active_index is not None:
        piece_image = get_piece_image(active_piece)
        possible_moves = filter(lambda move: move.start == active_index, game.moves)

        for move in possible_moves:
            i = BOARD_OFFSET + (move.end % 8) * CELL_SIZE
            j = BOARD_OFFSET + (move.end // 8) * CELL_SIZE

            pygame.draw.rect(
                screen,
                (246, 206, 42),
                pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
                6,
            )

        x = mx - piece_image.get_width() / 2
        y = my - piece_image.get_height() / 2

        if abs(active_piece) % 2 != 0:
            screen.blit(piece_image, (x, y))
        else:
            screen.blit(piece_image, (x, y + 3))
            screen.blit(piece_image, (x, y - 3))

    pygame.display.update()
    clock.tick(60)
