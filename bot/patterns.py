"""
Course: Agenti Intelligenti 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file patterns.py


PURPOSE OF THE FILE: patterns to match.
"""

import numpy as np


def check_five_in_row(lines, stone_player):
    """Return number of matched five in row pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched five in row pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, stone_player, stone_player, stone_player, stone_player]):
            count += 1

    return count


def check_four_in_row(lines, stone_player):
    """Return number of matched four in row pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched four in row pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [0, stone_player, stone_player, stone_player, stone_player]) or \
                np.all(line == [stone_player, stone_player, stone_player, stone_player, 0]):
            count += 1

    return count


def check_broken_four(lines, stone_player):
    """Return number of matched broken four pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched broken four pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, 0, stone_player, stone_player, stone_player]) or \
                np.all(line == [stone_player, stone_player, 0, stone_player, stone_player]) or \
                np.all(line == [stone_player, stone_player, stone_player, 0, stone_player]):
            count += 1

    return count


def check_three_in_row(lines, stone_player):
    """Return number of matched three in row pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched three in row pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, stone_player, stone_player, 0, 0]) or \
                np.all(line == [0, stone_player, stone_player, stone_player, 0]) or \
                np.all(line == [0, 0, stone_player, stone_player, stone_player]):
            count += 1

    return count


def check_broken_three(lines, stone_player):
    """Return number of matched broken three pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched broken three pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, stone_player, 0, 0, stone_player]) or \
                np.all(line == [stone_player, stone_player, 0, stone_player, 0]) or \
                np.all(line == [stone_player, 0, 0, stone_player, stone_player]) or \
                np.all(line == [stone_player, 0, stone_player, stone_player, 0]) or \
                np.all(line == [stone_player, 0, stone_player, 0, stone_player]) or \
                np.all(line == [0, stone_player, 0, stone_player, stone_player]) or \
                np.all(line == [0, stone_player, stone_player, 0, stone_player]):
            count += 1

    return count


def check_two_in_row(lines, stone_player):
    """Return number of matched two in row pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched two in row pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, stone_player, 0, 0, 0]) or \
                np.all(line == [0, stone_player, stone_player, 0, 0]) or \
                np.all(line == [0, 0, stone_player, stone_player, 0]) or \
                np.all(line == [0, 0, 0, stone_player, stone_player]):
            count += 1

    return count


def check_broken_two(lines, stone_player):
    """Return number of matched broken two pattern

    Args:
        lines (array[int]): array to be checked
        stone_player (int) : player's stone to be checked

    Returns:
        int: number of matched broken two pattern
    """
    # Init parameters
    count = 0

    # Check
    for line in lines:
        if np.all(line == [stone_player, 0, stone_player, 0, 0]) or \
                np.all(line == [stone_player, 0, 0, stone_player, 0]) or \
                np.all(line == [stone_player, 0, 0, 0, stone_player]) or \
                np.all(line == [0, stone_player, 0, stone_player, 0]) or \
                np.all(line == [0, stone_player, 0, 0, stone_player]) or \
                np.all(line == [0, 0, stone_player, 0, stone_player]):
            count += 1

    return count
