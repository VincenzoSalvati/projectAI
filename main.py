"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file main.py


PURPOSE OF THE FILE: running game.
"""

import numpy as np
import os
import random
import sys
import threading
import warnings
from tkinter import Tk, messagebox, ttk, DISABLED

from bot.BotGomoku import BotGomoku
from bot.constants_ai import *
from graphics.BoardGomoku import BoardGomoku, draw_board_match
from graphics.ButtonHome import *
from graphics.constants_graphics import *
from utility.utils import write_csv_player_vs_pc, write_csv_pc_vs_pc

warnings.filterwarnings("ignore", category=DeprecationWarning)


def init_home_gomoku():
    """Init home Gomoku in order to choose three type of mod:
        - Player VS PC
        - Player VS Player
        - PC VS PC
        - Otherwise: Exit
    """
    # Init home
    screen = pygame.display.set_mode((BOARD_DIMENSION, BOARD_DIMENSION))
    pygame.display.set_caption('Home Gomoku')
    gui_font = pygame.font.Font(None, 30)

    # Init buttons
    button_player_vs_pc = ButtonHome((X_BUTTON_POSITION, Y_BUTTON_POSITION),
                                     (WIDTH_BUTTON, HEIGHT_BUTTON),
                                     "Player VS PC",
                                     gui_font,
                                     ELEVATION_BUTTON)
    button_player_vs_player = ButtonHome((X_BUTTON_POSITION, Y_BUTTON_POSITION + 60),
                                         (WIDTH_BUTTON, HEIGHT_BUTTON),
                                         "Player VS Player",
                                         gui_font,
                                         ELEVATION_BUTTON)
    button_pc_vs_pc = ButtonHome((X_BUTTON_POSITION, Y_BUTTON_POSITION + 120),
                                 (WIDTH_BUTTON, HEIGHT_BUTTON),
                                 "PC VS PC",
                                 gui_font,
                                 ELEVATION_BUTTON)
    button_exit = ButtonHome((X_BUTTON_POSITION, Y_BUTTON_POSITION + 180),
                             (WIDTH_BUTTON, HEIGHT_BUTTON),
                             "Exit",
                             gui_font,
                             ELEVATION_BUTTON)
    list_buttons = [button_player_vs_pc, button_player_vs_player, button_pc_vs_pc, button_exit]

    # Make buttons visible and clickable
    update_home(screen, list_buttons)


def update_home(screen, list_buttons):
    """Draw home's buttons and deal with event click

    Args:
        screen (obj pygame): home's window
        list_buttons (List[Button]): list of buttons to be drawn and on which to listen to the click event
            (default is False)
    """

    # noinspection PyShadowingNames
    def draw_buttons(screen, list_buttons):
        for button in list_buttons:
            button.draw(screen)

    # Init parameters
    clock = pygame.time.Clock()
    stop_drawing_button = False
    while True:
        for event in pygame.event.get():
            # Exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Animation button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in list_buttons:
                    button.check_click()

            # Start mod
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
                            pygame.quit()
                            sys.exit()

        # Update home screen
        screen.fill('#c7692a')
        draw_buttons(screen, list_buttons)
        pygame.display.update()
        clock.tick(15)
        if stop_drawing_button:
            break


# noinspection PyGlobalUndefined,PyDeprecation
def play_player_vs_pc():
    """Match Player VS PC

    """

    global board_gomoku, root

    def opening_human():
        board_gomoku.make_move(PLAYER_BLACK)
        board_gomoku.make_move(PLAYER_WHITE)
        board_gomoku.make_move(PLAYER_BLACK)

    def opening_bot():
        board_gomoku.make_move(BotGomoku(PLAYER_BLACK))
        board_gomoku.make_move(BotGomoku(PLAYER_WHITE))
        board_gomoku.make_move(BotGomoku(PLAYER_BLACK))

    def human_moves_black_stones():
        root.destroy()

        # Start game
        start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)

    def human_moves_white_stones():
        root.destroy()

        # Start game
        start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))

    # noinspection PyShadowingNames
    def human_places_other_2_stones():
        root.destroy()

        board_gomoku.make_move(PLAYER_WHITE)
        board_gomoku.make_move(PLAYER_BLACK)

        # Lets bot decides basing on utility value
        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:  # bot plays with white stones
            # Start game
            start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)
        else:  # bot plays with black stones
            # Start game
            start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))

    def first_turn_of_human():
        Tk().wm_withdraw()  # to hide the main window
        return messagebox.askyesno(title="Turn selection", message="Do you want to be the first to play?")

    # Init board
    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS PC")

    # Swap 2
    if first_turn_of_human():
        # Opening human
        opening_human()

        # Lets bot decides basing on utility value
        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:  # bot plays with white stones
            # Start game
            start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)
        elif white_utility < black_utility:  # bot plays with black stones
            # Start game
            start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))
        else:  # bot places other two stones
            board_gomoku.make_move(BotGomoku(PLAYER_WHITE))
            board_gomoku.make_move(BotGomoku(PLAYER_BLACK))

            # Refresh board screen with a new text
            board_gomoku.draw(1)

            # Lets human decides
            root = Tk()
            root.title("What do you want to do?")
            root.geometry("310x50")
            ttk.Button(root, text="Play with black stones", command=human_moves_black_stones).pack()
            ttk.Button(root, text="Play with white stones", command=human_moves_white_stones).pack()
            root.protocol("WM_DELETE_WINDOW", DISABLED)
            root.eval('tk::PlaceWindow . center')
            root.mainloop()
    else:
        # Opening bot
        opening_bot()

        # Refresh board screen with a new text
        board_gomoku.draw(1)

        # Lets human decides
        root = Tk()
        root.title("What do you want to do?")
        root.geometry("310x75")
        ttk.Button(root, text="Play with black stones", command=human_moves_black_stones).pack()
        ttk.Button(root, text="Play with white stones", command=human_moves_white_stones).pack()
        ttk.Button(root, text="Place 2 stones", command=human_places_other_2_stones).pack()
        root.protocol("WM_DELETE_WINDOW", DISABLED)
        root.eval('tk::PlaceWindow . center')
        root.mainloop()


# noinspection PyDeprecation,PyShadowingNames
def play_player_vs_player():
    """Match Player VS Player

    """
    # Init board
    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS Player")

    # Start game
    start_game(board_gomoku, PLAYER_BLACK, PLAYER_WHITE)


# noinspection PyDeprecation,PyShadowingNames
def play_pc_vs_pc():
    """Match PC VS PC

    """
    # Init board
    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("PC VS PC")

    # Nullify initial advantage between bots
    first_bot = BotGomoku(random.choice((PLAYER_WHITE, PLAYER_BLACK)))
    second_bot = BotGomoku(PLAYER_WHITE if first_bot.get_stone_player() == PLAYER_BLACK else PLAYER_BLACK,
                           BOT_WEIGHTS_2)
    second_bot.main_heuristic = False
    # First black stone randomly placed
    board_gomoku.make_move(BotGomoku(PLAYER_BLACK))
    # Second white stone randomly placed around the black stone
    available_moves = list(BotGomoku(PLAYER_WHITE).search_useful_moves(board_gomoku.board))
    move = available_moves[random.randint(0, len(available_moves) - 1)]
    board_gomoku.board[move] = PLAYER_WHITE
    board_gomoku.moves_done.append((move, np.count_nonzero(board_gomoku.board), PLAYER_WHITE))
    board_gomoku.change_turn()

    # Start game
    start_game(board_gomoku,
               first_bot if first_bot.get_stone_player() == PLAYER_BLACK else second_bot,
               first_bot if first_bot.get_stone_player() == PLAYER_WHITE else second_bot,
               True)


# noinspection PyShadowingNames
def start_game(board_gomoku, player1, player2, is_pc_vs_pc=False):
    """Start game alternating turns between players and, eventually, producing file.csv in order have a matches' log

    Args:
        board_gomoku (BoardGomoku): board on which the game gets involve
        player1 (int or BotGomoku): player who takes part into games
        player2 (int or BotGomoku): player who takes part into games
        is_pc_vs_pc (bool): match between two bot players
            (default is False)
    """
    # Match
    while True:
        board_gomoku.make_move(player1)
        if board_gomoku.end_game:
            break

        board_gomoku.make_move(player2)
        if board_gomoku.end_game:
            break

    # Update matches' log
    if not type(player1) == type(player2) == int:
        if is_pc_vs_pc:
            row = [str(player1.main_heuristic), str(round((player1.chronometer.mean_log() / 1000), 2)) + ' s',
                   str(player1.has_won),
                   str(player2.main_heuristic), str(round((player2.chronometer.mean_log() / 1000), 2)) + ' s',
                   str(player2.has_won),
                   str(board_gomoku.has_tie),
                   str(round((board_gomoku.chronometer_match.get_execution_time() / 1000), 2)) + ' s',
                   str(np.count_nonzero(board_gomoku.board))]
            write_csv_pc_vs_pc(row)
        else:
            bot = player1 if type(player1) == BotGomoku else player2
            row = [str(bot.main_heuristic), str(round((bot.chronometer.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
                   str(board_gomoku.has_tie),
                   str(round((board_gomoku.chronometer_match.get_execution_time() / 1000), 2)) + ' s',
                   str(np.count_nonzero(board_gomoku.board))]
            write_csv_player_vs_pc(row)

    # Restart home
    init_home_gomoku()


if __name__ == '__main__':
    # Init module pygame
    pygame.init()

    # Create log file if it does not exist
    if not os.path.exists("./log"):
        os.mkdir("./log")

    # Start home
    init_home_gomoku()
