from math import inf
import numpy as np
from .move import generate_sliding_moves, generate_attacking_moves
from .utils import PieceTypes, POSITION_NOTATIONS


class Board:
    """The Board Class contains the
    board to play the game on
    """

    def __init__(self, board, current_side: PieceTypes = PieceTypes.BLUE):
        if board is None:
            self.__board = np.zeros(64, dtype=np.dtype(int))
            self.__default_arrange_pieces()

        else:
            self.__board = np.array(board, dtype=np.dtype(int))

        self.current_side = current_side
        self.__made_moves = []

        self.is_playing = True
        self.winner: None | int = None
        self.moves_without_kills = 0

    def reset(self):
        """Resets the Board to the initial state"""
        self.__default_arrange_pieces()
        self.current_side = PieceTypes.BLUE
        self.__made_moves = []

        self.is_playing = True
        self.winner: None | int = None
        self.moves_without_kills = 0

    @property
    def all_pieces(self):
        """Gets all the piece index on the board and returns
        them as an iterator where each element is a tuple
        that is in the form of (piece, index)"""

        indices = np.where(self.__board != 0)[0]
        pieces = map(lambda x: (self.__board[x], x), indices)
        return pieces

    def piece(self, index: int) -> int:
        """Gets a Piece from the board

        Args:
            index (int): the piece index

        Returns: the piece
        """
        return self.__board[index]

    def __default_arrange_pieces(self):
        """Sets up the board pieces"""
        self.__board = np.zeros(64, dtype=np.dtype(int))

        # setup red pieces
        for i in range(3):
            is_even = i % 2 == 0
            for j in range(4):

                row = i
                column = j * 2
                if is_even:
                    column += 1

                index = (row * 8) + column
                self.__board[index] = -1

        # setup blue pieces
        for i in range(5, 8):
            is_even = i % 2 == 0
            for j in range(4):

                row = i
                column = j * 2
                if is_even:
                    column += 1

                index = (row * 8) + column
                self.__board[index] = 1

    @property
    def last_move(self) -> list | None:
        """Gives u the last move made and if its the beggining of the game
        then it returns None

        Returns:
            list: (old_position, new_position, kill_positions, made_king)
        """
        return self.__made_moves[-1] if len(self.__made_moves) > 0 else None

    def get_notation(self, index: int) -> int | None:
        """Gets the notation for a move on the board
        this can also be used to validate wheter a move is valid
        or not!
        Args:
            index (int): the position to get the notation for
        Returns:
            int | None: position notation
        """
        return POSITION_NOTATIONS[index]

    def move(self, old_index: int, new_index: int):
        """Moves Piece from old_index to new_index

        Args:
            old_index (int): the current position of the piece
            new_index (int): the new position for the piece

        Raises:
            IndexError: If you try to move the piece to an occupied position
            IndexError: If you try to move a non existent piece
        """
        if self.__board[new_index] != 0:
            raise IndexError("You cant move a piece to an occupied square")

        if self.__board[old_index] == 0:
            raise IndexError("You cant move a non existent piece!")

        piece = self.__board[old_index]
        self.__board[old_index] = 0
        self.__board[new_index] = piece

        self.__made_moves.append(
            [old_index, new_index, [], False, self.moves_without_kills]
        )
        self.moves_without_kills += 1

        if self.current_side == PieceTypes.BLUE:
            self.current_side = PieceTypes.RED
        else:
            self.current_side = PieceTypes.BLUE

    def kill_piece(self, index: int):
        """Kills / removes a piece from the board

        Args:
            index (int): the index to kill

        Raises:
            IndexError: when it tries to kill a piece
                that is nonexistent
        """
        if self.__board[index] == 0:
            raise IndexError("Cannot kill a non existent piece")

        self.__made_moves[-1][2].append((index, self.__board[index]))
        self.moves_without_kills = 0
        self.__board[index] = 0

    def make_king(self, index: int):
        """Makes a Piece at the given index a king

        Args:
            index (int): the index of the piece

        Raises:
            IndexError: if the position is not at the edges
            IndexError: if there is no piece at the given index
        """
        if index // 8 not in [0, 7]:
            raise IndexError("Piece can only promote if Reaches the Edges!!")

        if self.piece(index) == 0:
            raise IndexError("You cant king a non existent piece")

        self.__board[index] = self.__board[index] * 2
        self.__made_moves[-1][3] = True

    def undo_move(self):
        """Undo the last made move"""
        last_move = self.__made_moves.pop()

        if last_move[3]:
            self.__board[last_move[1]] = self.__board[last_move[1]] // 2

        for (index, piece) in last_move[2]:  # type: ignore
            self.__board[index] = piece

        piece = self.__board[last_move[1]]
        self.__board[last_move[1]] = 0
        self.__board[last_move[0]] = piece

        self.moves_without_kills = last_move[4]

        if self.current_side == PieceTypes.BLUE:
            self.current_side = PieceTypes.RED
        else:
            self.current_side = PieceTypes.BLUE

    @property
    def board(self) -> list:
        """Gives the Board Representation

        Returns:
            numpy array
        """
        return self.__board.tolist()

    def is_draw(self) -> bool:
        """Check wether or not the board state
        is draw or not

        Returns:
            bool: wether or not it is a draw
        """
        is_draw = self.moves_without_kills >= 40

        if self.current_side == PieceTypes.BLUE:
            try:

                last_three_blue_moves = list(
                    map(
                        lambda index: sorted(self.__made_moves[index][:2]),
                        range(-2, -8, -2),
                    )
                )
                last_three_red_moves = list(
                    map(
                        lambda index: sorted(self.__made_moves[index][:2]),
                        range(-1, -6, -2),
                    )
                )

                if (
                    last_three_blue_moves[0]
                    == last_three_blue_moves[1]
                    == last_three_blue_moves[2]
                    and last_three_red_moves[0]
                    == last_three_red_moves[1]
                    == last_three_red_moves[2]
                ):
                    is_draw = True

            except IndexError:
                is_draw = False

        if is_draw:
            self.winner = None
            self.is_playing = False

        return is_draw

    @property
    def score(self) -> int | float:
        """Gets the Score of the Board!"""

        # TODO: FIX SCORE
        # * IF WINNING GIVE INF
        # * IF DRAW GIVE 0

        # * SUM THE WHOLE BOARD * 2 * ENDGAME_WEIGHT
        # * LEN ( BLUE MOVES ) - LEN ( RED MOVES )
        # * TOWARDS THE END FORCE OPPONENTS TO EDGES
        # * TOWARDS THE END FORCE MYSELF TO CENTER

        # * IF CURRENT IS RED: SCORE *= -1

        self.update_state()

        if not self.is_playing:
            if self.winner is not None:
                return inf * self.winner
            return 0

        score = sum(map(lambda x: x[0], filter(lambda x: x[0] != 0, self.all_pieces)))

        if self.current_side == PieceTypes.RED:
            score *= -1

        return score

    def update_state(self):
        """Checks the State of the Game
        whether its draw or if someone won!!
        """
        is_draw = self.is_draw()

        if is_draw:
            return

        is_moves_possible = False
        pieces = self.all_pieces
        board = self.board  # type: ignore

        for (piece, start) in pieces:
            if piece in self.current_side.value:

                piece_attack_moves = generate_attacking_moves(piece, start, board)
                piece_sliding_moves = generate_sliding_moves(piece, start, board)

                if len(piece_attack_moves) > 0 or len(piece_sliding_moves) > 0:
                    is_moves_possible = True
                    break

        if not is_moves_possible:
            self.winner = self.current_side.value[0] * -1
            self.is_playing = False

    def hash(self):
        # TODO: ADD DOCUMENTATION
        return str(self.board)
