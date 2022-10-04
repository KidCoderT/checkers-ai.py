# pylint: disable=global-statement

import time
from math import inf
from copy import deepcopy

from .move import Move, generate_moves
from .board import Board

POSITIONS = 0
TRANSPOSITION_TABLE = {}
ITERATIVE_DEEPENING_TABLE = {}
WIN_CUT_OFF = 10000000
SHOULD_CUT_OFF = False


def search_all_captures(board: Board, alpha, beta, start_time, time_limit):
    """Search all captures until no more captures are
    possible. this allows more accurate score checking

    Args:
        board (Board): the board
        alpha (_type_): the highest value
        beta (_type_): the worst values
        start_time (_type_): the start_time
        time_limit (_type_): the time limit for the search

    Returns:
        _type_: the score
    """
    global POSITIONS, SHOULD_CUT_OFF
    evaluation = board.score

    if time.monotonic() - start_time > time_limit:
        SHOULD_CUT_OFF = True
        return 0

    if evaluation >= beta:
        POSITIONS += 1
        return beta

    alpha = max(alpha, evaluation)
    all_moves = generate_moves(board)

    try:
        if not all_moves[0].is_killing_move:
            POSITIONS += 1
            return alpha
    except IndexError:
        return evaluation

    for move in all_moves:
        move.play(board)
        evaluation = -search_all_captures(board, -beta, -alpha, start_time, time_limit)
        board.undo_move()

        if evaluation >= beta:
            POSITIONS += 1
            return beta

        alpha = max(alpha, evaluation)

    return alpha


def search(board: Board, depth: int, alpha, beta, start_time, time_limit) -> float:
    global POSITIONS, TRANSPOSITION_TABLE, SHOULD_CUT_OFF, ITERATIVE_DEEPENING_TABLE
    board.update_state()

    if time.monotonic() - start_time > time_limit:
        SHOULD_CUT_OFF = True
        return 0

    key = board.hash()

    if key in TRANSPOSITION_TABLE[depth]:
        return TRANSPOSITION_TABLE[depth][key]

    if depth == 0:
        POSITIONS += 1
        score = search_all_captures(board, alpha, beta, start_time, time_limit)
        TRANSPOSITION_TABLE[depth][key] = score
        return score

    if not board.is_playing:
        POSITIONS += 1
        score = board.score
        TRANSPOSITION_TABLE[depth][key] = score
        return score

    try:
        # check if depth present
        ITERATIVE_DEEPENING_TABLE[depth]
    except KeyError:
        # the depth is not there sc create it
        ITERATIVE_DEEPENING_TABLE[depth] = []
    finally:
        all_moves = []

        if len(ITERATIVE_DEEPENING_TABLE[depth]) > 0:
            all_moves = ITERATIVE_DEEPENING_TABLE[depth]

        else:
            all_moves = generate_moves(board)

            def score_move(move: Move):
                move_score = 0

                weak_piece = abs(board.piece(move.start)) == 1
                on_kill_king = 4 if weak_piece else 2

                for index in move.kills:
                    if abs(board.piece(index)) == 2:
                        move_score += on_kill_king
                        continue

                    move_score += 2

                if move.make_king:
                    move_score += 3

                return move_score

            all_moves.sort(key=score_move)

    moves_score = []

    best_val = -inf
    for move in all_moves:
        move.play(board)
        evaluation = -search(board, depth - 1, -beta, -alpha, start_time, time_limit)

        # add the evaluation score
        moves_score.append(evaluation)

        board.undo_move()

        if evaluation >= beta:
            POSITIONS += 1
            TRANSPOSITION_TABLE[depth][key] = beta
            return beta

        alpha = max(best_val, evaluation)

    arranged_moves = list(
        map(lambda x: x[0], sorted(zip(all_moves, moves_score), key=lambda x: x[1]))
    )
    ITERATIVE_DEEPENING_TABLE[depth] = arranged_moves

    return alpha


#  DONE -TODO: CREATE ITERATIVE DEEPENING FUNC (board, time limit)
def iterative_deepening(board: Board, time_limit: float) -> tuple[float, float]:
    """This is the Function that using iterative_deepening
    searches as far as possible into each and every move based
    on the given time limit

    Args:
        board (Board): the board
        time_limit (float): the time limit for the search

    Returns:
        tuple[float, float]: score, depth searched
    """
    global SHOULD_CUT_OFF, TRANSPOSITION_TABLE, ITERATIVE_DEEPENING_TABLE

    start_time = time.monotonic()
    SHOULD_CUT_OFF = False
    depth = 1
    score = 0

    # should reset for every search
    ITERATIVE_DEEPENING_TABLE = {}

    while not SHOULD_CUT_OFF:
        # cut of if time passed
        if time.monotonic() - start_time > time_limit:
            SHOULD_CUT_OFF = True
            continue

        # resting transpositionTable for every depth
        TRANSPOSITION_TABLE = {key: {} for key in range(depth + 1)}
        search_score = search(board, depth, -inf, inf, start_time, time_limit)

        # cut of if found winning move
        if search_score >= 50000000:
            return search_score, depth

        if not SHOULD_CUT_OFF:
            score = search_score

        # update the depth for the next search
        depth += 1

        # update iterative_deepening table
        ITERATIVE_DEEPENING_TABLE = {
            key + 1: value for (key, value) in ITERATIVE_DEEPENING_TABLE.items()
        }
        print(ITERATIVE_DEEPENING_TABLE)

    return score, depth - 1


def search_best_move(real_board: Board, wait_time: int) -> tuple[Move, float, float]:
    """This is the high level function that when given
    a board and the time limit it can search
    using iterative deepening it searches for it until
    the given time limit is reached after which it returns
    the best move.

    Args:
        real_board (Board): the board to search the best move
        wait_time (int): the wait time the ai can afford

    Returns:
        tuple[Move, int, int]: best move, positions checked, max depth
    """
    global POSITIONS, TRANSPOSITION_TABLE

    best_score = -inf
    all_moves = generate_moves(real_board)
    best_move = all_moves[0]

    if len(all_moves) == 1:  # killing move only
        return best_move, 0, 0

    POSITIONS = 0
    positions = 0
    depth = 1

    # calculating time for searching each move
    search_time_limit = wait_time / len(all_moves)

    for move in all_moves:
        board = deepcopy(real_board)

        move.play(board)
        search_score, search_depth = iterative_deepening(board, search_time_limit)

        # found win move
        if search_score >= WIN_CUT_OFF:
            return best_move, depth, positions

        is_best_score = search_score >= best_score

        # update values if is the best score
        if is_best_score:
            best_score = search_score

        depth = max(search_depth, depth)
        positions = POSITIONS
        best_move = move

        board.undo_move()

    return best_move, positions, depth
