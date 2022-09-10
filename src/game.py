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

        if self.red is not None and self.blue is not None:
            raise Exception("Red and Blue Both cannot be controlled by the mouse")

        self.should_inverse_board = red is not None
        self.mouse_allowed = xor(self.red is not None, self.blue is not None)

    def play_move(self, index: int):
        move = self.moves[index]
        move.play(self.board)
        self.moves = generate_moves(self.board)
