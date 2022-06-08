from collections import namedtuple

import numpy as np

from botAI.AlphaBetaPruning import alpha_beta_search
from utility.Patterns import check_five_in_row, check_four_in_row, check_broken_four, check_three_in_row, \
    check_broken_three, check_two_in_row, check_broken_two

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
        def filtering(coordinates):
            x, y = coordinates
            padded_board = np.pad(board, 1)
            if board[x][y] == 0:
                if np.any(padded_board[x:x + 3, y:y + 3] != 0):
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

    def extract_lines(self, array):
        my_lines = []
        opp_lines = []

        for start in range(0, len(array) - self.length_victory + 1):
            line = []
            count_my_color = 0
            count_opp_color = 0
            valid_line = True
            for end in range(0, self.length_victory):
                if array[start + end] == self.my_color:
                    if count_opp_color != 0:
                        valid_line = False
                        break
                    else:
                        count_my_color += 1
                        line.append(array[start + end])

                elif array[start + end] == self.opp_color:
                    if count_my_color != 0:
                        valid_line = False
                        break
                    else:
                        count_opp_color += 1
                        line.append(array[start + end])
                else:
                    line.append(0)
            if valid_line:
                if count_my_color > 1:
                    my_lines.append(line)
                elif count_opp_color > 1:
                    opp_lines.append(line)

        return my_lines, opp_lines

    def compare_evaluate_line(self, array):
        my_lines, opp_lines = self.extract_lines(array)
        if len(my_lines) == 0 and len(opp_lines) == 0:
            return 0

        return check_five_in_row(my_lines, self.my_color) * 20 - check_five_in_row(opp_lines, self.opp_color) * 20 + \
               check_four_in_row(my_lines, self.my_color) * 5.3 - check_four_in_row(opp_lines, self.opp_color) * 8.7 + \
               check_broken_four(my_lines, self.my_color) * 5.2 - check_broken_four(opp_lines, self.opp_color) * 8.3 + \
               check_three_in_row(my_lines, self.my_color) * 1.6 - check_three_in_row(opp_lines, self.opp_color) * 3.6 + \
               check_broken_three(my_lines, self.my_color) * 1.4 - check_broken_three(opp_lines, self.opp_color) * 2.6 + \
               check_two_in_row(my_lines, self.my_color) * 1 - check_two_in_row(opp_lines, self.opp_color) * .5 + \
               check_broken_two(my_lines, self.my_color) * 1 - check_broken_two(opp_lines, self.opp_color) * .5

    def main_evaluate_line(self, array):
        my_lines, opp_lines = self.extract_lines(array)
        if len(my_lines) == 0 and len(opp_lines) == 0:
            return 0

        return check_five_in_row(my_lines, self.my_color) * 10000 - check_five_in_row(opp_lines,
                                                                                      self.opp_color) * 9999 + \
               check_four_in_row(my_lines, self.my_color) * 105 - check_four_in_row(opp_lines, self.opp_color) * 100 + \
               check_broken_four(my_lines, self.my_color) * 105 - check_broken_four(opp_lines, self.opp_color) * 100 + \
               check_three_in_row(my_lines, self.my_color) * 5 - check_three_in_row(opp_lines, self.opp_color) * 10 + \
               check_broken_three(my_lines, self.my_color) * 5 - check_broken_three(opp_lines, self.opp_color) * 10 + \
               check_two_in_row(my_lines, self.my_color) * 1 - check_two_in_row(opp_lines, self.opp_color) * .5 + \
               check_broken_two(my_lines, self.my_color) * 1 - check_broken_two(opp_lines, self.opp_color) * .5

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
                score += self.main_evaluate_line(array)
            else:
                score += self.compare_evaluate_line(array)

        return score

    def bot_move(self, board, branching=2):
        if np.count_nonzero(board) == 225:
            return -1, -1

        moves = self.compute_moves(board)
        state = GameState(to_move=self.my_color,
                          utility=0,
                          board=board,
                          moves=moves,
                          branching=branching)

        return alpha_beta_search(self, state)
