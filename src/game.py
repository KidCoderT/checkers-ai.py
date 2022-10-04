import time
import threading
from typing import Optional

from .board import Board, PieceTypes
from .move import Move, generate_moves
from .ai import search_best_move


class Game:
    """The Game class for a checkers game
    this also contains the ai gameplay"""

    def __init__(self, blue, red, board: None | list = None):
        self.board = Board(board)
        self.moves: list[Move] = []

        self.reset_correct_moves()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None
        self.comp_is_playing = False

        self.red = red
        self.blue = blue

        # TODO: ADD FOLOWING VARIABLES
        # * - depth searched
        # * - time_taken
        # * - positions evaluated and found

    def make_comp_play(self):
        # TODO: ADD DOCUMENTATION
        # TODO: CHECK TIME TAKEN TO COMPLETE FUNC
        self.comp_is_playing = True

        time.sleep(0.2)
        # random.choice(self.moves).play(self.board)
        # TODO: CHANGE TO SEARCH BEST MOVE & PASS TIME
        search_best_move(self.board).play(self.board)
        self.reset_correct_moves()
        self.board.update_state()

        self.comp_is_playing = False
        self.update_game()

        # TODO: SET THE TIME TAKEN AND NEW VALUES ONCE RETRIEVED

    def update_game(self, move: Optional[Move] = None):
        """Play a move on the Board & updates
        the game state accordingly

        Args:
            move (Move): the move to play
        """

        if move is not None:
            move.play(self.board)
            self.reset_correct_moves()
            self.board.update_state()

        if (
            not self.is_players_turn
            and self.board.is_playing
            and not self.comp_is_playing
        ):
            comp = threading.Thread(target=self.make_comp_play)
            comp.daemon = True
            comp.start()

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
        # TODO: ADD DOCUMENTATION
        self.board.reset()
        self.moves.clear()
        self.reset_correct_moves()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None

        self.red = red
        self.blue = blue

        self.update_game()

    @property
    def is_players_turn(self) -> bool:
        return (self.red is not None and self.board.current_side == PieceTypes.RED) or (
            self.blue is not None and self.board.current_side == PieceTypes.BLUE
        )
