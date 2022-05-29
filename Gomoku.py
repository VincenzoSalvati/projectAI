import itertools
import sys
import threading
import time
from collections import namedtuple

import numpy as np
import pygame
from pygame import gfxdraw

# Game constants
BOARD_BROWN = (199, 105, 42)
BOARD_WIDTH = 700
BOARD_BORDER = 75
STONE_RADIUS = 14
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURN_POS = (BOARD_BORDER, 20)
SCORE_POS = (BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER + 30)
DOT_RADIUS = 4

PLAYER_BLACK = 1
PLAYER_WHITE = 2

GameState = namedtuple('GameState', 'to_move, utility, board, moves, branching')


# noinspection PyShadowingNames
def alpha_beta_search(game, state):
    player = state.to_move

    # noinspection PyShadowingNames
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        value = -np.inf
        for move in game.actions(state):
            value = max(value, min_value(game.result(state, move), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    # noinspection PyShadowingNames
    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
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


# Graphics
def make_grid(size):
    """Return list of (start_point, end_point pairs) defining gridlines
    Args:
        size (int): size of grid
    Returns:
        Tuple[List[Tuple[float, float]]]: start and end points for gridlines
    """
    start_points, end_points = [], []

    # vertical start points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full(size, BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full(size, BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full(size, BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full(size, BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return start_points, end_points


def col_row_from(x, y, size):
    """Convert x,y coordinates to column and row number
    Args:
        x (float): x position
        y (float): y position
        size (int): size of grid
    Returns:
        Tuple[int, int]: column and row numbers of intersection
    """
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x_dist = x - BOARD_BORDER
    y_dist = y - BOARD_BORDER
    col = int(round(x_dist / inc))
    row = int(round(y_dist / inc))
    return col, row


def x_y_from(col, row, size):
    """Convert column and row numbers to x,y coordinates
    Args:
        col (int): column number (horizontal position)
        row (int): row number (vertical position)
        size (int): size of grid
    Returns:
        Tuple[float, float]: x,y coordinates of intersection
    """
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x = int(BOARD_BORDER + col * inc)
    y = int(BOARD_BORDER + row * inc)
    return x, y


class Gomoku:

    def __init__(self, size, length_victory=5):
        pygame.init()

        self.size = size
        self.length_victory = length_victory
        self.board = np.zeros((size, size))

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.start_points, self.end_points = make_grid(size)
        self.stop_drawing = False
        self.font = pygame.font.SysFont("arial", 30)
        self.WRONG_CLICK = pygame.mixer.Sound("wav/wrong_click.wav")
        self.RIGHT_CLICK = pygame.mixer.Sound("wav/right_click.wav")

        # Where the game is getting involved
        self.x_min = 16
        self.x_max = -1
        self.y_min = 16
        self.y_max = -1

        self.black_turn = True

        moves = [(x, y)
                 for x in range(size)
                 for y in range(size)]

        self.initial = GameState(to_move=(PLAYER_BLACK if self.black_turn else PLAYER_WHITE),
                                 utility=0,
                                 board=self.board,
                                 moves=moves,
                                 branching=3)

    @staticmethod
    def actions(state):
        """Legal moves are any square not yet taken."""
        return state.moves

    @staticmethod
    def utility(state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == PLAYER_BLACK else -state.utility

    @staticmethod
    def terminal_test(state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0 or state.branching == 0

    @staticmethod
    def to_move(state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def pass_move(self):
        self.black_turn = not self.black_turn

    def compute_moves(self, board):

        def filtering(coordinates):
            x, y = coordinates
            padded = np.pad(board, 1)
            if board[x][y] == 0:
                if np.any(padded[x:x + 3, y:y + 3] != 0):
                    return True
            else:
                return False

        return set(filter(filtering, [(x, y)
                                      for x in range(self.size)
                                      for y in range(self.size)]))

    def result(self, state, move):
        if move not in state.moves:
            return state

        board = state.board.copy()
        board[move] = state.to_move
        moves = self.compute_moves(board)

        return GameState(to_move=(PLAYER_BLACK if self.black_turn else PLAYER_WHITE),
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
        for j in range(self.size - self.length_victory + 1):
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
        lines = self.subarray(array, 5)

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
        return (self.check_five_in_row(lines, 1) * 12 - self.check_five_in_row(lines, 2) * 12) + \
               (self.check_four_in_row(lines, 1) * 5.2 - self.check_four_in_row(lines, 2) * 3.2) + \
               (self.check_broken_four(lines, 1) * 5 - self.check_broken_four(lines, 2) * 3.1) + \
               (self.check_three_in_row(lines, 1) * 2.15 - self.check_three_in_row(lines, 2) * 0.95) + \
               (self.check_broken_three(lines, 1) * 1.55 - self.check_broken_three(lines, 2) * 0.85) + \
               (self.check_two_in_row(lines, 1) * 0.02 - self.check_two_in_row(lines, 2) * 0.2) + \
               (self.check_broken_two(lines, 1) * 0.02 - self.check_broken_two(lines, 2) * 0.2) + \
               (self.check_one(lines, 1) * 0.001 - self.check_one(lines, 2) * 0.01)

    def compute_utility(self, board):
        arrays = self.extract_arrays(board)
        score = 0
        for array in arrays:
            score += self.evaluate_line(array)
        return score

    def update_game_range(self, x, y):
        if self.x_min > x:
            self.x_min = x
        if self.x_max < x:
            self.x_max = x
        if self.y_min > y:
            self.y_min = y
        if self.y_max < y:
            self.y_max = y

    def end(self, player, move):
        x, y = move
        x = x + 5
        y = y + 5

        padded = np.pad(self.board, 5)

        clipped_row = padded[x - 5:x + 6, y]
        clipped_col = padded[x, y - 5:y + 6]
        clipped_diagonals = np.diag(padded[x - 5:x + 6, y - 5:y + 6])
        clipped_flipped_diagonals = np.diag(np.flip(padded[x - 5:x + 6, y - 5:y + 6], 1))

        count_stones = 0
        for clip in [clipped_row, clipped_col, clipped_diagonals, clipped_flipped_diagonals]:
            for element in clip:
                if element == player:
                    count_stones += 1
                elif count_stones == 5:
                    break
                else:
                    count_stones = 0
            if count_stones == 5:
                self.win()
            else:
                count_stones = 0

    def win(self):
        # TODO: Win
        time.sleep(5)
        self.stop_drawing = True
        pygame.quit()
        sys.exit()

    def bot_move(self):
        state = GameState(to_move=(PLAYER_BLACK if self.black_turn else PLAYER_WHITE),
                          utility=0,
                          board=self.board,
                          moves=self.compute_moves(self.board),
                          branching=4)
        col_bot, row_bot = alpha_beta_search(game, state)

        # range game coordinates
        self.update_game_range(col_bot, row_bot)

        # draw stone, play sound, check end and pass move
        self.board[col_bot, row_bot] = PLAYER_WHITE
        self.RIGHT_CLICK.play()
        self.end(PLAYER_WHITE, (col_bot, row_bot))
        self.pass_move()

    def is_valid_move(self, col, row):
        if col < 0 or col >= self.size:
            return False
        if row < 0 or row >= self.size:
            return False
        return self.board[col, row] == 0

    def handle_click(self):
        # get board position
        x, y = pygame.mouse.get_pos()
        col, row = col_row_from(x, y, self.size)
        if not self.is_valid_move(col, row):
            self.WRONG_CLICK.play()
            return

        # range game coordinates
        self.update_game_range(col, row)

        # draw stone, play sound, check end and pass move
        self.board[col, row] = PLAYER_BLACK
        self.RIGHT_CLICK.play()
        self.end(PLAYER_BLACK, (col, row))
        self.pass_move()
        self.bot_move()

    def display(self, state):
        board = state.board
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def clear_screen(self):
        # fill board and add gridlines
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # add guide dots
        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        pygame.display.flip()

    def draw(self):
        self.clear_screen()

        for col, row in zip(*np.where(self.board == 1)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, WHITE)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, WHITE)

        turn_msg = (
                f"{'Black' if self.black_turn else 'White'} to move. "
                + "Click to place stone, press P to pass."
        )
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        pygame.display.flip()

    def update(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.stop_drawing = True
                pygame.quit()
                sys.exit()

        if len(events) > 0:
            if events[0].type == pygame.MOUSEBUTTONUP and self.black_turn:
                self.handle_click()
            if events[0].type == pygame.KEYUP and self.black_turn:
                if events[0].key == pygame.K_p:
                    self.pass_move()
                    self.bot_move()

        pygame.event.clear()


def update_screen():
    while True:
        game.draw()
        time.sleep(0.5)
        if game.stop_drawing:
            break


if __name__ == "__main__":
    game = Gomoku(15)
    thread_draw = threading.Thread(target=update_screen, args=())
    thread_draw.start()
    while True:
        game.update()
        pygame.time.wait(100)
