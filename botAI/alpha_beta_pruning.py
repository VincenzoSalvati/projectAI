import numpy as np


def alpha_beta_search(game, state):
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state)
        value = -np.inf
        for move in game.actions(state):
            value = max(value, min_value(game.result(state, move), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state)
        value = np.inf
        for move in game.actions(state):
            value = min(value, max_value(game.result(state, move), alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for move in game.actions(state):
        value = min_value(game.result(state, move), best_score, beta)
        if value > best_score:
            best_score = value
            best_action = move
    return best_action
