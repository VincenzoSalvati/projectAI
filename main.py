import os
import random
import sys
import threading
from tkinter import Tk, messagebox, ttk, DISABLED

import numpy as np

from botAI.BotGomoku import BotGomoku
from graphics.BoardGomoku import BoardGomoku, draw_board_match
from graphics.ButtonHome import *
from graphics.constants import *
from utility.utils import write_csv_player_vs_pc, write_csv_pc_vs_pc


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


def update_home(screen, list_buttons):
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


def draw_buttons(screen, list_buttons):
    for button in list_buttons:
        button.draw(screen)


# noinspection PyGlobalUndefined
def play_player_vs_pc():
    global board_gomoku, root

    def opening_bot():
        board_gomoku.make_move(BotGomoku(PLAYER_BLACK))
        board_gomoku.make_move(BotGomoku(PLAYER_WHITE))
        board_gomoku.make_move(BotGomoku(PLAYER_BLACK))

    def human_move_black_stones():
        root.destroy()

        # Start game
        start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)

    def human_move_white_stones():
        root.destroy()

        # Start game
        start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))

    def human_place_other_2_stones():
        root.destroy()

        board_gomoku.make_move(PLAYER_WHITE)
        board_gomoku.make_move(PLAYER_BLACK)

        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:
            # Start game
            start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)
        else:
            # Start game
            start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))

    def first_turn_of_human():
        Tk().wm_withdraw()  # to hide the main window
        return messagebox.askyesno(title="Turn selection", message="Do you want to be the first to play?")

    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS PC")

    # Swap 2
    if first_turn_of_human():
        board_gomoku.make_move(PLAYER_BLACK)
        board_gomoku.make_move(PLAYER_WHITE)
        board_gomoku.make_move(PLAYER_BLACK)

        white_utility = BotGomoku(PLAYER_WHITE).compute_utility(board_gomoku.board)
        black_utility = BotGomoku(PLAYER_BLACK).compute_utility(board_gomoku.board)
        if white_utility > black_utility:
            # Start game
            start_game(board_gomoku, BotGomoku(PLAYER_WHITE), PLAYER_BLACK)
        elif white_utility < black_utility:
            # Start game
            start_game(board_gomoku, PLAYER_WHITE, BotGomoku(PLAYER_BLACK))
        else:
            board_gomoku.make_move(BotGomoku(PLAYER_WHITE))
            board_gomoku.make_move(BotGomoku(PLAYER_BLACK))

            board_gomoku.draw()

            root = Tk()
            root.title("What do you want to do?")
            root.geometry("310x50")
            ttk.Button(root, text="Playing with black stones", command=human_move_black_stones).pack()
            ttk.Button(root, text="Playing with white stones", command=human_move_white_stones).pack()
            root.protocol("WM_DELETE_WINDOW", DISABLED)
            root.eval('tk::PlaceWindow . center')
            root.mainloop()
    else:
        opening_bot()

        board_gomoku.draw()

        root = Tk()
        root.title("What do you want to do?")
        root.geometry("310x75")
        ttk.Button(root, text="Playing with black stones", command=human_move_black_stones).pack()
        ttk.Button(root, text="Playing with white stones", command=human_move_white_stones).pack()
        ttk.Button(root, text="Place 2 stones", command=human_place_other_2_stones).pack()
        root.protocol("WM_DELETE_WINDOW", DISABLED)
        root.eval('tk::PlaceWindow . center')
        root.mainloop()


def play_player_vs_player():
    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("Player VS Player")

    # Start game
    start_game(board_gomoku, PLAYER_BLACK, PLAYER_WHITE)


def play_pc_vs_pc():
    board_gomoku = BoardGomoku(15)
    thread_draw_board_gomoku = threading.Thread(target=draw_board_match, args=([board_gomoku]))
    thread_draw_board_gomoku.setDaemon(True)
    thread_draw_board_gomoku.start()
    pygame.display.set_caption("PC VS PC")

    first_bot = BotGomoku(random.choice((PLAYER_WHITE, PLAYER_BLACK)))
    second_bot = BotGomoku(PLAYER_WHITE if first_bot.get_color() == PLAYER_BLACK else PLAYER_BLACK)
    second_bot.main_heuristic = False

    # First black stone randomly placed
    board_gomoku.make_move(BotGomoku(PLAYER_BLACK))
    # Second white stone randomly placed around the black stone
    available_moves = list(BotGomoku(PLAYER_WHITE).compute_moves(board_gomoku.board))
    move = available_moves[random.randint(0, len(available_moves) - 1)]
    board_gomoku.board[move] = PLAYER_WHITE
    board_gomoku.moves_done.append((move, np.count_nonzero(board_gomoku.board), PLAYER_WHITE))
    board_gomoku.change_turn()

    # Start game
    start_game(board_gomoku,
               first_bot if first_bot.get_color() == PLAYER_BLACK else second_bot,
               first_bot if first_bot.get_color() == PLAYER_WHITE else second_bot,
               True)


def start_game(board, player1, player2, pc_vs_pc=False):
    while True:
        board.make_move(player1)
        if board.end_game:
            break

        board.make_move(player2)
        if board.end_game:
            break

    # Update log matches
    if not type(player1) == type(player2) == int:
        if pc_vs_pc:
            row = [str(player1.main_heuristic), str(round((player1.chronometer.mean_log() / 1000), 2)) + ' s',
                   str(player1.has_won),
                   str(player2.main_heuristic), str(round((player2.chronometer.mean_log() / 1000), 2)) + ' s',
                   str(player2.has_won),
                   str(board.has_tie), str(round((board.chronometer_match.get_execution_time() / 1000), 2)) + ' s',
                   str(np.count_nonzero(board.board))]
            write_csv_pc_vs_pc(row)
        else:
            bot = player1 if type(player1) == BotGomoku else player2
            row = [str(bot.main_heuristic), str(round((bot.chronometer.mean_log() / 1000), 2)) + ' s', str(bot.has_won),
                   str(board.has_tie), str(round((board.chronometer_match.get_execution_time() / 1000), 2)) + ' s',
                   str(np.count_nonzero(board.board))]
            write_csv_player_vs_pc(row)

    init_home_gomoku()


if __name__ == '__main__':
    pygame.init()

    if not os.path.exists("./log"):
        os.mkdir("./log")

    init_home_gomoku()
