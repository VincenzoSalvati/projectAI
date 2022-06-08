import numpy as np


def check_five_in_row(lines, player):
    count = 0
    for line in lines:
        if np.all(line == [player, player, player, player, player]):
            count += 1
    return count


def check_four_in_row(lines, player):
    count = 0
    for line in lines:
        if np.all(line == [0, player, player, player, player]) or \
                np.all(line == [player, player, player, player, 0]):
            count += 1
    return count


def check_broken_four(lines, player):
    count = 0
    for line in lines:
        if np.all(line == [player, 0, player, player, player]) or \
                np.all(line == [player, player, 0, player, player]) or \
                np.all(line == [player, player, player, 0, player]):
            count += 1
    return count


def check_three_in_row(lines, player):
    count = 0
    for line in lines:
        if np.all(line == [player, player, player, 0, 0]) or \
                np.all(line == [0, player, player, player, 0]) or \
                np.all(line == [0, 0, player, player, player]):
            count += 1
    return count


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


def check_two_in_row(lines, player):
    count = 0
    for line in lines:
        if np.all(line == [player, player, 0, 0, 0]) or \
                np.all(line == [0, player, player, 0, 0]) or \
                np.all(line == [0, 0, player, player, 0]) or \
                np.all(line == [0, 0, 0, player, player]):
            count += 1
    return count


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

# def check_one(lines, player):
#     count = 0
#     for line in lines:
#         if np.all(line == [player, 0, 0, 0, 0]) or \
#                 np.all(line == [0, player, 0, 0, 0]) or \
#                 np.all(line == [0, 0, player, 0, 0]) or \
#                 np.all(line == [0, 0, 0, player, 0]) or \
#                 np.all(line == [0, 0, 0, 0, player]):
#             count += 1
#     return count
