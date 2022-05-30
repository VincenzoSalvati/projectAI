import random
from collections import namedtuple

import numpy as np

from gomoku.AlphaBetaPruning import alpha_beta_search

GameState = namedtuple('GameState', 'to_move, utility, board, moves, branching')

PLAYER_BLACK = 1
PLAYER_WHITE = 2


# noinspection PyShadowingNames
class BotGomoku:
    def __init__(self, color, k=5):
        self.myColor = color
        self.opponent = PLAYER_BLACK if color == PLAYER_WHITE else PLAYER_WHITE
        self.length_victory = k

    def get_color(self):
        return self.myColor

    @staticmethod
    def actions(state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == self.opponent else -state.utility

    @staticmethod
    def terminal_test(state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0 or state.branching == 0

    @staticmethod
    def to_move(state):
        """Return the player whose move it is in this state."""
        return state.to_move

    @staticmethod
    def compute_moves(board):

        def filtering(coordinates):
            x, y = coordinates
            padded = np.pad(board, 1)
            if board[x][y] == 0:
                if np.any(padded[x:x + 3, y:y + 3] != 0):
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
        moves = self.compute_moves(board)

        return GameState(to_move=(PLAYER_BLACK if state.to_move == PLAYER_WHITE else PLAYER_WHITE),
                         utility=self.compute_utility(board),
                         board=board,
                         moves=moves,
                         branching=state.branching - 1)

    def extract_arrays(self, board):
        transpose_board = np.transpose(board)
        flipped_board = np.flip(board, 1)
        flipped_transposed_board = np.transpose(flipped_board)

        rows = [board[_, :] for _ in range(board.shape[0])]
        cols = [board[:, _] for _ in range(board.shape[1])]
        diagonals = []
        for j in range(len(board) - self.length_victory + 1):
            diagonals.append(np.diag(board[0:, j:]))
            diagonals.append(np.diag(flipped_board[0:, j:]))
            if j != 0:
                diagonals.append(np.diag(transpose_board[0:, j:]))
                diagonals.append(np.diag(flipped_transposed_board[0:, j:]))

        return [*rows, *cols, *diagonals]

    @staticmethod
    def subarray(array, length_subarray):
        return [*np.fromfunction(lambda i, j: array[i + j], (len(array) - length_subarray + 1, length_subarray),
                                 dtype=int)]

    @staticmethod
    def check_five_in_row(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, player, player, player, player]):
                count += 1
        return count

    @staticmethod
    def check_four_in_row(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [0, player, player, player, player]) or \
                    np.all(line == [player, player, player, player, 0]):
                count += 1
        return count

    @staticmethod
    def check_broken_four(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, 0, player, player, player]) or \
                    np.all(line == [player, player, 0, player, player]) or \
                    np.all(line == [player, player, player, 0, player]):
                count += 1
        return count

    @staticmethod
    def check_three_in_row(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, player, player, 0, 0]) or \
                    np.all(line == [0, player, player, player, 0]) or \
                    np.all(line == [0, 0, player, player, player]):
                count += 1
        return count

    @staticmethod
    def check_broken_three(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, 0, player, player, 0]) or \
                    np.all(line == [player, 0, 0, player, player]) or \
                    np.all(line == [0, player, 0, player, player]) or \
                    np.all(line == [player, player, 0, 0, player]) or \
                    np.all(line == [player, player, 0, player, 0]) or \
                    np.all(line == [0, player, player, 0, player]):
                count += 1
        return count

    @staticmethod
    def check_two_in_row(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, player, 0, 0, 0]) or \
                    np.all(line == [0, player, player, 0, 0]) or \
                    np.all(line == [0, 0, player, player, 0]) or \
                    np.all(line == [0, 0, 0, player, player]):
                count += 1
        return count

    @staticmethod
    def check_broken_two(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, 0, player, 0, 0]) or \
                    np.all(line == [player, 0, 0, player, 0]) or \
                    np.all(line == [player, 0, 0, 0, player]) or \
                    np.all(line == [0, player, 0, player, 0]) or \
                    np.all(line == [0, player, 0, 0, player]) or \
                    np.all(line == [0, 0, player, 0, player]):
                count += 1
        return count

    @staticmethod
    def check_one(lines, player):
        count = 0
        for line in lines:
            if np.all(line == [player, 0, 0, 0, 0]) or \
                    np.all(line == [0, player, 0, 0, 0]) or \
                    np.all(line == [0, 0, player, 0, 0]) or \
                    np.all(line == [0, 0, 0, player, 0]) or \
                    np.all(line == [0, 0, 0, 0, player]):
                count += 1
        return count

    def evaluate_line(self, array):
        lines = np.array(self.subarray(array, 5))

        my_lines = lines[np.count_nonzero(lines == self.myColor, axis=1) >= 1]
        opp_lines = lines[np.count_nonzero(lines == self.opponent, axis=1) >= 1]

        if len(my_lines) == 0 and len(opp_lines) == 0:
            return 0

        # Offensive at the beginning or when there are no combinations greater than 2-patterns

        # Defensive as far as patterns of 3 and 4 are concerned.
        # However, 3-patterns must be generated to put the opponent in difficulty,
        # hence their weight is not too much smaller than 4-patterns... except for defence

        # Broken-pattern are worth less than Row-pattern because you can win with just one move and, in addition to
        # that, such patterns are easily spotted on a chessboard

        # Victory must be both taken (for itself) and avoided (for the opponent) and must be worth much more than
        # other combinations

        # Weaknesses:
        # 1.Does not pay attention to sequences longer than 5 stones (both for himself and for the opponent)
        # 2.Does not elaborate complicated strategies on purpose (e.g. special patterns)

        # Strengths:
        # 1.He is alarmed in situations of at least 5 consecutive stones (both for himself and for the opponent)
        # 2.A high value of 3-patterns and 4-patterns gives more chances to generate advantageous situations for
        # itself, but, at the same time, it prefers blocking the generation of such situations
        # by the opponent (even if only slightly)
        # 3. It continues his attack strategy without being fooled by single opposing stones located far from
        # the masses
        # noinspection PyPep8
        return self.check_five_in_row(opp_lines, self.opponent) * 12 - self.check_five_in_row(my_lines,
                                                                                              self.myColor) * 12 + \
               self.check_four_in_row(opp_lines, self.opponent) * 5.2 - self.check_four_in_row(my_lines,
                                                                                               self.myColor) * 3.2 + \
               self.check_broken_four(opp_lines, self.opponent) * 5.2 - self.check_broken_four(my_lines,
                                                                                               self.myColor) * 3.2 + \
               self.check_three_in_row(opp_lines, self.opponent) * 2.15 - self.check_three_in_row(my_lines,
                                                                                                  self.myColor) * .95 + \
               self.check_broken_three(opp_lines, self.opponent) * 1.55 - self.check_broken_three(my_lines,
                                                                                                  self.myColor) * .85 + \
               self.check_two_in_row(lines, self.opponent) * .02 - self.check_two_in_row(lines, self.myColor) * .2 + \
               self.check_broken_two(lines, self.opponent) * .02 - self.check_broken_two(lines, self.myColor) * .2 + \
               self.check_one(lines, self.opponent) * .01 - self.check_one(lines, self.myColor) * .01

    def compute_utility(self, board):
        arrays = self.extract_arrays(board)
        score = 0
        for array in arrays:
            score += self.evaluate_line(array)
        return score

    def bot_move(self, board):
        state = GameState(to_move=self.myColor,
                          utility=0,
                          board=board,
                          moves=self.compute_moves(board),
                          branching=3)
        return alpha_beta_search(self, state)
