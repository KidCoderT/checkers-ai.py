import numpy as np


class Board:
    def __init__(self):
        self.__board = np.zeros(64)
        self.__setup_pieces()

    @property
    def all_pieces(self):
        """Gets all the piece index on the board and returns
        them as red, blue where red and blue are numpy arrays
        containing the index of the red and blue pieces respectively"""
        red = np.where(self.__board < 0)[0]
        blue = np.where(self.__board > 0)[0]
        return (red, blue)

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

    def __setup_pieces(self):
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
