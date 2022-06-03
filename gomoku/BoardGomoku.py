import csv
import itertools
import random
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import numpy as np
import pygame
from pygame import gfxdraw

from gomoku.BotGomoku import BotGomoku
from gomoku.ButtonHome import ButtonHome
from gomoku.ChronoMeter import ChronoMeter

BOARD_BROWN = (199, 105, 42)
BOARD_DIMENSION = 700
BOARD_BORDER = 75

STONE_RADIUS = 18
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GUIDE_DOT_RADIUS = 4

TURN_POS = (BOARD_BORDER, 30)

WIDTH_BUTTON = 200
HEIGHT_BUTTON = 40
X_BUTTON_POSITION = BOARD_DIMENSION / 2 - WIDTH_BUTTON / 2
Y_BUTTON_POSITION = BOARD_DIMENSION / 2 - 110
ELEVATION_BUTTON = 5

PLAYER_BLACK = 1
PLAYER_WHITE = 2


def read_csv_player_vs_pc():
    with open('Player_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def read_csv_pc_vs_pc():
    with open('PC_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def write_csv_player_vs_pc(row):
    with open('Player_VS_PC.csv', 'a+', newline='') as player_vs_pc_file:
        csvwriter = csv.writer(player_vs_pc_file)
        if not read_csv_player_vs_pc():
            csvwriter.writerow(['Bot main heuristic', 'Bot mean elapsed time', 'Bot win',
                                'Tie', 'Match elapsed time'])
        csvwriter.writerow(row)


def write_csv_pc_vs_pc(row):
    with open('PC_VS_PC.csv', 'a+', newline='') as pc_vs_pc_file:
        csvwriter = csv.writer(pc_vs_pc_file)
        if not read_csv_pc_vs_pc():
            csvwriter.writerow(
                ['1° bot main heuristic', '1° bot mean elapsed time', '1° bot win',
                 '2° bot main heuristic', '2° bot mean elapsed time', '2° bot win',
                 'Tie', 'Match elapsed time'])
        csvwriter.writerow(row)


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


# noinspection PyShadowingNames


class BoardGomoku:
    def __init__(self, size, length_victory=5):
        self.size = size
        self.length_victory = length_victory
        self.board = np.zeros((size, size))

        self.screen = pygame.display.set_mode((BOARD_DIMENSION, BOARD_DIMENSION))
        self.start_points, self.end_points = make_grid(size)
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_number_stone = pygame.font.SysFont('Arial', 15, bold=True)
        self.WRONG_CLICK = pygame.mixer.Sound("../wav/wrong_click.wav")
        self.RIGHT_CLICK = pygame.mixer.Sound("../wav/right_click.wav")

        self.black_turn = True

        self.stop_drawing = False
        self.end_game = False
        self.stop_passing = False

        self.has_tie = False

        self.moves_done = []

    def end(self, player, move, bot):
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
            if count_stones == 5 and not self.stop_drawing:
                self.win(player, bot)
            else:
                count_stones = 0

    def win(self, player, bot=None):
        self.stop_drawing = True
        heuristic_string = ""
        if bot is not None:
            bot.has_won = True
            heuristic_string = f"Main heuristic = {bot.main_heuristic}."
        Tk().wm_withdraw()  # Hide useless window
        messagebox.showinfo('Game over',
                            "The winner is: " f"{'BLACK!!' if player == PLAYER_BLACK else 'WHITE!! '} {'Bot has won! - ' + heuristic_string if bot is not None else 'Human has won!'}")

    def tie(self):
        self.has_tie = True
        self.stop_drawing = True
        Tk().wm_withdraw()  # Hide useless window
        messagebox.showinfo('Game over',
                            "The game ended in a tie.")

    def request_move(self, bot_gomoku):
        if np.count_nonzero(self.board) == 0:
            col, row = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        else:
            col, row = bot_gomoku.bot_move(self.board)

        if (col, row) == (-1, -1):
            self.tie()

        # Draw stone, play sound, check end and pass move
        self.board[col, row] = bot_gomoku.get_color()
        self.moves_done.append(((col, row), np.count_nonzero(self.board), bot_gomoku.get_color()))
        self.RIGHT_CLICK.play()
        self.end(bot_gomoku.get_color(), (col, row), bot_gomoku)
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
        # Fill board and add gridlines
        self.screen.fill(BOARD_BROWN)
        for start_point, end_point in zip(self.start_points, self.end_points):
            pygame.draw.line(self.screen, BLACK, start_point, end_point)

        # Add guide dots
        guide_dots = [3, self.size // 2, self.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, GUIDE_DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, GUIDE_DOT_RADIUS, BLACK)
        pygame.display.flip()

    def draw(self, mod):
        self.clear_screen()

        # Redraw stones
        for col, row in zip(*np.where(self.board == 1)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, BLACK)
        for col, row in zip(*np.where(self.board == 2)):
            x, y = x_y_from(col, row, self.size)
            gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, WHITE)
            gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, WHITE)

        # Draw number stones
        for stone in self.moves_done:
            col = stone[0][0]
            row = stone[0][1]
            number = stone[1]
            player = stone[2]
            if number < 10:
                col -= 0.1
                row -= 0.2
            elif number < 100:
                col -= 0.2
                row -= 0.2
            else:
                col -= 0.3
                row -= 0.2
            position_stone = x_y_from(col, row, self.size)
            number = self.font_number_stone.render(str(number), True, WHITE if player == PLAYER_BLACK else BLACK)
            self.screen.blit(number, position_stone)

        # Text above
        if mod == 1 and not self.stop_passing:
            turn_msg = (
                f"{'Black to move. Press P to pass own turn.' if self.black_turn else 'White to move. Press P to pass own turn.'}")
        elif mod == 2:
            turn_msg = (
                f"{'Black to move. Press P to pass own turn.' if self.black_turn else 'White to move. Press P to pass own turn.'}")
        elif mod == 3 or self.stop_passing:
            turn_msg = f"{'Black to move.' if self.black_turn else 'White to move.'}"
        else:
            turn_msg = "Game over!"
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        pygame.display.flip()

        if mod == 0:
            self.end_game = True

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
                        self.moves_done.append(((col, row), np.count_nonzero(self.board), human_player))
                        self.RIGHT_CLICK.play()
                        self.end(human_player, (col, row), None)
                        self.change_turn()
                        break
                    else:
                        self.WRONG_CLICK.play()
                elif events[0].type == pygame.KEYUP and not self.stop_passing:
                    if events[0].key == pygame.K_p:
                        self.change_turn()
                        break


# noinspection PyShadowingNames
def draw_board_match(board_gomoku, mod):
    while True:
        board_gomoku.draw(mod)
        time.sleep(.5)
        if board_gomoku.stop_drawing:
            break

    while True:
        board_gomoku.draw(0)
        time.sleep(.5)
        if board_gomoku.end_game:
            break


# noinspection PyGlobalUndefined,DuplicatedCode
def play_player_vs_pc():
    global board_gomoku, chrono_match, chrono_bot, root, player_color, bot

    # noinspection PyShadowingNames,DuplicatedCode
    def opening_bot():
        move = random.randint(0, board_gomoku.size - 1), random.randint(0, board_gomoku.size - 1)
        board_gomoku.moves_done.append((move, np.count_nonzero(board_gomoku.board) + 1, PLAYER_BLACK))
        board_gomoku.board[move] = PLAYER_BLACK
        board_gomoku.change_turn()

        board_gomoku.request_move(BotGomoku(PLAYER_WHITE))

        board_gomoku.request_move(BotGomoku(PLAYER_BLACK))

    # noinspection PyShadowingNames
    def human_move_black_stones():
        root.destroy()

        player_color = PLAYER_BLACK
        bot = BotGomoku(PLAYER_WHITE)

        chrono_bot.start()
        board_gomoku.request_move(bot)
        chrono_bot.stop_and_append_log()
        print(
            "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
            str(np.count_nonzero(board_gomoku.board)) + "): " +
            str(round(chrono_bot.get_execution_time() / 1000, 3)) +
            "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
            str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

        # Start game
        while True:
            if board_gomoku.stop_drawing:
                break
            board_gomoku.update_match(player_color)
            if board_gomoku.stop_drawing:
                break

            chrono_bot.start()
            if board_gomoku.stop_drawing:
                break
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            if board_gomoku.stop_drawing:
                break
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            pygame.event.clear()

        chrono_match.stop()
        row = [str(bot.main_heuristic), str(round((chrono_bot.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
               str(board_gomoku.has_tie), str(round((chrono_match.get_execution_time() / 1000), 2)) + ' s']
        write_csv_player_vs_pc(row)

        sys.exit()

    # noinspection PyShadowingNames,DuplicatedCode
    def human_move_white_stones():
        root.destroy()

        player_color = PLAYER_WHITE
        bot = BotGomoku(PLAYER_BLACK)

        # Start game
        while True:
            if board_gomoku.stop_drawing:
                break
            board_gomoku.update_match(player_color)
            if board_gomoku.stop_drawing:
                break

            chrono_bot.start()
            if board_gomoku.stop_drawing:
                break
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            if board_gomoku.stop_drawing:
                break
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            pygame.event.clear()

        chrono_match.stop()
        row = [str(bot.main_heuristic), str(round((chrono_bot.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
               str(board_gomoku.has_tie), str(round((chrono_match.get_execution_time() / 1000), 2)) + ' s']
        write_csv_player_vs_pc(row)

        sys.exit()

    # noinspection DuplicatedCode, PyShadowingNames
    def human_place_other_2_stones():
        root.destroy()

        board_gomoku.stop_passing = True
        board_gomoku.update_match(PLAYER_WHITE)
        board_gomoku.update_match(PLAYER_BLACK)
        board_gomoku.stop_passing = False

        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:
            player_color = PLAYER_BLACK
            bot = BotGomoku(PLAYER_WHITE)
        else:
            player_color = PLAYER_WHITE
            bot = BotGomoku(PLAYER_BLACK)

            chrono_bot.start()
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            board_gomoku.change_turn()

        # Start game
        while True:
            if board_gomoku.stop_drawing:
                break
            board_gomoku.update_match(player_color)
            if board_gomoku.stop_drawing:
                break

            chrono_bot.start()
            if board_gomoku.stop_drawing:
                break
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            if board_gomoku.stop_drawing:
                break
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            pygame.event.clear()

        chrono_match.stop()
        row = [str(bot.main_heuristic), str(round((chrono_bot.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
               str(board_gomoku.has_tie), str(round((chrono_match.get_execution_time() / 1000), 2)) + ' s']
        write_csv_player_vs_pc(row)

        sys.exit()

    def first_turn_of_human():
        Tk().wm_withdraw()  # to hide the main window
        return messagebox.askyesno(title="Turn selection", message="Do you want to be the first to play?")

    board_gomoku = BoardGomoku(15)
    mod = 1
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS PC")

    chrono_match = ChronoMeter()
    chrono_bot = ChronoMeter()

    chrono_match.start()
    # Swap 2
    if first_turn_of_human():
        board_gomoku.stop_passing = True
        board_gomoku.update_match(PLAYER_BLACK)
        board_gomoku.update_match(PLAYER_WHITE)
        board_gomoku.update_match(PLAYER_BLACK)
        board_gomoku.stop_passing = False

        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:
            player_color = PLAYER_BLACK
            bot = BotGomoku(PLAYER_WHITE)
        else:
            player_color = PLAYER_WHITE
            bot = BotGomoku(PLAYER_BLACK)

            chrono_bot.start()
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            board_gomoku.change_turn()

        # Start game
        while True:
            if board_gomoku.stop_drawing:
                break
            board_gomoku.update_match(player_color)
            if board_gomoku.stop_drawing:
                break

            chrono_bot.start()
            if board_gomoku.stop_drawing:
                break
            board_gomoku.request_move(bot)
            chrono_bot.stop_and_append_log()
            if board_gomoku.stop_drawing:
                break
            print(
                "Elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
                str(np.count_nonzero(board_gomoku.board)) + "): " +
                str(round(chrono_bot.get_execution_time() / 1000, 3)) +
                "[s]    -    Mean elapsed time" + f"{' main' if bot.main_heuristic == True else ' No-main'}" + " bot: " +
                str(round(chrono_bot.mean_log() / 1000, 3)) + "[s]")

            pygame.event.clear()

        chrono_match.stop()

        row = [str(bot.main_heuristic), str(round((chrono_bot.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
               str(board_gomoku.has_tie), str(round((chrono_match.get_execution_time() / 1000), 2)) + ' s']
        write_csv_player_vs_pc(row)

        pygame.quit()
        sys.exit()

    else:
        opening_bot()
        root = Tk()
        root.title("What do you want to do?")
        root.geometry("310x75")
        ttk.Button(root, text="Playing with black stones", command=human_move_black_stones).pack()
        ttk.Button(root, text="Playing with white stones", command=human_move_white_stones).pack()
        ttk.Button(root, text="Place 2 stones", command=human_place_other_2_stones).pack()
        root.protocol("WM_DELETE_WINDOW", human_place_other_2_stones)
        root.mainloop()


# noinspection PyShadowingNames
def play_player_vs_player():
    board_gomoku = BoardGomoku(15)
    mod = 2
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS Player")

    while True:
        if board_gomoku.stop_drawing:
            break

        board_gomoku.update_match(PLAYER_BLACK)

        if board_gomoku.stop_drawing:
            break

        board_gomoku.update_match(PLAYER_WHITE)

        if board_gomoku.stop_drawing:
            break

    sys.exit()


# noinspection PyShadowingNames,DuplicatedCode
def play_pc_vs_pc():
    board_gomoku = BoardGomoku(15)
    mod = 3
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku, mod]))
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("PC VS PC")

    first_bot = BotGomoku(random.randint(1, 2))

    second_bot = BotGomoku(PLAYER_WHITE if first_bot.get_color() == PLAYER_BLACK else PLAYER_BLACK)
    second_bot.main_heuristic = False

    chrono_match = ChronoMeter()

    chrono_match.start()
    # First 2 random move
    chrono_first_bot = ChronoMeter()
    chrono_second_bot = ChronoMeter()

    if first_bot.get_color() == PLAYER_BLACK:
        board_gomoku.request_move(first_bot)

        available_moves = list(second_bot.compute_moves(board_gomoku.board))
        move = available_moves[random.randint(0, len(available_moves) - 1)]
        board_gomoku.board[move] = second_bot.get_color()
        board_gomoku.moves_done.append((move, np.count_nonzero(board_gomoku.board), second_bot.get_color()))
        board_gomoku.change_turn()
    else:
        board_gomoku.request_move(second_bot)

        available_moves = list(first_bot.compute_moves(board_gomoku.board))
        move = available_moves[random.randint(0, len(available_moves) - 1)]
        board_gomoku.board[move] = first_bot.get_color()
        board_gomoku.moves_done.append((move, np.count_nonzero(board_gomoku.board), first_bot.get_color()))
        board_gomoku.change_turn()

        chrono_second_bot.start()
        board_gomoku.request_move(second_bot)
        chrono_second_bot.stop_and_append_log()
        print(
            "Elapsed time" + f"{' main' if second_bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
            str(np.count_nonzero(board_gomoku.board)) + "): " +
            str(round(chrono_second_bot.get_execution_time() / 1000, 3)) +
            "[s]    -    Mean elapsed time" + f"{' main' if second_bot.main_heuristic == True else ' No-main'}" + " bot: " +
            str(round(chrono_second_bot.mean_log() / 1000, 3)) + "[s]")

    # Start game
    while True:
        chrono_first_bot.start()
        if board_gomoku.stop_drawing:
            break
        board_gomoku.request_move(first_bot)
        chrono_first_bot.stop_and_append_log()
        if board_gomoku.stop_drawing:
            break
        print(
            "Elapsed time" + f"{' main' if first_bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
            str(np.count_nonzero(board_gomoku.board)) + "): " +
            str(round(chrono_first_bot.get_execution_time() / 1000, 3)) +
            "[s]    -    Mean elapsed time" + f"{' main' if first_bot.main_heuristic == True else ' No-main'}" + " bot: " +
            str(round(chrono_first_bot.mean_log() / 1000, 3)) + "[s]")

        chrono_second_bot.start()
        if board_gomoku.stop_drawing:
            break
        board_gomoku.request_move(second_bot)
        chrono_second_bot.stop_and_append_log()
        if board_gomoku.stop_drawing:
            break
        print(
            "Elapsed time" + f"{' main' if second_bot.main_heuristic == True else ' No-main'}" + " bot(#move " +
            str(np.count_nonzero(board_gomoku.board)) + "): " +
            str(round(chrono_second_bot.get_execution_time() / 1000, 3)) +
            "[s]    -    Mean elapsed time" + f"{' main' if second_bot.main_heuristic == True else ' No-main'}" + " bot: " +
            str(round(chrono_second_bot.mean_log() / 1000, 3)) + "[s]")

        pygame.event.clear()

    chrono_match.stop()
    row = [str(first_bot.main_heuristic), str(round((chrono_first_bot.mean_log() / 1000), 2)) + ' s',
           str(first_bot.has_won),
           str(second_bot.main_heuristic), str(round((chrono_second_bot.mean_log() / 1000), 2)) + ' s',
           str(second_bot.has_won),
           str(board_gomoku.has_tie), str(round((chrono_match.get_execution_time() / 1000), 2)) + ' s']
    write_csv_pc_vs_pc(row)

    sys.exit()


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
                            play_player_vs_pc()
                        elif button.text == "Player VS Player":
                            play_player_vs_player()
                        elif button.text == "PC VS PC":
                            play_pc_vs_pc()
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
