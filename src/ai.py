# pylint: disable=global-statement

import time
from math import inf
from copy import deepcopy

from .move import Move, generate_moves
from .board import Board

DEPTH = 6  # TODO: DELETER THIS
POSITIONS = 0
TRANSPOSITION_TABLE = {key: {} for key in range(DEPTH)}
# TODO: ADD ITERATIVE DEEPENING TABLE


def search_all_captures(board: Board, alpha, beta):
    # TODO: ADD DOCUMENTATION
    global POSITIONS
    evaluation = board.score

    # TODO: IF TIME LIMIT REACHED END PROCESS

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
        evaluation = -search_all_captures(board, -beta, -alpha)
        board.undo_move()

        if evaluation >= beta:
            POSITIONS += 1
            return beta

        alpha = max(alpha, evaluation)

    return alpha


def search(board: Board, depth: int, alpha, beta) -> float:
    global POSITIONS, TRANSPOSITION_TABLE
    all_moves = generate_moves(board)
    board.update_state()

    # TODO: IF TIME LIMIT REACHED END PROCESS

    key = board.hash()

    if key in TRANSPOSITION_TABLE[depth]:
        return TRANSPOSITION_TABLE[depth][key]

    if depth == 0:
        POSITIONS += 1
        score = search_all_captures(board, alpha, beta)
        TRANSPOSITION_TABLE[depth][key] = score
        return score

    if not board.is_playing:
        POSITIONS += 1
        score = board.score
        TRANSPOSITION_TABLE[depth][key] = score
        return score

    # TODO: CHECK IF DEPTH SEEN BEFORE
    # ? - if so then use that
    # ? - otherwise get moves and do move_ordering
    # move ordering
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

    # TODO: SAVE SCORE OF ALL THE MOVES

    best_val = -inf
    for move in all_moves:
        move.play(board)
        evaluation = -search(board, depth - 1, -beta, -alpha)
        board.undo_move()

        if evaluation >= beta:
            POSITIONS += 1
            TRANSPOSITION_TABLE[depth][key] = beta
            return beta

        alpha = max(best_val, evaluation)

    # TODO: SORT THE MOVES BASED ON THE SCORES
    # TODO: SET THAT AS THE DEPTH SCORE

    return alpha


# TODO: CREATE ITERATIVE DEEPENING FUNC (board, time limit)
# - while time limit not passed
# -     search to new depth
# -     if score of new_depth found win return
# -     if time limit not passed:
#           - set new depth, add new position no. & set new score
# -     else: break
# -     depth ++
# - return score, depth, position no.

# TODO: RENAME TO SEARCH_BEST_MOVE
# - calculate time to give each move
# - for move in possible_move
# -     do iterative search for the move
# -     if score > best_score:
# -         best_score = score
# -         best_move = move
# - return best move, positions_searched, evals_made
def get_best_move(real_board: Board) -> Move:
    global POSITIONS, TRANSPOSITION_TABLE

    start_time = time.monotonic()
    board = deepcopy(real_board)

    best_val = -inf
    all_moves = generate_moves(board)
    best_move = all_moves[0]

    POSITIONS = 0
    TRANSPOSITION_TABLE = {key: {} for key in range(DEPTH + 1)}

    if len(all_moves) == 1:
        print(0)
        return best_move

    for move in all_moves:
        move.play(board)
        value = -search(board, DEPTH, -inf, inf)
        is_best_val = value >= best_val

        if is_best_val:
            best_val = value
            best_move = move

        board.undo_move()

    end_time = time.monotonic()

    print(end_time - start_time, POSITIONS)
    return best_move
