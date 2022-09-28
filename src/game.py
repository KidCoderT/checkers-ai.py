from .board import Board
from .move import Move, generate_moves


class Game:
    """The Game class for a checkers game"""

    def __init__(self, blue, red, board: None | list = None):
        self.board = Board(board)
        self.moves: list[Move] = []

        self.is_playing = True
        self.winner: None | int = None
        self.reset_correct_moves()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None

        self.red = red
        self.blue = blue

    def update_game(self, move: Move):
        """Play a move on the Board & updates
        the game state accordingly

        Args:
            move (Move): the move to play
        """
        move.play(self.board)
        self.reset_correct_moves()
        is_draw = self.board.is_draw()

        if len(self.moves) == 0 or is_draw:
            if is_draw:
                self.winner = None
            else:
                self.winner = self.board.current_side.value[0] * -1

            self.is_playing = False

    def find_move(self, start: int, end: int) -> Move:
        """Find the index for the  move based on the start and end
        this is possible only because all the moves are unique

        Args:
            start (int): the start index
            end (int): the end index

        Raises:
            ValueError: this is when the position is not there

        Returns:
            Move: the move to be played
        """
        for move in self.moves:
            if move.start == start and move.end == end:
                return move

        raise ValueError(f"Move not Present with start and end: {(start, end)}")

    def reset_correct_moves(self):
        """Resets the game instances correct move
        based on the position
        """
        self.moves = generate_moves(self.board)

    def reset_game(self, blue, red):
        self.board.reset()
        self.moves.clear()

        self.is_playing = True
        self.winner = None
        self.reset_correct_moves()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None

        self.red = red
        self.blue = blue

    @property
    def is_players_turn(self) -> bool:
        return (
            self.red is not None
            and self.board.current_side == self.board.PieceTypes.RED
        ) or (
            self.blue is not None
            and self.board.current_side == self.board.PieceTypes.BLUE
        )
