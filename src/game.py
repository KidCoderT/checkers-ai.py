import time
import threading
from typing import Optional

from .board import Board, PieceTypes
from .move import Move, generate_moves
from .ai import search_best_move

TIME_LIMIT_FOR_SEARCH = 6


class Game:
    """The Game class for a checkers game
    this also contains the ai game play"""

    def __init__(self, blue, red, board: None | list = None):
        self.board = Board(board)
        self.moves: list[Move] = []

        self.reset_correct_moves()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None
        self.comp_is_playing = False

        self.red = red
        self.blue = blue

        self.ai_time = 0
        self.start_time = 0
        self.depth_searched = 0
        self.positions_evaluated = 0

        self.process: list[threading.Thread] = []

    def make_comp_play(self):
        """Makes the computer play and
        stores the return from the computer.
        This is important for the multithreading
        need in this function
        """
        self.start_time = time.monotonic()
        self.comp_is_playing = True

        if not self.player_is_there:
            time.sleep(0.3)

        time_limit_for_play = TIME_LIMIT_FOR_SEARCH if self.player_is_there else 2
        move, positions_checked, max_depth_searched = search_best_move(
            self.board, time_limit_for_play
        )
        move.play(self.board)
        self.reset_correct_moves()
        self.board.update_state()

        self.comp_is_playing = False
        self.update_game()

        time_taken = time.monotonic() - self.start_time
        self.depth_searched = max_depth_searched
        self.positions_evaluated = positions_checked
        self.ai_time = time_taken

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
            if 0:
                comp = threading.Thread(target=self.make_comp_play)
                comp.daemon = True
                self.process.append(comp)
                comp.start()
            else:
                self.make_comp_play()

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

    def __stop_all_process(self):
        self.comp_is_playing = False
        for process in self.process:
            process.join()

        self.process.clear()
        self.board.reset()
        self.moves.clear()
        self.reset_correct_moves()
        self.update_game()

    def reset_game(self, blue, red):
        """Resets the Game to the original state
        and sets it up for the new game

        Args:
            blue (_type_): is blue being played
            red (_type_): is red being played
        """
        self.board.clear()

        reset_process_thread = threading.Thread(target=self.__stop_all_process)
        reset_process_thread.daemon = True
        reset_process_thread.start()

        self.should_inverse_board = blue is None and red is not None
        self.player_is_there = blue is not None or red is not None

        self.red = red
        self.blue = blue

        self.ai_time = 0
        self.start_time = 0
        self.depth_searched = 0
        self.positions_evaluated = 0

    @property
    def is_players_turn(self) -> bool:
        """Checks whether or not it currently is the players
        turn! if there is no player by default it will return False
        """
        return (self.red is not None and self.board.current_side == PieceTypes.RED) or (
            self.blue is not None and self.board.current_side == PieceTypes.BLUE
        )
