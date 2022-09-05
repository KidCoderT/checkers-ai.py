import pytest
from src.board import Board

# pylint: disable=redefined-outer-name


@pytest.fixture()
def board():
    """A pytest fixture
    that allows me to create a new board
    instance for every test

    Yields:
        Board: The Created Board Instance
    """
    board = Board()
    yield board

    del board


def test_pieces_are_present(board):
    """Tests whether or not all the pieces in the board
    are present or not!
    """
    pieces = list(board.all_pieces)
    assert len(pieces) == 24


def test_move_piece(board):
    """Tests whether or not the move method works
    1. Test that the move method moves the piece
    2. Test that the move raises error when moving
        to filled position
    3. Test that the move raises error when moving
        an empty position
    """
    board.move(10, 28)
    board.move(49, 35)
    red, blue = board.all_pieces

    assert 28 in red
    assert 35 in blue

    with pytest.raises(IndexError, match="You cant move a piece to an occupied square"):
        board.move(1, 8)

    with pytest.raises(IndexError, match="You cant move a non existent piece!"):
        board.move(0, 25)
