from collections import namedtuple

import numpy as np

from botAI.AI_constants import BOT_WEIGHTS, BOT_WEIGHTS2
from botAI.alpha_beta_pruning import alpha_beta_search

from utility.ChronoMeter import ChronoMeter
from utility.patterns import check_five_in_row, check_four_in_row, check_broken_four, check_three_in_row, \
    check_broken_three, check_two_in_row, check_broken_two
from utility.utils import extract_subarrays

PLAYER_BLACK = 1
PLAYER_WHITE = 2

GameState = namedtuple('GameState', 'to_move, utility, board, moves, branching')


class BotGomoku:
    def __init__(self, color, k=5):
        self.my_color = color
        self.opp_color = PLAYER_BLACK if color == PLAYER_WHITE else PLAYER_WHITE
        self.length_victory = k

        self.main_heuristic = True
        self.has_won = False

        self.chronometer = ChronoMeter()
        self.weights = BOT_WEIGHTS

    def get_color(self):
        return self.my_color

    @staticmethod
    def actions(state):
        """Legal moves are any square not yet taken."""
        return state.moves

    @staticmethod
    def utility(state):
        """Return the score utility of a particular state."""
        return state.utility

    @staticmethod
    def terminal_test(state):
        """Returns the Boolean to verify the end of the depth search."""
        return len(state.moves) == 0 or state.branching == 0

    @staticmethod
    def to_move(state):
        """Return the player whose move it is in this state."""
        return state.to_move

    @staticmethod
    def compute_moves(board):
        def filtering(coordinates, neighbourhood=3):
            x, y = coordinates
            padding = (neighbourhood-1)//2
            padded_board = np.pad(board, padding)
            if board[x][y] == 0:
                if np.any(padded_board[x:x + neighbourhood, y:y + neighbourhood] != 0):
                    return True
            else:
                return False

        return set(filter(filtering, [(x, y)
                                      for x in range(board.shape[0])
                                      for y in range(board.shape[1])]))

    def result(self, state, move):
        if move not in state.moves:
            return state

        board = state.board.copy()
        board[move] = state.to_move

        player = (PLAYER_BLACK if state.to_move == PLAYER_WHITE else PLAYER_WHITE)
        utility = self.compute_utility(board)
        moves = self.compute_moves(board)
        branching = state.branching - 1
        return GameState(to_move=player,
                         utility=utility,
                         board=board,
                         moves=moves,
                         branching=branching)

    def evaluate_line(self, array, weights):
        lines = extract_subarrays(array, 5)
        my_lines = lines[np.count_nonzero(lines == self.my_color, axis=1) >= 2]
        opp_lines = lines[np.count_nonzero(lines == self.opp_color, axis=1) >= 2]

        if len(my_lines) == 0 and len(opp_lines) == 0:
            return 0

        # Six Lines Check
        six_lines = extract_subarrays(array, 6)
        if len(six_lines) > 0:
            num_six_lines_my_color = np.count_nonzero(np.count_nonzero(six_lines == self.my_color, axis=1) == 6)
            num_six_lines_opp_color = np.count_nonzero(np.count_nonzero(six_lines == self.opp_color, axis=1) == 6)
            num_six_lines_my_color = num_six_lines_my_color if num_six_lines_my_color > 0 else -1
            num_six_lines_opp_color = num_six_lines_opp_color if num_six_lines_opp_color > 0 else -1
        else:
            num_six_lines_my_color = -1
            num_six_lines_opp_color = -1

        score = num_six_lines_my_color * (-weights["FiveInRow"][0] * (num_six_lines_my_color + 1)) - num_six_lines_opp_color * (
                -weights["FiveInRow"][1] * (num_six_lines_opp_color + 1))

        functions = [check_five_in_row, check_four_in_row, check_broken_four, check_three_in_row, check_broken_three,
                     check_two_in_row, check_broken_two]

        for fun, val in zip(functions, weights.values()):
            score += fun(my_lines, self.my_color) * val[0] - fun(opp_lines, self.opp_color) * val[1]

        return score

    def extract_arrays(self, board):
        cols = []
        rows = []
        diagonals = []

        transpose_board = np.transpose(board)
        flipped_board = np.flip(board, 1)
        flipped_transposed_board = np.transpose(flipped_board)
        for c in range(0, board.shape[0]):
            col = []
            row = []
            for r in range(0, board.shape[1]):
                row.append(board[c][r])
                col.append(board[r][c])
            cols.append(col)
            rows.append(row)
            if c < board.shape[0] - self.length_victory + 1:
                diagonals.append(np.diag(board[0:, c:]))
                diagonals.append(np.diag(flipped_board[0:, c:]))
                if c != 0:
                    diagonals.append(np.diag(transpose_board[0:, c:]))
                    diagonals.append(np.diag(flipped_transposed_board[0:, c:]))

        return [*rows, *cols, *diagonals]

    def compute_utility(self, board):
        arrays = self.extract_arrays(board)
        score = 0

        for array in arrays:
            if self.main_heuristic:
                score += self.evaluate_line(array, BOT_WEIGHTS)
            else:
                score += self.evaluate_line(array, BOT_WEIGHTS2)

        return score

    def bot_search_move(self, board, branching=2):
        if np.count_nonzero(board) == 225:
            return -1, -1

        moves = self.compute_moves(board)
        state = GameState(to_move=self.my_color,
                          utility=0,
                          board=board,
                          moves=moves,
                          branching=branching)

        return alpha_beta_search(self, state)
