# pylint: disable=dangerous-default-value
from .board import Board

NUM_SQUARES_TO_EDGE = [(0, 0, 0, 0) for _ in range(64)]
DIRECTIONAL_OFFSET = (7, 9, -7, -9)

for row in range(8):
    for column in range(8):
        index = column * 8 + row

        dist_north: int = 7 - column
        dist_south: int = column
        dist_east: int = 7 - row
        dist_west: int = row

        NUM_SQUARES_TO_EDGE[index] = (  # type: ignore
            min(dist_north, dist_west),
            min(dist_north, dist_east),
            min(dist_south, dist_east),
            min(dist_south, dist_west),
        )

        del index


class Move:
    """This contains data for any and all moves
    and also can play the move on the board
    """

    def __init__(
        self,
        piece: int,
        start: int,
        end: int,
        kill: list[int] = [],
        move_through: list[int] = [],
    ):
        self.start = start
        self.end = end
        self.kill = kill
        self.move_through = move_through

        self.is_killing_move = len(kill) > 0
        self.make_king = False

        if abs(piece) % 2 != 0 and end // 8 in [0, 7]:
            self.make_king = True

    def play(self, board: Board):
        """Plays a move on the Board
        Args:
            board (Board): the board to update
        """
        board.move(self.start, self.end)

        for index in self.kill:
            board.kill_piece(index)

        if self.make_king:
            board.make_king(self.end)

    def __str__(self):
        return f"{self.start} -> {self.end} | making king - {self.make_king}"


def generate_sliding_moves(piece: int, start: int, board: Board) -> list[Move]:
    """Generate all the sliding moves for a piece

    Args:
        piece (int): the piece
        start (int): the start position
        board (Board): the board where the piece is present

    Returns:
        list[Move]: the number of moves possible by the piece
    """
    is_king = piece % 2 == 0
    move = []

    start_direction_index = 0
    end_direction_index = 4

    if is_king:
        end_direction_index = 4
    elif piece < 0:
        end_direction_index = 2
    else:
        start_direction_index = 2

    for offset in range(start_direction_index, end_direction_index):
        if NUM_SQUARES_TO_EDGE[start][offset] > 0:
            target_square = start + DIRECTIONAL_OFFSET[offset]
            target_contains_piece = board.piece(target_square) != 0

            if target_contains_piece:
                continue

            new_move = Move(piece, start, target_square)
            move.append(new_move)

    return move


def generate_attacking_moves(piece: int, start: int, board: Board) -> list[Move]:
    """Generate all the sliding moves for a piece

    Args:
        piece (int): the piece
        start (int): the start position
        board (Board): the board where the piece is present

    Returns:
        list[Move]: the number of moves possible by the piece
    """
    is_king = piece % 2 == 0
    move = []

    opposite_piece = (
        Board.PieceTypes.RED
        if piece in Board.PieceTypes.BLUE.value
        else Board.PieceTypes.BLUE
    )

    start_direction_index = 0
    end_direction_index = 4

    if is_king:
        end_direction_index = 4
    elif piece < 0:
        end_direction_index = 2
    else:
        start_direction_index = 2

    offsets = range(start_direction_index, end_direction_index)
    attack_positions = []  # current position, kill position, moved through position

    for offset in offsets:
        if NUM_SQUARES_TO_EDGE[start][offset] >= 2:
            kill_piece = start + DIRECTIONAL_OFFSET[offset]
            final_index = start + DIRECTIONAL_OFFSET[offset] * 2

            if (
                board.piece(kill_piece) in opposite_piece.value
                and board.piece(final_index) == 0
            ):
                attack_positions.append((final_index, [kill_piece], []))

    while len(attack_positions) > 0:
        attack = attack_positions.pop(0)
        move.append(Move(piece, start, attack[0], attack[1], attack[2]))

        for offset in offsets:
            if NUM_SQUARES_TO_EDGE[attack[0]][offset] >= 2:
                kill_piece = attack[0] + DIRECTIONAL_OFFSET[offset]
                final_index = attack[0] + DIRECTIONAL_OFFSET[offset] * 2

                if (
                    board.piece(kill_piece) in opposite_piece.value
                    and board.piece(final_index) == 0
                ):
                    if attack[1][-1] != kill_piece:
                        attack_positions.append(
                            (
                                final_index,
                                attack[1] + [kill_piece],
                                attack[2] + [attack[0]],
                            )
                        )

    return move


def generate_moves(board: Board) -> list[Move]:
    """Generate all the possible moves for
    all the pieces on the board
    and returns a list of moves

    Args:
        board (Board): The board

    Returns:
        list[Move]: the moves
    """

    # TODO: Add multiprocessing

    attacking_moves = []
    max_kills = -100

    sliding_moves = []

    pieces = board.all_pieces
    for (piece, start) in pieces:
        if piece in board.current_side.value:

            piece_attack_moves = generate_attacking_moves(piece, start, board)

            for move in piece_attack_moves:
                if len(move.kill) > max_kills:
                    attacking_moves = [move]
                    max_kills = len(move.kill)

                elif len(move.kill) == max_kills:
                    attacking_moves.append(move)

                else:
                    continue

            if len(attacking_moves) <= 0:
                sliding_moves = sliding_moves + generate_sliding_moves(
                    piece, start, board
                )

    if len(attacking_moves) <= 0:
        return sliding_moves

    return attacking_moves
