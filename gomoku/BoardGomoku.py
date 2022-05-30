import itertools
import sys
import threading
import time

import numpy as np
import pygame
from pygame import gfxdraw

from gomoku.BotGomoku import BotGomoku
from gomoku.ButtonHome import ButtonHome

BOARD_BROWN = (199, 105, 42)
BOARD_DIMENSION = 700
BOARD_BORDER = 75
STONE_RADIUS = 14
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TURN_POS = (BOARD_BORDER, 30)
SCORE_POS = (BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER + 30)
DOT_RADIUS = 4

WIDTH_BUTTON = 200
HEIGHT_BUTTON = 40
X_BUTTON_POSITION = BOARD_DIMENSION / 2 - WIDTH_BUTTON / 2
Y_BUTTON_POSITION = BOARD_DIMENSION / 2 - 110
ELEVATION_BUTTON = 5

PLAYER_BLACK = 1
PLAYER_WHITE = 2


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
    xs = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    ys = np.full(size, BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full(size, BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    ys = np.full(size, BOARD_DIMENSION - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full(size, BOARD_DIMENSION - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
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
    inc = (BOARD_DIMENSION - 2 * BOARD_BORDER) / (size - 1)
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
    inc = (BOARD_DIMENSION - 2 * BOARD_BORDER) / (size - 1)
    x = int(BOARD_BORDER + col * inc)
    y = int(BOARD_BORDER + row * inc)
    return x, y


class BoardGomoku:
    def __init__(self, size, length_victory=5):
        self.size = size
        self.length_victory = length_victory
        self.board = np.zeros((size, size))

        self.screen = pygame.display.set_mode((BOARD_DIMENSION, BOARD_DIMENSION))
        self.start_points, self.end_points = make_grid(size)
        self.stop_drawing = False
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.WRONG_CLICK = pygame.mixer.Sound("../wav/wrong_click.wav")
        self.RIGHT_CLICK = pygame.mixer.Sound("../wav/right_click.wav")

        self.black_turn = True

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

    def request_move(self, ai):
        col, row = ai.bot_move(self.board)

        # draw stone, play sound, check end and pass move
        self.board[col, row] = ai.get_color()
        self.RIGHT_CLICK.play()
        self.end(ai.get_color(), (col, row))
        self.change_turn()

    def is_valid_move(self, col, row):
        if col < 0 or col >= self.size:
            return False
        if row < 0 or row >= self.size:
            return False
        return self.board[col, row] == 0

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

    def draw(self, mod):
        self.clear_screen()

        for col, row in zip(*np.where(self.board == 1)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, WHITE)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, WHITE)

        if mod == 1:
            turn_msg = (
                f"{'Black to move. Click to place stone, press P to pass.' if self.black_turn else 'White to move.'} ")
        elif mod == 2:
            turn_msg = (
                f"{'Black to move. Click to place stone, press P to pass.' if self.black_turn else 'White to move. Click to place stone, press P to pass.'} ")
        else:
            turn_msg = f"{'Black to move.' if self.black_turn else 'White to move.'} "
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        pygame.display.flip()

    def change_turn(self):
        self.black_turn = not self.black_turn

    def update_match(self, human_player):
        while True:
            events = pygame.event.get()
            # Exit
            for event in events:
                if event.type == pygame.QUIT:
                    self.stop_drawing = True
                    pygame.quit()
                    sys.exit()
            # Move or pass turn
            if len(events) > 0:
                if events[0].type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = col_row_from(x, y, self.size)
                    if self.is_valid_move(col, row):
                        # draw stone, play sound, check end and pass move
                        self.board[col, row] = human_player
                        self.RIGHT_CLICK.play()
                        self.end(human_player, (col, row))
                        self.change_turn()
                        break
                    else:
                        self.WRONG_CLICK.play()
                elif events[0].type == pygame.KEYUP:
                    if events[0].key == pygame.K_p:
                        self.change_turn()
                        break


def draw_board_match(board_gomoku, mod):
    while True:
        board_gomoku.draw(mod)
        time.sleep(.1)
        if board_gomoku.stop_drawing:
            break


def play_Player_VS_PC():
    board_gomoku = BoardGomoku(15)
    mod = 1
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS PC")

    bot_white = BotGomoku(PLAYER_WHITE)

    while True:
        board_gomoku.update_match(PLAYER_BLACK)
        board_gomoku.request_move(bot_white)
        pygame.event.clear()


def play_Player_VS_Player():
    board_gomoku = BoardGomoku(15)
    mod = 2
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS Player")

    while True:
        board_gomoku.update_match(PLAYER_BLACK)
        board_gomoku.update_match(PLAYER_WHITE)


def play_PC_VS_PC():
    board_gomoku = BoardGomoku(15)
    mod = 3
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("PC VS PC")

    bot_black = BotGomoku(PLAYER_BLACK)
    bot_white = BotGomoku(PLAYER_WHITE)

    board_gomoku.board[7, 7] = PLAYER_BLACK
    while True:
        board_gomoku.request_move(bot_black)
        board_gomoku.request_move(bot_white)
        pygame.event.clear()


def draw_buttons(screen, list_buttons):
    for button in list_buttons:
        button.draw(screen)


def update_home(screen, list_buttons):
    clock = pygame.time.Clock()
    stop_drawing_button = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Animation button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in list_buttons:
                    button.check_click()
            # Start match
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in list_buttons:
                    if button.pressed:
                        stop_drawing_button = True
                        if button.text == "Player VS PC":
                            play_Player_VS_PC()
                        elif button.text == "Player VS Player":
                            play_Player_VS_Player()
                        elif button.text == "PC vs PC":
                            play_PC_VS_PC()
                        else:
                            exit()
        # Update home screen
        screen.fill('#c7692a')
        draw_buttons(screen, list_buttons)
        pygame.display.update()
        clock.tick(15)
        if stop_drawing_button:
            break


def init_home_gomoku():
    screen = pygame.display.set_mode((BOARD_DIMENSION, BOARD_DIMENSION))
    pygame.display.set_caption('Home Gomoku')
    gui_font = pygame.font.Font(None, 30)

    button_player_vs_pc = ButtonHome(gui_font,
                                     "Player VS PC",
                                     WIDTH_BUTTON,
                                     HEIGHT_BUTTON,
                                     (X_BUTTON_POSITION, Y_BUTTON_POSITION),
                                     ELEVATION_BUTTON)

    button_player_vs_player = ButtonHome(gui_font,
                                         "Player VS Player",
                                         WIDTH_BUTTON,
                                         HEIGHT_BUTTON,
                                         (X_BUTTON_POSITION, Y_BUTTON_POSITION + 60),
                                         ELEVATION_BUTTON)

    button_pc_vs_pc = ButtonHome(gui_font,
                                 "PC VS PC",
                                 WIDTH_BUTTON,
                                 HEIGHT_BUTTON,
                                 (X_BUTTON_POSITION, Y_BUTTON_POSITION + 120),
                                 ELEVATION_BUTTON)

    button_exit = ButtonHome(gui_font,
                             "Exit",
                             WIDTH_BUTTON,
                             HEIGHT_BUTTON,
                             (X_BUTTON_POSITION, Y_BUTTON_POSITION + 180),
                             ELEVATION_BUTTON)

    list_buttons = [button_player_vs_pc, button_player_vs_player, button_pc_vs_pc, button_exit]

    update_home(screen, list_buttons)
