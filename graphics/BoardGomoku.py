"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file BoardGomoku.py


PURPOSE OF THE FILE: set board Gomoku and deal with the match.
"""

import itertools
import random
import sys
from tkinter import *
from tkinter import messagebox

import numpy as np
import pygame
from pygame import gfxdraw

from bot.BotGomoku import BotGomoku
from bot.constants import PLAYER_BLACK
from graphics.constants import *
from utility.Chronometer import Chronometer

new_actions_performed = False


def make_grid(size):
    """Return list of (start_point, end_point pairs) defining gridlines

    Args:
        size (int): size of grid

    Returns:
        Tuple[List[Tuple[float, float]]]: start and end points for gridlines
    """
    start_points, end_points = [], []
    # Vertical start points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    ys = np.full(size, BOARD_BORDER)
    start_points += list(zip(xs, ys))
    # Horizontal start points (constant x)
    xs = np.full(size, BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))
    # Vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_DIMENSION - BOARD_BORDER, size)
    ys = np.full(size, BOARD_DIMENSION - BOARD_BORDER)
    end_points += list(zip(xs, ys))
    # Horizontal end points (constant x)
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
    """Object BoardGomoku

    Attributes:
        size (int): size board along one dimension
        length_victory (int): number of consecutively stones necessary to win

        board (numpy.array[int, int]): representative matrix of Gomoku board

        screen (obj pygame): home's window
        start_points (List[Tuple[float, float]]): start points for gridlines
        end_points (List[Tuple[float, float]]): end points for gridlines
        font (obj pygame): font of top written
        font_number_stone (obj pygame): font of stones' number written
        RIGHT_CLICK (obj pygame): sound right click
        WRONG_CLICK (obj pygame): sound wrong click

        moves_done (List[Tuple[int, int], int, int]): list of moved stones

        black_turn (bool): color turn
        bot_turn (bool): bot turn
        end_game (bool): end of the game with a winner
        has_tie (bool): end of the game as tie

        chronometer_match (Chronometer): take the elapsed time of the match
    """

    def __init__(self, size, length_victory=5):
        """Init board

        Args:
            size (int): size board along one dimension
            length_victory (int): number of consecutively stones necessary to win
                (default is 5)
        """
        # Init attributes
        self.size = size
        self.length_victory = length_victory

        self.board = np.zeros((size, size))

        self.screen = pygame.display.set_mode((BOARD_DIMENSION, BOARD_DIMENSION))
        self.start_points, self.end_points = make_grid(size)
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_number_stone = pygame.font.SysFont('Arial', 15, bold=True)
        self.RIGHT_CLICK = pygame.mixer.Sound("./data/right_click.wav")
        self.WRONG_CLICK = pygame.mixer.Sound("./data/wrong_click.wav")

        self.moves_done = []

        self.black_turn = True
        self.bot_turn = True
        self.end_game = False
        self.has_tie = False

        self.chronometer_match = Chronometer()

        # Start match's chronometer
        self.chronometer_match.start()

    def check_end_game(self, player_stone, last_move, bot=None):
        """Check if the player has won the match

        Args:
            player_stone (int): identification player's stone
            last_move (Tuple[int, int]): last player's move
            bot (BotGomoku): BotGomoku object that could win
                (default is None)
        """
        # Init parameters
        x, y = last_move
        x += 5
        y += 5

        padded = np.pad(self.board, 5)
        clipped_row = padded[x - 5:x + 6, y]
        clipped_col = padded[x, y - 5:y + 6]
        clipped_diagonals = np.diag(padded[x - 5:x + 6, y - 5:y + 6])
        clipped_flipped_diagonals = np.diag(np.flip(padded[x - 5:x + 6, y - 5:y + 6], 1))

        count_stones = 0

        # Check if the player has won
        for clip in [clipped_row, clipped_col, clipped_diagonals, clipped_flipped_diagonals]:
            for stone in clip:
                if stone == player_stone:
                    count_stones += 1
                elif count_stones == 5:
                    break
                else:
                    count_stones = 0
            if count_stones == 5:
                self.win(player_stone, bot)
            else:
                count_stones = 0

    def win(self, player_stone, bot=None):
        """Announcing the player's victory and stopping the match's chronometer

        Args:
            player_stone (int): identification player's stone
            bot (BotGomoku): bot player
                (default is None)
        """
        if self.end_game:
            return

        # Stop match's chronometer
        self.chronometer_match.stop()

        # Refresh board screen with a new text
        self.draw()

        # Set end game
        self.end_game = True

        # Announcement
        Tk().wm_withdraw()  # Hide useless window
        heuristic_string = ""
        if bot is not None:
            bot.has_won = True
            heuristic_string = f"Main heuristic = {bot.main_heuristic}."
        messagebox.showinfo('Game over',
                            "The winner is: " f"{'BLACK!!' if player_stone == PLAYER_BLACK else 'WHITE!! '}"
                            f" {'Bot has won! - ' + heuristic_string if bot is not None else 'Human has won!'}")

    def tie(self):
        """Announcing the tie and stopping the match's chronometer

        """
        if self.end_game:
            return

        # Stop match's chronometer
        self.chronometer_match.stop()

        # Refresh board screen with a new text
        self.draw()

        # Set end game
        self.end_game = True
        self.has_tie = True

        # Announcement
        Tk().wm_withdraw()  # Hide useless window
        messagebox.showinfo('Game over',
                            "The game ended in a tie.")

    def is_valid_move(self, col, row):
        """Return if the coordinates do not create conflicts

        Args:
            col (int): column number (horizontal position)
            row (int): row number (vertical position)

        Returns:
            bool: coordinates do not create conflicts
        """
        if col < 0 or col >= self.size:
            return False
        if row < 0 or row >= self.size:
            return False
        return self.board[col, row] == 0

    def reset_board(self):
        """Clean the board and add a grid line with guide points

        """
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

        # Flip matrix of Gomoku board
        pygame.display.flip()

    def draw(self, mod=0):
        """Draw board with stones and text

        Args:
            mod (int): indicate the text to write

        """
        # Reset board
        self.reset_board()

        # Draw stones
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
        if mod == 1:
            turn_msg = f"{'Black to move.' if self.black_turn else 'White to move.'}"
        elif mod == 2:
            turn_msg = f"{'Bot ' if self.bot_turn else 'Human '}" + \
                       f"{'black to move.' if self.black_turn else 'white to move.'}"
        else:
            turn_msg = "Game over!"
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        pygame.display.flip()

    def change_turn(self):
        """Change turn

        """
        global new_actions_performed

        self.black_turn = not self.black_turn
        new_actions_performed = True

    def human_move(self, human):
        """Manage human events

        Args:
            human (int): human player's stone
        """
        while True:
            events = pygame.event.get()
            # Exit
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Move and pass turn
            if len(events) > 0:
                if events[0].type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = col_row_from(x, y, self.size)
                    if self.is_valid_move(col, row):
                        # draw stone, play sound, check end and pass move
                        self.board[col, row] = human
                        self.moves_done.append(((col, row), np.count_nonzero(self.board), human))
                        self.RIGHT_CLICK.play()
                        self.check_end_game(human, (col, row))
                        self.change_turn()
                        break
                    else:
                        self.WRONG_CLICK.play()

    def bot_move(self, bot):
        """Manage bot move

        Args:
            bot (BotGomoku): bot player
        """
        if np.count_nonzero(self.board) == 0:
            col, row = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        else:
            col, row = bot.bot_search_move(self.board)

        # Tie
        if (col, row) == (-1, -1):
            self.tie()

        # Draw stone, play sound, check end and pass move
        self.board[col, row] = bot.get_stone_player()
        self.moves_done.append(((col, row), np.count_nonzero(self.board), bot.get_stone_player()))
        self.RIGHT_CLICK.play()
        self.check_end_game(bot.get_stone_player(), (col, row), bot)
        self.change_turn()

    def make_move(self, player):
        """Manage player move

        Args:
            player (int or BotGomoku): player who takes part into games
        """

        global new_actions_performed

        # Bot
        if type(player) == BotGomoku:
            # Set parameters
            self.bot_turn = True
            new_actions_performed = True
            events = pygame.event.get()
            # Bot move
            player.chronometer.start()
            self.bot_move(player)
            player.chronometer.stop_and_append_log()
            # Exit
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        # Human
        else:
            # Set parameters
            self.bot_turn = False
            new_actions_performed = True
            # Human move
            self.human_move(player)


def draw_board_match(board_gomoku):
    """Draw and refresh board

    Args:
        board_gomoku (BoardGomoku): board on which the game gets involve
    """

    global new_actions_performed

    board_gomoku.draw(1)
    while True:
        if new_actions_performed:
            new_actions_performed = False
            board_gomoku.draw(2)
        if board_gomoku.end_game:
            break
    board_gomoku.draw()
