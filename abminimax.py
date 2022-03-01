from board import *

def ab_minimax(board: Board, depth: int, alpha: int, beta: int, MAXIMIZING: bool):
    if depth == 0 or board.game_over():
        return board.evaluate() , board
    next_states = board.get_next_states()
    if next_states == []:
        return 0, board
    best_state = None
    if MAXIMIZING:
        value = -math.inf
        for next_state in next_states:
            MAX = ab_minimax(next_state, depth - 1, alpha, beta, False)[0]
            if MAX >= value:
                value = MAX
                best_state = next_state
            if value >= beta:
                break # beta cutoff
            alpha = max(alpha, value)
    else:
        value = math.inf
        for next_state in next_states:
            MIN = ab_minimax(next_state, depth - 1, alpha, beta, True)[0]
            if MIN <= value:
                value = MIN
                best_state = next_state
            if value <= alpha: # alpha cutoff
                break # beta cutoff
            beta = min(beta, value)
    return value,best_state


