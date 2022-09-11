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


class Move:
    """This contains data for any and all moves
    and also can play the move on the board
    """

    def __init__(self, piece: int, start: int, end: int, kill: list[int]):
        self.start = start
        self.end = end
        self.kill = kill

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

            new_move = Move(piece, start, target_square, [])
            move.append(new_move)

    return move


def generate_moves(
    board: Board, only_sliding=False, only_attacking=False
) -> list[Move]:
    """Generate all the possible moves for
    all the pieces on the board
    and returns a list of moves

    Args:
        board (Board): The board

    Returns:
        list[Move]: the moves
    """
    moves: list[Move] = []

    if only_sliding:
        should_generate_sliding_move = True
        should_generate_attacking_move = False

    elif only_attacking:
        should_generate_sliding_move = False
        should_generate_attacking_move = True

    else:
        should_generate_sliding_move = True
        should_generate_attacking_move = True

    pieces = board.all_pieces
    for (piece, start) in pieces:
        if piece in board.current_side.value:

            sliding_moves = []
            if should_generate_sliding_move:
                sliding_moves = generate_sliding_moves(piece, start, board)

            attacking_moves = []
            if should_generate_attacking_move:
                # attacking_moves = generate_attacking_moves(piece, start, board)
                attacking_moves = []

            moves = moves + sliding_moves + attacking_moves

    return moves
