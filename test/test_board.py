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
    pieces = map(lambda x: x[1], board.all_pieces)

    assert 28 in pieces
    assert 35 in pieces

    with pytest.raises(IndexError, match="You cant move a piece to an occupied square"):
        board.move(1, 8)

    with pytest.raises(IndexError, match="You cant move a non existent piece!"):
        board.move(0, 25)


@pytest.mark.parametrize(
    "old_index, new_index", [(10, 28), (49, 35), (51, 37), (17, 26), (1, 29), (5, 26)]
)
def test_get_piece(board, old_index, new_index):
    """Test the Get Piece Method"""

    assert board.piece(old_index) != 0.0
    assert board.piece(new_index) == 0.0

    board.move(old_index, new_index)

    assert board.piece(old_index) == 0.0
    assert board.piece(new_index) != 0.0


@pytest.mark.parametrize(
    "move_data",
    [
        [(49, 35), (10, 28), (51, 37), (17, 26)],
        [(49, 35), (10, 28)],
        [(5, 26)],
        [(10, 28), (49, 35), (1, 29), (51, 37), (17, 24), (5, 26)],
    ],
)
def test_get_last_move(board, move_data):
    """Test Last Method Works"""
    assert board.last_move is None

    for move in move_data:
        board.move(*move)
        assert board.last_move == move

    assert board.last_move == move_data[-1]
