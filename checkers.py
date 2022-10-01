# pylint: disable=no-member, not-an-iterable, invalid-name, unsubscriptable-object, redefined-outer-name, global-variable-not-assigned

import sys
import random
import pygame
import kct_pygame_tools as kpt
from src.game import Game, PieceTypes

from settings import BOARD_SIZE, BOARD_OFFSET, BOARD_BORDER_THICKNESS, CELL_SIZE
from particles import SparksContainer
from button import Button

# TODO: MAKE CLICK AND SHOW MOVES
#   -- REMOVE DRAG & DROP

num_pass, num_fail = pygame.init()

if num_fail > 0:
    print("There is some Error with pygame!")
    sys.exit()

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

RED_INFO_PIECE = kpt.load_and_scale("./assets/images/red.png", 0.76)
BLUE_INFO_PIECE = kpt.load_and_scale("./assets/images/blue.png", 0.76)
DRAW_INFO_PIECE = kpt.load_and_scale("./assets/images/grey.png", 0.76)

RED_WIN_BANNER = kpt.load_and_scale("./assets/images/Red Banner.png", 1)
BLUE_WIN_BANNER = kpt.load_and_scale("./assets/images/Blue Banner.png", 1)
DRAW_BANNER = kpt.load_and_scale("./assets/images/Draw Banner.png", 1)

MOVE_SQUARE = pygame.Surface((CELL_SIZE, CELL_SIZE))
MOVE_SQUARE.fill((255, 255, 255))
MOVE_SQUARE.set_alpha(50)

BLACK_OVERLAY = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
BLACK_OVERLAY.set_alpha(100)

MAX_NUMBER_OF_FIREWORKS = 65

BTN_FONT = pygame.font.Font("./assets/fonts/FiraCode-Medium.ttf", 24)
TEXT_FONT = pygame.font.Font("./assets/fonts/FiraCode-Medium.ttf", 24)


def get_piece_image(piece_value: int | None, is_info: bool = False):
    """Gets the Image for a piece
    based on the piece value

    Args:
        piece_value (int): the piece value
    Raises:
        ValueError: when the piece_value is 0

    Returns:
        pygame.surface.Surface: the piece image
    """
    if is_info:
        if piece_value is None or piece_value == 0:
            return DRAW_INFO_PIECE
        image = RED_INFO_PIECE if piece_value < 0 else BLUE_INFO_PIECE
        return image

    if piece_value is None or piece_value == 0:
        raise ValueError("piece_value must not be zero!!")

    image = RED_PIECE if piece_value < 0 else BLUE_PIECE
    return image


def get_position(
    index: int, inverse_diff: int, offset: float = 0.0
) -> tuple[float, float]:
    """Following the Dry method this function takes
    in the index and returns the position of whetever
    item.

    Args:
        index (int): the index of the item
        inverse_diff (int): by how much to inverse
        offset (float, optional): extra to the index. Defaults to 0.0.

    Returns:
        tuple[float, float]: position
    """
    global game

    i, j = (index % 8) + offset, (index // 8) + offset

    if game.should_inverse_board:
        i = inverse_diff - i
        j = inverse_diff - j

    x = BOARD_OFFSET + i * CELL_SIZE
    y = BOARD_OFFSET + j * CELL_SIZE

    return x, y


clock = pygame.time.Clock()
active_index: int | None = None
active_piece: int = 0
game = Game(True, None)

should_show_sparks = False
sparks_timer = pygame.time.get_ticks()
sparks_wait_time = 0

last_move_notation = None
sparks = SparksContainer()
made_fireworks = 0

buttons = [
    (Button((714, 472), "AI VS AI", 4, 7, 458, 62, BTN_FONT), (None, None)),
    (Button((714, 543), "PLAY AS BLUE", 4, 7, 458, 62, BTN_FONT), (True, None)),
    (Button((714, 614), "PLAY AS RED", 4, 7, 458, 62, BTN_FONT), (None, True)),
]

while True:
    mx, my = pygame.mouse.get_pos()
    screen.fill(BG_COLOR)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game.board.is_playing and event.type == pygame.MOUSEBUTTONDOWN:
            x = mx - BOARD_OFFSET
            y = my - BOARD_OFFSET

            is_x_okay = 0 <= x <= BOARD_SIZE
            is_y_okay = 0 <= y <= BOARD_SIZE

            index = (y // CELL_SIZE) * 8 + (x // CELL_SIZE)

            if game.should_inverse_board:
                index = (7 - (y // CELL_SIZE)) * 8 + (7 - (x // CELL_SIZE))

            if 0 <= index < 64 and is_x_okay and is_y_okay:

                piece = game.board.piece(index)
                if piece != 0:
                    active_piece = game.board.piece(index)
                    active_index = index
                # else:
                #     screen_shake(500)

        if game.board.is_playing and event.type == pygame.MOUSEBUTTONUP:
            if active_index is not None:
                x = mx - BOARD_OFFSET
                y = my - BOARD_OFFSET

                is_x_okay = 0 <= x <= BOARD_SIZE
                is_y_okay = 0 <= y <= BOARD_SIZE

                index = (y // CELL_SIZE) * 8 + (x // CELL_SIZE)

                if game.should_inverse_board:
                    index = (7 - (y // CELL_SIZE)) * 8 + (7 - (x // CELL_SIZE))

                piece = game.board.piece(index)

                if (
                    active_index != index
                    and game.player_is_there
                    and game.is_players_turn
                ):
                    if (
                        0 <= index < 64
                        and is_x_okay
                        and is_y_okay
                        and game.board.get_notation(index) is not None
                        and game.board.piece(index) == 0
                    ):
                        try:
                            move = game.find_move(active_index, index)
                            game.update_game(move)
                            color = "r" if game.board.piece(index) < 1 else "b"
                            last_move_notation = color = str(
                                game.board.get_notation(index)
                            )

                            if not game.board.is_playing:
                                if game.board.winner is not None:

                                    if (
                                        game.board.winner < 0
                                        and game.red is not None
                                        or game.board.winner > 0
                                        and game.blue is not None
                                    ):
                                        should_show_sparks = True
                                        for _ in range(30):
                                            sparks.create_new_firework()

                                        sparks_timer = pygame.time.get_ticks()

                        except ValueError:
                            pass

                active_index = None

    last_move = game.board.last_move
    pieces = game.board.all_pieces

    if last_move is not None:
        for index in last_move[:2]:  # type: ignore
            x, y = get_position(index, 7)
            screen.blit(MOVE_SQUARE, (x, y))

    for (piece, index) in pieces:
        if index == active_index:
            continue

        x, y = get_position(index, 8, 0.5)

        piece_image = get_piece_image(piece)
        x -= piece_image.get_width() / 2
        y -= piece_image.get_height() / 2

        if abs(piece) % 2 != 0:
            screen.blit(piece_image, (x, y))
        else:
            screen.blit(piece_image, (x, y + 3))
            screen.blit(piece_image, (x, y - 3))

    if game.player_is_there and game.is_players_turn:
        if active_index is not None:
            possible_moves = filter(lambda move: move.start == active_index, game.moves)

            for move in possible_moves:
                i, j = get_position(move.end, 7)

                pygame.draw.rect(
                    screen,
                    pygame.Color("#2AF63E"),
                    pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
                    6,
                )

                for pos in move.move_through + [move.start]:
                    i, j = get_position(pos, 7)

                    pygame.draw.rect(
                        screen,
                        pygame.Color("#F6CE2A"),
                        pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
                        6,
                    )

                for attack_pos in move.kills:
                    i, j = get_position(attack_pos, 7)

                    pygame.draw.rect(
                        screen,
                        pygame.Color("#F62A2A"),
                        pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
                        6,
                    )

        else:
            for pos in game.moves:
                i, j = get_position(pos.start, 7)

                pygame.draw.rect(
                    screen,
                    pygame.Color("#F6CE2A"),
                    pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
                    6,
                )

    if active_index is not None:
        piece_image = get_piece_image(active_piece)
        x = mx - piece_image.get_width() / 2
        y = my - piece_image.get_height() / 2

        i, j = get_position(active_index, 7)

        pygame.draw.rect(
            screen,
            pygame.Color("#F6CE2A"),
            pygame.Rect(i, j, CELL_SIZE, CELL_SIZE),
            6,
        )

        if abs(active_piece) % 2 != 0:
            screen.blit(piece_image, (x, y))
        else:
            screen.blit(piece_image, (x, y + 3))
            screen.blit(piece_image, (x, y - 3))

    for (button, options) in buttons:
        clicked = button.update(screen)

        if not clicked:
            continue

        game.reset_game(*options)

    if not game.board.is_playing:
        screen.blit(BLACK_OVERLAY, (BOARD_OFFSET, BOARD_OFFSET))

        sparks.update(screen)

        if should_show_sparks and made_fireworks <= MAX_NUMBER_OF_FIREWORKS:
            if pygame.time.get_ticks() - sparks_timer > sparks_wait_time:
                for _ in range(random.randint(3, 10)):
                    sparks.create_new_firework()

                sparks_wait_time = random.randint(50, 400)
                sparks_timer = pygame.time.get_ticks()
                made_fireworks += 1

        if game.board.winner is not None:
            if game.board.winner > 0:
                screen.blit(
                    BLUE_WIN_BANNER,
                    (BOARD_OFFSET, (height / 2) - (BLUE_WIN_BANNER.get_height() / 2)),
                )
            else:
                screen.blit(
                    RED_WIN_BANNER,
                    (BOARD_OFFSET, (height / 2) - (RED_WIN_BANNER.get_height() / 2)),
                )

        else:
            screen.blit(
                DRAW_BANNER,
                (BOARD_OFFSET, (height / 2) - (DRAW_BANNER.get_height() / 2)),
            )

        player_won = game.board.winner is not None and (
            (game.board.winner < 0 and game.red is not None)
            or (game.board.winner > 0 and game.blue is not None)
        )
        side = "GAME OVER!!!"
        state_text = "YOU WON!!!!" if player_won else "YOU LOSE!!!"

        if game.board is None:
            state_text = "DRAW!!"

        state_surf = TEXT_FONT.render(side, False, (0, 0, 0))
        msg_surf = TEXT_FONT.render(state_text, False, (0, 0, 0))

        screen.blit(state_surf, (915, 362))
        screen.blit(msg_surf, (915, 392))

        screen.blit(get_piece_image(game.board.winner, True), (789, 340))

    else:
        side = "RED" if game.board.current_side == PieceTypes.RED else "BLUE"
        state_text = "State: " + side

        msg = "AI's THINKING"
        if game.player_is_there and game.is_players_turn:
            msg = "YOUR TURN!!"
        elif not game.player_is_there:
            msg = "AI's PLAYING"

        state_surf = TEXT_FONT.render(state_text, False, (0, 0, 0))
        msg_surf = TEXT_FONT.render(msg, False, (0, 0, 0))

        screen.blit(state_surf, (915, 362))
        screen.blit(msg_surf, (915, 392))

        screen.blit(
            get_piece_image(game.board.current_side.value[0], True),
            (789, 340),
        )

    pygame.display.update()
    clock.tick(60)
