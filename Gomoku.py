import copy

from TickTacToe.games import *

import random
import pygame
import numpy as np
import itertools
import sys
import networkx as nx
from pygame import gfxdraw

# Game constants
BOARD_BROWN = (199, 105, 42)
BOARD_WIDTH = 700
BOARD_BORDER = 75
STONE_RADIUS = 22
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURN_POS = (BOARD_BORDER, 20)
SCORE_POS = (BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER + 30)
DOT_RADIUS = 4

PLAYER_BLACK = 1
PLAYER_WHITE = 2


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
    ys = np.full((size), BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full((size), BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full((size), BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return (start_points, end_points)


def xy_to_colrow(x, y, size):
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


def colrow_to_xy(col, row, size):
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


def has_no_liberties(board, group):
    """Check if a stone group has any liberties on a given board.
    Args:
        board (object): game board (size * size matrix)
        group (List[Tuple[int, int]]): list of (col,row) pairs defining a stone group
    Returns:
        [boolean]: True if group has any liberties, False otherwise
    """
    for x, y in group:
        if x > 0 and board[x - 1, y] == 0:
            return False
        if y > 0 and board[x, y - 1] == 0:
            return False
        if x < board.shape[0] - 1 and board[x + 1, y] == 0:
            return False
        if y < board.shape[0] - 1 and board[x, y + 1] == 0:
            return False
    return True


def get_stone_groups(board, color):
    """Get stone groups of a given color on a given board
    Args:
        board (object): game board (size * size matrix)
        color (str): name of color to get groups for
    Returns:
        List[List[Tuple[int, int]]]: list of list of (col, row) pairs, each defining a group
    """
    size = board.shape[0]
    color_code = 1 if color == "black" else 2
    xs, ys = np.where(board == color_code)
    graph = nx.grid_graph(dim=[size, size])
    stones = set(zip(xs, ys))
    all_spaces = set(itertools.product(range(size), range(size)))
    stones_to_remove = all_spaces - stones
    graph.remove_nodes_from(stones_to_remove)
    return nx.connected_components(graph)


def is_valid_move(col, row, board):
    """Check if placing a stone at (col, row) is valid on board
    Args:
        col (int): column number
        row (int): row number
        board (object): board grid (size * size matrix)
    Returns:
        boolean: True if move is valid, False otherewise
    """
    # TODO: check for ko situation (infinite back and forth)
    if col < 0 or col >= board.shape[0]:
        return False
    if row < 0 or row >= board.shape[0]:
        return False
    return board[col, row] == 0


class Gomoku:
    def __init__(self, size, k=5):

        self.k = k
        moves = [(x, y) for x in range(1, size + 1)
                 for y in range(1, size + 1)]

        self.board = np.zeros((size, size))
        self.size = size
        self.black_turn = True
        self.start_points, self.end_points = make_grid(self.size)

        self.initial = GameState(to_move=PLAYER_BLACK, utility=0, board=self.board, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=(PLAYER_WHITE if state.to_move == PLAYER_BLACK else PLAYER_BLACK),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board,
                         moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == PLAYER_BLACK else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def extract_matrix(self, board, move):
        x, y = move
        list = []

        start_row = x - 5 if x - 5 >= 0 else 0
        start_col = y - 5 if y - 5 >= 0 else 0

        end_row = x + 5 if x + 5 <= self.size else self.size
        end_col = y + 5 if y + 5 <= self.size else self.size

        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                list.append(board[i:i + 5, j:j + 5])

        return list

    def extract_arrays(self, board, move):

        x, y = move
        list = []

        start_row = x - 5 if x - 5 >= 0 else 0
        start_col = y - 5 if y - 5 >= 0 else 0

        end_row = x + 5 if x + 5 <= self.size else self.size
        end_col = y + 5 if y + 5 <= self.size else self.size


        spazi_prima_colonne = 5 if y-5 >=0 else y
        spazi_dopo_colonne = 5 if y+5 <= self.size else self.size-y


        if spazi_prima_colonne == spazi_dopo_colonne == 5:
            for i in range(6):
                # Horizontal
                list.append(board[x, y - i:y + 5 - i])
        elif spazi_prima_colonne != 5:
            for i in range(spazi_prima_colonne):
                list.append(board[x, y - i:y + 5 - i])
        else:
            for i in range(spazi_dopo_colonne):
                list.append(board[x, y - 5 + i: y + i])
        #
        # transpose_board = np.transpose(board)
        # for i in range(spazi_prima_colonne):
        #     # Horizontal
        #     list.append(board[x, y-i:y+5-i])

        # for i in range(end_row - start_row):
        #     # Vertical
        #     list.append(board[start_row + i:end_row - i, y])
        #
        # for i in range(min(end_col - start_col, end_row - start_row)):
        #     # Diag1
        #     list.append(np.diag(board[start_row + i:end_row - i, start_col + i:end_col - i]))
        #     # Diag2
        #     list.append(np.diag(transpose_board[start_row + i:end_row - i, start_col + i:end_col - i]))

        return list

    def generation_pattern(self):
        list = []
        for i in range(5):
            matrix = []
            for ii in range(i):
                matrix.append("-")
            for j in range(5 - i):
                matrix.append("x")
            list.append(matrix)

        for i in range(5):
            matrix = copy.copy(list[0])
            matrix[i] = "-"
            list.append(matrix)

        list.remove(list[0])
        list.remove(list[0])

        for i in range(3):
            matrix = copy.copy(list[i])
            matrix = matrix.reverse()
            list.append(list(matrix))

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        matrices = self.extract_matrix(board, move)
        arrays = self.extract_arrays(board, move)
        print("CIAO")

    def check_endgame(self, board, move, player):
        x, y = move  # coordinates of the last added stone
        row_start = x - 5 if x - 5 > 0 else 0
        col_start = y - 5 if y - 5 > 0 else 0
        # Horizontal
        count_stones = 0
        for k in range(2 * 5 - 1):
            if board[x][y + k] == player:
                count_stones += 1
            else:
                count_stones = 0

    def k_in_row(self, board, move, player, delta_x_y):
        # Check ends of game
        count_r = count_c = count_d1 = count_d2 = 0
        for i in range(self.size):
            for j in range(self.size):

                # Orizzontale
                if board[i][j] == player:
                    count_r += 1
                    if count_r == 5:
                        self.win()
                else:
                    count_r = 0

                # Verticale
                if board[j][i] == player:
                    count_c += 1
                    if count_c == 5:
                        self.win()
                else:
                    count_c = 0

                # Diagonale 1
                if i + 5 < self.size and j + 5 < self.size:
                    for k in range(5):
                        if board[i + k][j + k] == player:
                            count_d1 += 1
                        else:
                            count_d1 = 0
                            break

                    if count_d1 == 5:
                        self.win()

                if i + 5 < self.size and j - 5 < self.size:
                    for k in range(5):
                        if board[i + k][j - k] == player:
                            count_d2 += 1
                        else:
                            count_d2 = 0
                            break

                    if count_d2 == 5:
                        self.win()

        return n >= self.k

    def init_pygame(self):
        # Inizializza la partita
        pygame.init()
        screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH), pygame.RESIZABLE)
        self.screen = screen
        self.ZOINK = pygame.mixer.Sound("wav/zoink.wav")
        self.CLICK = pygame.mixer.Sound("wav/click.wav")
        self.font = pygame.font.SysFont("arial", 30)

    def clear_screen(self):

        # fill board and add gridlines
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # add guide dots
        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        pygame.display.flip()

    def pass_move(self):
        self.black_turn = not self.black_turn
        self.draw()

    def to_move(self, state):
        return PLAYER_WHITE
    def handle_click(self):
        # get board position
        x, y = pygame.mouse.get_pos()
        col, row = xy_to_colrow(x, y, self.size)
        if not is_valid_move(col, row, self.board):
            self.ZOINK.play()
            return

        # update board array
        self.board[col, row] = 1 if self.black_turn else 2

        # get stone groups for black and white
        self_color = "black" if self.black_turn else "white"
        other_color = "white" if self.black_turn else "black"

        # TODO : End of Game
        self.end()

        def filtering(position):
            x, y = position
            if self.board[x-1][y-1] == 0:
                return True
            else:
                return False

        # Mossa del BOT
        global game
        state = GameState(to_move=PLAYER_BLACK,
                          utility=0,
                          board=self.board,
                          moves=set(filter(filtering, [(x, y)
                                                       for x in range(1, self.size + 1)
                                                       for y in range(1, self.size + 1)])))
        a, b = alpha_beta_player(game, state)

        # change turns and draw screen
        self.CLICK.play()
        # self.black_turn = not self.black_turn
        self.draw()

    def end(self):
        # Check ends of game
        count_r = count_c = count_d1 = count_d2 = 0
        curr = 1.0 if self.black_turn else 2.0

        for i in range(self.size):
            for j in range(self.size):

                # Orizzontale
                if self.board[i][j] == curr:
                    count_r += 1
                    if count_r == 5:
                        self.win()
                else:
                    count_r = 0

                # Verticale
                if self.board[j][i] == curr:
                    count_c += 1
                    if count_c == 5:
                        self.win()
                else:
                    count_c = 0

                # Diagonale 1
                if i + 5 < self.size and j + 5 < self.size:
                    for k in range(5):
                        if self.board[i + k][j + k] == curr:
                            count_d1 += 1
                        else:
                            count_d1 = 0
                            break

                    if count_d1 == 5:
                        self.win()

                if i + 5 < self.size and j - 5 < self.size:
                    for k in range(5):
                        if self.board[i + k][j - k] == curr:
                            count_d2 += 1
                        else:
                            count_d2 = 0
                            break

                    if count_d2 == 5:
                        self.win()

    def win(self):
        # TODO: Win
        exit(1)
        pass

    def critical(self):
        # Check ends of game
        count_r = count_c = count_d1 = count_d2 = 0
        adversarial = 1.0 if self.black_turn else 2.0
        my_color = 2.0 if self.black_turn else 1.0
        for i in range(self.size):
            for j in range(self.size):

                # Verticale
                if self.board[i][j] == adversarial:
                    count_r += 1
                    if count_r == 4:
                        if (i < 4 and self.board[i - 4][j] == 0):
                            self.board[i - 4][j] = my_color
                            return True
                        elif (self.board[i + 1][j] == 0):
                            self.board[i + 1][j] = my_color
                            return True

                else:
                    count_r = 0

                # Orizzontale
                if self.board[j][i] == adversarial:
                    count_c += 1
                    if count_c == 4:
                        if (j > 4 and self.board[j - 4][i] == 0):
                            self.board[j - 4][i] = my_color
                            return True
                        elif (j + 1 < self.size and self.board[j + 1][i] == 0):
                            self.board[j + 1][i] = my_color
                            return True
                else:
                    count_c = 0

                # Diagonale 1
                if i + 5 < self.size and j + 5 < self.size:
                    for k in range(4):
                        if self.board[i + k][j + k] == adversarial:
                            count_d1 += 1
                        else:
                            count_d1 = 0
                            break

                    if count_d1 == 4:
                        if (i > 0 and j > 0 and self.board[i - 1][j - 1] == 0):
                            self.board[i - 1][j - 1] = my_color
                            return True
                        elif (i + 4 < self.size and j + 4 < self.size and self.board[i + 4][j + 4] == 0):
                            self.board[i + 4][j + 4] = my_color
                            return True

                if i + 5 < self.size and j - 5 < self.size:
                    for k in range(4):
                        if self.board[i + k][j - k] == adversarial:
                            count_d2 += 1
                        else:
                            count_d2 = 0
                            break

                    if count_d2 == 4:
                        if (i > 0 and j > 0 and self.board[i - 1][j - 1] == 0):
                            self.board[i - 1][j - 1] = my_color
                            return True
                        elif (i < self.size - 1 and j < self.size - 1 and self.board[i + 1][j + 1] == 0):
                            self.board[i + 1][j + 1] = my_color
                            return True
        return False

    def nuova_mossa(self, my_color):
        v = random.sample(range(1, 15), 2)
        while (not is_valid_move(v[0], v[1], self.board)):
            v = random.sample(range(1, 15), 2)
        self.board[v[0], v[1]] = my_color

    def draw(self):
        # draw stones - filled circle and antialiased ring
        self.clear_screen()
        for col, row in zip(*np.where(self.board == 1)):
            x, y = colrow_to_xy(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = colrow_to_xy(col, row, self.size)
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
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_click()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.pass_move()


if __name__ == "__main__":
    game = Gomoku(15)
    game.init_pygame()
    game.clear_screen()
    game.draw()

    while True:
        game.update()
        pygame.time.wait(100)
