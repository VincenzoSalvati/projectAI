"""
Course: Agenti Intelligenti 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file BotGomoku.py


PURPOSE OF THE FILE: bot intelligence.
"""

from collections import namedtuple

import numpy as np

from bot.alpha_beta_pruning import alpha_beta_search
from bot.constants_ai import *
from bot.patterns import check_five_in_row, check_four_in_row, check_broken_four, check_three_in_row, \
    check_broken_three, check_two_in_row, check_broken_two
from utility.Chronometer import Chronometer

GameState = namedtuple('GameState', 'player, utility, board, moves, branching')


class BotGomoku:
    """Object BotGomoku

    Attributes:
        stone_player (int): player's stone
        stone_opponent (int): opponent's stone
        length_victory (int): number of consecutively stones necessary to win

        main_heuristic (bool): bot use main heuristic
        has_won (bool): bot has won

        chronometer (Chronometer): take the elapsed time of the match
    """

    def __init__(self, stone_player, weights=BOT_WEIGHTS_MAIN):
        """Init bot

        Args:
            stone_player (int): player's stone
            weights (dict[str, Tuple[String,Tuple[int, int]]]): heuristic's weight
        """
        # Init attributes
        self.stone_player = stone_player
        self.stone_opponent = PLAYER_BLACK if stone_player == PLAYER_WHITE else PLAYER_WHITE
        self.length_victory = LENGTH_VICTORY

        self.main_heuristic = True  # For CSV print
        self.has_won = False

        self.weights = weights
        self.chronometer = Chronometer()

    def get_stone_player(self):
        """Return player's stone

        Returns:
            int: player's stone
        """
        return self.stone_player

    @staticmethod
    def utility(state):
        """Return the utility score of a particular state

        Returns:
            int: the utility score of a particular state
        """
        return state.utility

    @staticmethod
    def actions(state):
        """Return list of legal moves are any square not yet taken

        Returns:
            List[Tuple[int, int]]: list of legal moves are any square not yet taken
        """
        return state.moves

    def terminal_test(self, state):
        """Returns if it is achieved the end of the depth search

        Returns:
            bool: is achieved the end of the depth search
        """
        return len(state.moves) == 0 or \
               state.branching == 0 or \
               state.utility >= self.weights["FiveInRow"][0] * WEIGHT_TERMINAL_STATE

    @staticmethod
    def player(state):
        """Return the player of a particular state

        Returns:
            int: player of a particular state
        """
        return state.player

    @staticmethod
    def search_useful_moves(board):
        """Return list of useful moves which can be taken into account by the bot

        Args:
            board (numpy.array[int, int]): representative matrix of Gomoku board

        Return:
            List[Tuple[int, int]]: list of useful moves which can be taken into account by the bot
        """

        def filtering(coordinates, neighbourhood=3):
            x, y = coordinates
            padding = (neighbourhood - 1) // 2
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
        """Return new state of the game after a move

        Args:
            state (GameState): old state
            move (Tuple[int, int]): chosen move by specific player

        Return:
            GameState: new state of the game after a move
        """
        # Check move
        if move not in state.moves:
            return state

        # Perform move
        board = state.board.copy()
        board[move] = state.player

        # Set new state
        player = (PLAYER_BLACK if state.player == PLAYER_WHITE else PLAYER_WHITE)
        utility = self.compute_utility(board)
        moves = self.search_useful_moves(board)
        branching = state.branching - 1
        return GameState(player=player,
                         utility=utility,
                         board=board,
                         moves=moves,
                         branching=branching)

    def masking_array(self, array):
        """Return masked array in order to avoid considering over 5 stones consecutively

        Args:
            array (array[int]): array to be masked

        Return:
            array[int]: masked array
        """
        # Init parameters
        array = np.array(array)
        array_next_different = np.r_[True, array[:-1] != array[1:], True]
        occurrences = np.diff(np.flatnonzero(array_next_different))
        values_occurrences = array[array_next_different[:-1]]
        indexes_occurrences = np.cumsum(occurrences)

        # Masking internal holes
        for i in range(len(values_occurrences) - 2):
            if occurrences[i + 1] == 1:
                if (values_occurrences[i] == self.stone_player and
                    values_occurrences[i + 1] == 0 and
                    values_occurrences[i + 2] == self.stone_player) \
                        or \
                        (values_occurrences[i] == self.stone_opponent and
                         values_occurrences[i + 1] == 0 and
                         values_occurrences[i + 2] == self.stone_opponent):
                    if sum(occurrences[i:i + 3]) >= 6:
                        array[indexes_occurrences[i]] = MASKING_ELEMENT

        # Masking SIX Combinations
        indexes = list(np.where(occurrences >= 6)[0])
        for i in indexes:
            if values_occurrences[i] != 0:
                start = indexes_occurrences[i - 1]
                stop = indexes_occurrences[i]
                array[start:stop + 1] = MASKING_ELEMENT
                try:
                    if array[stop + 1] == 0:
                        array[stop + 1] = MASKING_ELEMENT
                except IndexError:
                    pass
                try:
                    if array[start - 1] == 0:
                        array[start - 1] = MASKING_ELEMENT
                except IndexError:
                    pass
        return array

    # noinspection DuplicatedCode
    def array_analysis(self, array):
        """Return extracted lines (stride of 1) and how many six in row has been found into an array

        Args:
            array (array[int]): array to be analyzed

        Return:
            List[List[array[int], array[int], int, int]]: extracted lines and how many six in row has been found
        """
        # Init parameters
        array = self.masking_array(array)
        my_lines = []
        opp_lines = []

        for start_index in range(0, len(array) - self.length_victory + 1):  # stride 1 until to (length - 5)
            line = []
            count_my_color = 0
            count_opp_color = 0

            valid_line = True
            for end_index in range(0, self.length_victory):  # check next 5 starting from start_index

                # My color
                if array[start_index + end_index] == self.stone_player:
                    if count_opp_color != 0:
                        valid_line = False
                        break
                    else:
                        count_my_color += 1
                        line.append(array[start_index + end_index])

                # Opponent color
                elif array[start_index + end_index] == self.stone_opponent:
                    if count_my_color != 0:
                        valid_line = False
                        break
                    else:
                        count_opp_color += 1
                        line.append(array[start_index + end_index])

                # My color and opponent color
                else:
                    if array[start_index + end_index] == 0:
                        line.append(0)
                    else:  # array[start_index + end_index] == MASKING_ELEMENT
                        valid_line = False
                        break

            if valid_line:
                if count_my_color >= 2:
                    my_lines.append(line)
                elif count_opp_color >= 2:
                    opp_lines.append(line)

        return my_lines, opp_lines

    def evaluate_line(self, array, weights):
        """Return array's score

        Args:
            array (array[int]): array to be analyzed
            weights (Dict[String, Tuple[int, int]]): dictionary of weights

        Returns:
            int: array's score
        """
        # Init parameters
        functions = [check_five_in_row,
                     check_four_in_row, check_broken_four,
                     check_three_in_row, check_broken_three,
                     check_two_in_row, check_broken_two]

        # Extract lines
        my_lines, opp_lines = self.array_analysis(array)

        # Perform score
        score = 0
        for function, value in zip(functions, weights.values()):
            score += function(my_lines, self.stone_player) * value[0] - \
                     function(opp_lines, self.stone_opponent) * value[1]

        return score

    def extract_lists_of_stones_from(self, board):
        """Return lists of stones extracted from a board

        Args:
            board (numpy.array[int, int]): representative matrix of Gomoku board

        Returns:
            List[List[int]]: lists of stones extracted from a board
        """
        # Init parameters
        cols = []
        rows = []
        diagonals = []

        transpose_board = np.transpose(board)
        flipped_board = np.flip(board, 1)
        flipped_transposed_board = np.transpose(flipped_board)

        # Extract lists of stones
        for c in range(0, board.shape[0]):
            col = []
            row = []

            # Cols and rows
            for r in range(0, board.shape[1]):
                row.append(board[c][r])
                col.append(board[r][c])
            cols.append(np.array(col))
            rows.append(np.array(row))

            # Diagonals
            if c < board.shape[0] - self.length_victory + 1:
                diagonals.append(np.diag(board[0:, c:]))
                diagonals.append(np.diag(flipped_board[0:, c:]))
                if c != 0:
                    diagonals.append(np.diag(transpose_board[0:, c:]))
                    diagonals.append(np.diag(flipped_transposed_board[0:, c:]))

        return [*rows, *cols, *diagonals]

    def compute_utility(self, board):
        """Return utility score of a specific board

        Args:
            board (numpy.array[int, int]): representative matrix of Gomoku board

        Returns:
            int: utility score of a specific board
        """
        # Init parameters
        score = 0

        # Extract lists of stones
        lists_of_stones = self.extract_lists_of_stones_from(board)

        # Perform utility score
        for list_of_stones in lists_of_stones:
            score += self.evaluate_line(list_of_stones, self.weights)

        return score

    def bot_search_move(self, board, branching=2):
        """Return bot player's move

        Args:
            board (numpy.array[int, int]): representative matrix of Gomoku board
            branching (int): number of level under a specific state

        Returns:
            Tuple[int, int]: bot player's move
        """
        # No moves --> tie
        if np.count_nonzero(board) == 225:
            return -1, -1

        # Set new state
        player = self.get_stone_player()
        utility = 0
        moves = self.search_useful_moves(board)
        state = GameState(player=player,
                          utility=utility,
                          board=board,
                          moves=moves,
                          branching=branching)

        # Search move to return
        return alpha_beta_search(self, state)
