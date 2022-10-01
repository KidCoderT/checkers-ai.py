import time
from math import inf
from .board import Board
from .move import Move, generate_moves
from copy import deepcopy

# // TODO: MOVE ORDERING
# // TODO: CHECK HOW MANY POSITIONS EVALUATED
# TODO: TRANSPOSITION TABLE
# // TODO: MOVE UNTIL NO CAPTURE
# TODO: TOWARDS THE END MOVE PIECES TO EDGES
# TODO: OPENING
# TODO: ITERATIVE DEEPENING

POSITIONS = 0


def search_all_captures(board: Board, alpha, beta):
    global POSITIONS
    evaluation = board.score

    if evaluation >= beta:
        POSITIONS += 1
        return beta

    alpha = max(alpha, evaluation)
    all_moves = generate_moves(board)

    if not all_moves[0].is_killing_move:
        POSITIONS += 1
        return alpha

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
    global POSITIONS
    all_moves = generate_moves(board)
    board.update_state()

    if depth == 0:
        POSITIONS += 1
        return search_all_captures(board, alpha, beta)

    if not board.is_playing:
        POSITIONS += 1
        return board.score

    # move ordering
    def score_move(move: Move):
        move_score = 0

        weak_piece = abs(board.piece(move.start)) == 1
        weak_on_kill_king = 6 if weak_piece else 4

        for index in move.kills:
            if abs(board.piece(index)) == 2:
                move_score += weak_on_kill_king
                continue

            move_score += 2

        if move.make_king:
            move_score += 5

        return move_score

    all_moves.sort(key=score_move)

    best_val = -inf
    for move in all_moves:
        move.play(board)
        evaluation = -search(board, depth - 1, -beta, -alpha)
        board.undo_move()

        if evaluation >= beta:
            POSITIONS += 1
            return beta

        alpha = max(best_val, evaluation)
    return alpha


def get_best_move(real_board: Board) -> Move:
    global POSITIONS

    start_time = time.monotonic()
    board = deepcopy(real_board)

    best_val = -inf
    all_moves = generate_moves(board)
    best_move = all_moves[0]

    POSITIONS = 0

    if len(all_moves) == 1:
        print(0)
        return best_move

    for move in all_moves:
        move.play(board)
        value = -search(board, 10, -inf, inf)
        is_best_val = value >= best_val

        if is_best_val:
            best_val = value
            best_move = move

        board.undo_move()

    end_time = time.monotonic()

    print(end_time - start_time, POSITIONS)
    return best_move
