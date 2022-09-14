from .board import Board
from .move import Move, generate_moves


class Game:
    """The Game class for a checkers game"""

    def __init__(self, red=None, blue=None, board: None | list = None):
        self.board = Board(board)
        self.moves: list[Move] = []

        self.is_playing = True
        self.winner: None | int = None
        self.reset_correct_moves()

        self.red = red
        self.blue = blue

    def play_move(self, index: int):
        """Play a move on the Board

        Args:
            index (int): the index of the move
        """
        move = self.moves[index]
        move.play(self.board)
        self.reset_correct_moves()
        is_draw = self.board.is_draw()

        if len(self.moves) == 0 or is_draw:
            if is_draw:
                self.winner = None
            else:
                self.winner = self.board.current_side.value[0] * -1

            self.is_playing = False

    def find_move_index(self, start: int, end: int) -> int:
        """Find the index for the  move based on the start and end
        this is possible only because all the moves are unique

        Args:
            start (int): the start index
            end (int): the end index

        Raises:
            ValueError: this is when the position is not there

        Returns:
            int: the index of the move in the moves list
        """
        for i, move in enumerate(self.moves):
            if move.start == start and move.end == end:
                return i

        raise ValueError(f"Move not Present with start and end: {(start, end)}")

    def reset_correct_moves(self):
        """Resets the game instances correct move
        based on the position
        """
        try:
            self.moves = generate_moves(self.board)
        except Exception as e:
            print(self.board.board)
            raise e
