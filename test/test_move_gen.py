import pytest
from src.board import Board
from src.move import Move, generate_moves, generate_sliding_moves

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


def test_sliding_moves_generation(board):
    """Tests whether or not the sliding moves
    are being generated or not
    """
    moves = generate_moves(board, only_sliding=True)
    assert len(moves) > 0
