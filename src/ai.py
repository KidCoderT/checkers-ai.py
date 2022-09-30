from math import inf as infinity
from .board import Board, PieceTypes
from .move import Move, generate_moves


def minimax(board: Board, is_maximizing_player: bool) -> float:
    all_moves = generate_moves(board)
    board.update_state(len(all_moves))

    if board.winner is not None or not board.is_playing:
        return board.score

    if is_maximizing_player:
        best_val = -infinity
        for move in all_moves:
            move.play(board)
            evaluation = minimax(board, False)
            board.undo_move()

            best_val = max(best_val, evaluation)
        return best_val

    else:
        best_val = infinity
        for move in all_moves:
            move.play(board)
            evaluation = minimax(board, True)
            board.undo_move()

            best_val = min(best_val, evaluation)
        return best_val


def get_best_move(board: Board) -> Move:
    best_val = -infinity
    all_moves = generate_moves(board)
    best_move = all_moves[0]
    sign = 1 if board.current_side == PieceTypes.BLUE else -1

    for move in all_moves:
        move.play(board)
        value = minimax(board, board.current_side == PieceTypes.BLUE) * sign
        is_best_val = value >= best_val

        if is_best_val:
            best_val = value
            best_move = move

        board.undo_move()

    return best_move
