from collections import namedtuple

import numpy as np

from botAI.AlphaBetaPruning import alpha_beta_search

PLAYER_BLACK = 1
PLAYER_WHITE = 2

GameState = namedtuple('GameState', 'to_move, utility, board, moves, branching')


# noinspection PyShadowingNames,DuplicatedCode
class BotGomoku:
    def __init__(self, color, k=5):
        self.my_color = color
        self.opp_color = PLAYER_BLACK if color == PLAYER_WHITE else PLAYER_WHITE
        self.length_victory = k

        self.main_heuristic = True

        self.has_won = False

    def get_color(self):
        return self.my_color

    def set_color(self, color):
        self.my_color = color
        self.opp_color = PLAYER_WHITE if color == PLAYER_BLACK else PLAYER_BLACK

    @staticmethod
    def actions(state):
        """Legal moves are any square not yet taken."""
        return state.moves

    @staticmethod
    def utility(state):
        return state.utility

    @staticmethod
    def terminal_test(state):
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
        moves = self.compute_moves(board)
        player = (PLAYER_BLACK if state.to_move == PLAYER_WHITE else PLAYER_WHITE)
        return GameState(to_move=player,
                         utility=self.compute_utility(board),
                         board=board,
                         moves=moves,
                         branching=state.branching - 1)

    def extract_arrays(self, board):
        transpose_board = np.transpose(board)
        flipped_board = np.flip(board, 1)
        flipped_transposed_board = np.transpose(flipped_board)

        cols = []
        rows = []
        diagonals = []

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

    @staticmethod
    def subarray(array, length_subarray):
        array = np.array(array)
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

    def compare_evaluate_line(self, array):
        my_lines = []
        opp_lines = []
        length_check = 5

        for start in range(0, len(array) - length_check + 1):
            line = []
            count_my_color = 0
            count_opp_color = 0
            valid_line = True

            for end in range(0, length_check):
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
        return self.check_five_in_row(my_lines, self.my_color) * 20 - self.check_five_in_row(opp_lines,
                                                                                             self.opp_color) * 20 + \
               self.check_four_in_row(my_lines, self.my_color) * 5.3 - self.check_four_in_row(opp_lines,
                                                                                              self.opp_color) * 8.7 + \
               self.check_broken_four(my_lines, self.my_color) * 5.2 - self.check_broken_four(opp_lines,
                                                                                              self.opp_color) * 8.3 + \
               self.check_three_in_row(my_lines, self.my_color) * 1.6 - self.check_three_in_row(opp_lines,
                                                                                                self.opp_color) * 3.6 + \
               self.check_broken_three(my_lines, self.my_color) * 1.4 - self.check_broken_three(opp_lines,
                                                                                                self.opp_color) * 2.6 + \
               self.check_two_in_row(my_lines, self.my_color) * 1 - self.check_two_in_row(opp_lines,
                                                                                          self.opp_color) * .5 + \
               self.check_broken_two(my_lines, self.my_color) * 1 - self.check_broken_two(opp_lines,
                                                                                          self.opp_color) * .5

    def main_evaluate_line(self, array):
        my_lines = []
        opp_lines = []
        length_check = 5

        for start in range(0, len(array) - length_check + 1):
            line = []
            count_my_color = 0
            count_opp_color = 0
            valid_line = True

            for end in range(0, length_check):
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

        if len(my_lines) == 0 and len(opp_lines) == 0:
            return 0

        # Offensive at the beginning or when there are no combinations greater than 2-patterns

        # Defensive as far as patterns of 3 and 4 are concerned

        # However, 3-patterns must be generated to put the opponent in difficulty,
        # hence their weight is not too much smaller than 4-patterns... except for defence

        # Broken-pattern are worth less than Row-pattern because, although 3-patterns in rows are counted more times
        # (due to the stride of 1 in the subarray function), they are still very dangerous

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
        return self.check_five_in_row(my_lines, self.my_color) * 40 - self.check_five_in_row(opp_lines,
                                                                                             self.opp_color) * 39 + \
               self.check_four_in_row(my_lines, self.my_color) * 15 - self.check_four_in_row(opp_lines,
                                                                                             self.opp_color) * 20 + \
               self.check_broken_four(my_lines, self.my_color) * 15 - self.check_broken_four(opp_lines,
                                                                                             self.opp_color) * 20 + \
               self.check_three_in_row(my_lines, self.my_color) * 5 - self.check_three_in_row(opp_lines,
                                                                                              self.opp_color) * 8 + \
               self.check_broken_three(my_lines, self.my_color) * 5 - self.check_broken_three(opp_lines,
                                                                                              self.opp_color) * 8 + \
               self.check_two_in_row(my_lines, self.my_color) * 1 - self.check_two_in_row(opp_lines,
                                                                                          self.opp_color) * .5 + \
               self.check_broken_two(my_lines, self.my_color) * 1 - self.check_broken_two(opp_lines,
                                                                                          self.opp_color) * .5

    def compute_utility(self, board):
        arrays = self.extract_arrays(board)
        score = 0
        for array in arrays:
            if self.main_heuristic:
                score += self.main_evaluate_line(array)
            else:
                score += self.compare_evaluate_line(array)
        return score

    def bot_move(self, board):
        if np.count_nonzero(board) == 225:
            return -1, -1

        state = GameState(to_move=self.my_color,
                          utility=0,
                          board=board,
                          moves=self.compute_moves(board),
                          branching=2)
        return alpha_beta_search(self, state)
