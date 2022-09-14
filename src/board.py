from enum import Enum
import numpy as np


class Board:
    """The Board Class contains the
    board to play the game on
    """

    class PieceTypes(Enum):
        RED = (-1, -2)
        BLUE = (1, 2)

    def __init__(self, board):
        if board is None:
            self.__board = np.zeros(64, dtype=np.dtype(int))
            self.__default_arrange_pieces()

        else:
            self.__board = np.array(board, dtype=np.dtype(int))

        self.position_notations = []
        self.current_side = self.PieceTypes.BLUE

        index = 1
        for i in range(8):
            is_even = i % 2 == 0
            for j in range(8):

                if is_even and j % 2 == 0:
                    self.position_notations.append(None)
                    continue

                if not is_even and j % 2 != 0:
                    self.position_notations.append(None)
                    continue

                self.position_notations.append(index)
                index += 1

        self.__made_moves = []

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

        self.__made_moves.append((old_index, new_index))

        if self.current_side == self.PieceTypes.BLUE:
            self.current_side = self.PieceTypes.RED
        else:
            self.current_side = self.PieceTypes.BLUE

    def __default_arrange_pieces(self):
        """Sets up the board pieces"""

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
    def last_move(self) -> tuple[int, int] | None:
        """Gives u the last move made and if its the beggining of the game
        then it returns None

        Returns:
            tuple: (old_position, new_position)
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
        return self.position_notations[index]

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
        self.__made_moves[-1] = tuple(list(self.__made_moves[-1]) + [True])

    def undo_move(self):
        """Undo the last made move"""
        last_move = self.__made_moves.pop()

        if len(last_move) == 3:
            self.__board[last_move[2]] = self.__board[last_move[2]] // 2

        self.move(*last_move[:2])

    @property
    def board(self):
        """Gives the Board Representation

        Returns:
            numpy array
        """
        return self.__board.tolist()
