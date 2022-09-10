from operator import xor
from .board import Board
from .move import Move, generate_moves


class Game:
    def __init__(
        self,
        red=None,
        blue=None,
    ):
        self.board = Board()
        self.moves: list[Move] = generate_moves(self.board)

        self.red = red
        self.blue = blue

        self.should_inverse_board = blue is None and red is not None
        self.mouse_allowed = self.red is not None or self.blue is not None

    def play_move(self, index: int):
        move = self.moves[index]
        move.play(self.board)
        self.moves = generate_moves(self.board)

    def find_move_index(self, start: int, end: int) -> int:
        """Find the index for the  move based on the start and end
        this is possible only because all the moves are unique

        Args:
            start (int): the start index
            end (int): the end index

        Raises:
            Exception: this is when the position is not there

        Returns:
            int: the index of the move in the moves list
        """
        for i, move in enumerate(self.moves):
            if move.start == start and move.end == end:
                return i

        raise Exception(f"Move not Present with start and end: {(start, end)}")
