import copy

import numpy as np


def generation_pattern_by_five():
    # Winning matrix
    matrix_ones = [[1, 1, 1, 1, 1]]

    # Series of 3 and 4
    list_three_and_four = []
    for zeros in range(1, 3):
        matrix = []
        for zero in range(zeros):
            matrix.append(0)
        for one in range(5 - zeros):
            matrix.append(1)
        list_three_and_four.append(matrix)

    # Flip patterns horizontally
    reversed_list_three_and_four = []
    for pattern in list_three_and_four:
        matrix = copy.copy(pattern)
        matrix.reverse()
        reversed_list_three_and_four.append(matrix)

    # Add patterns with hole
    list_hole = []
    for index_hole in range(1, 4):
        matrix = copy.copy(matrix_ones[0])
        matrix[index_hole] = 0
        list_hole.append(matrix)

    return [matrix_ones, list_three_and_four, reversed_list_three_and_four, list_hole]


def generation_pattern_by_six():
    # Fetch list of patterns by five
    lists_of_patterns = generation_pattern_by_five()

    # Add permutations of 0s and 2s to the side
    for list_of_patterns in lists_of_patterns:
        list_of_patterns_app = copy.copy(list_of_patterns)
        for pattern in list_of_patterns_app:
            pattern_end = copy.copy(pattern)
            pattern.insert(0, 0)
            pattern_end.append(0)
            list_of_patterns.append(pattern_end)
            matrix = copy.copy(pattern)
            matrix_end = copy.copy(pattern_end)
            matrix[0] = 2
            matrix_end[5] = 2
            list_of_patterns.append(matrix)
            list_of_patterns.append(matrix_end)

    return lists_of_patterns


def generation_pattern_by_seven():
    # Fetch list of patterns by five
    lists_of_patterns = generation_pattern_by_five()

    # Add permutations of 0s and 2s combinations to the sides
    for list_of_patterns in lists_of_patterns:
        list_of_patterns_app = copy.copy(list_of_patterns)
        for pattern in list_of_patterns_app:
            pattern.insert(0, 0)
            pattern.append(0)
            matrix = copy.copy(pattern)
            matrix[0] = 0
            matrix[6] = 2
            list_of_patterns.append(matrix)
            matrix = copy.copy(pattern)
            matrix[0] = 2
            matrix[6] = 0
            list_of_patterns.append(matrix)
            matrix = copy.copy(pattern)
            matrix[0] = 2
            matrix[6] = 2
            list_of_patterns.append(matrix)

    return lists_of_patterns


def generation_special_pattern():
    #Obtuse angle
    pattern_V_three_obtuse_angle = np.zeros((5, 9))
    pattern_V_four_obtuse_angle = np.zeros((5, 9))
    pattern_V_three_obtuse_angle_central_one = np.zeros((5, 9))
    pattern_V_four_obtuse_angle_central_one = np.zeros((5, 9))
    for r in range(5):
        for c in range(9):
            if (r == c or r == 9 - c - 1) and r != 4:
                if r != 0:
                    pattern_V_three_obtuse_angle[r, c] = 1
                    pattern_V_three_obtuse_angle_central_one[r, c] = 1
                pattern_V_four_obtuse_angle[r, c] = 1
                pattern_V_four_obtuse_angle_central_one[r, c] = 1
            elif r == 4 and c == 4:
                pattern_V_three_obtuse_angle_central_one[r, c] = 1
                pattern_V_four_obtuse_angle_central_one[r, c] = 1

    #Acute angle
    pattern_V_three_acute_angle = np.zeros((5, 5))
    pattern_V_four_acute_angle = np.zeros((5, 5))
    pattern_V_three_acute_angle_central_one = np.zeros((5, 5))
    pattern_V_four_acute_angle_central_one = np.zeros((5, 5))
    for r in range(5):
        for c in range(5):
            if (r == c or c == 4) and r != 4:
                if r != 0:
                    pattern_V_three_acute_angle[r, c] = 1
                    pattern_V_three_acute_angle_central_one[r, c] = 1
                pattern_V_four_acute_angle[r, c] = 1
                pattern_V_four_acute_angle_central_one[r, c] = 1
            elif r == 4 and c == 4:
                pattern_V_three_acute_angle_central_one[r, c] = 1
                pattern_V_four_acute_angle_central_one[r, c] = 1

    #List for each rotation of 90 degree
    list_pattern_V_three_obtuse_angle = []
    list_pattern_V_four_obtuse_angle = []

    list_pattern_V_three_obtuse_angle_central_one = []
    list_pattern_V_four_obtuse_angle_central_one = []

    list_pattern_V_three_acute_angle = []
    list_pattern_V_four_acute_angle = []

    list_pattern_V_three_acute_angle_central_one = []
    list_pattern_V_four_acute_angle_central_one = []

    for rotation in range(4):
        pattern_V_three_obtuse_angle = np.rot90(pattern_V_three_obtuse_angle)
        list_pattern_V_three_obtuse_angle.append(pattern_V_three_obtuse_angle)
        pattern_V_four_obtuse_angle = np.rot90(pattern_V_four_obtuse_angle)
        list_pattern_V_four_obtuse_angle.append(pattern_V_four_obtuse_angle)

        pattern_V_three_obtuse_angle_central_one = np.rot90(pattern_V_three_obtuse_angle_central_one)
        list_pattern_V_three_obtuse_angle_central_one.append(pattern_V_three_obtuse_angle_central_one)
        pattern_V_four_obtuse_angle_central_one = np.rot90(pattern_V_four_obtuse_angle_central_one)
        list_pattern_V_four_obtuse_angle_central_one.append(pattern_V_four_obtuse_angle_central_one)

        pattern_V_three_acute_angle = np.rot90(pattern_V_three_acute_angle)
        list_pattern_V_three_acute_angle.append(pattern_V_three_acute_angle)
        pattern_V_four_acute_angle = np.rot90(pattern_V_four_acute_angle)
        list_pattern_V_four_acute_angle.append(pattern_V_four_acute_angle)

        pattern_V_three_acute_angle_central_one = np.rot90(pattern_V_three_acute_angle_central_one)
        list_pattern_V_three_acute_angle_central_one.append(pattern_V_three_acute_angle_central_one)
        pattern_V_four_acute_angle_central_one = np.rot90(pattern_V_four_acute_angle_central_one)
        list_pattern_V_four_acute_angle_central_one.append(pattern_V_four_acute_angle_central_one)

    return [list_pattern_V_four_obtuse_angle,
            list_pattern_V_four_acute_angle,
            list_pattern_V_three_obtuse_angle,
            list_pattern_V_three_acute_angle,
            list_pattern_V_three_obtuse_angle_central_one,
            list_pattern_V_three_acute_angle_central_one,
            list_pattern_V_four_obtuse_angle_central_one,
            list_pattern_V_four_acute_angle_central_one]


if __name__ == '__main__':

    list_12800_points = []
    list_6400_points = []
    list_3200_points = []
    list_1600_points = []
    list_800_points = []
    list_400_points = []
    list_200_points = []

    index = 0
    for list in generation_pattern_by_five():
        for pattern in list:
            if index == 0:
                list_12800_points.append(pattern)
            elif index == 1 or index == 2:
                if pattern.count(1) == 4:
                    list_1600_points.append(pattern)
                else:
                    list_400_points.append(pattern)
            else:
                list_1600_points.append(pattern)
        index = index + 1

    index = 0
    for list in generation_pattern_by_six():
        for pattern in list:
            if index == 0:
                list_12800_points.append(pattern)
            elif index == 1:
                if pattern.count(1) == 4:
                    if pattern[0] == 0 and pattern[5] == 0:
                        list_6400_points.append(pattern)
                    else:
                        list_1600_points.append(pattern)
                else:
                    if not pattern.__contains__(2) and pattern[5] == 0:
                        list_800_points.append(pattern)
                    else:
                        list_400_points.append(pattern)
            elif index == 2:
                if pattern.count(1) == 4:
                    if pattern[0] == 0 and pattern[5] == 0:
                        list_6400_points.append(pattern)
                    else:
                        list_1600_points.append(pattern)
                else:
                    if not pattern.__contains__(2) and pattern[0] == 0:
                        list_800_points.append(pattern)
                    else:
                        list_400_points.append(pattern)
            else:
                list_1600_points.append(pattern)
        index = index + 1

    index = 0
    for list in generation_pattern_by_seven():
        for pattern in list:
            if index == 0:
                list_12800_points.append(pattern)
            elif index == 1:
                if pattern.count(1) == 4:
                    if pattern[6] == 0:
                        list_6400_points.append(pattern)
                    else:
                        list_1600_points.append(pattern)
                else:
                    if pattern[6] == 0:
                        list_800_points.append(pattern)
                    else:
                        list_400_points.append(pattern)
            elif index == 2:
                if pattern.count(1) == 4:
                    if pattern[0] == 0:
                        list_6400_points.append(pattern)
                    else:
                        list_1600_points.append(pattern)
                else:
                    if pattern[0] == 0:
                        list_800_points.append(pattern)
                    else:
                        list_400_points.append(pattern)
            else:
                list_1600_points.append(pattern)
        index = index + 1

    index = 0
    for list in generation_special_pattern():
        for pattern in list:
            if index == 0:
                list_1600_points.append(pattern)
            elif index == 1:
                list_1600_points.append(pattern)
            elif index == 2:
                list_3200_points.append(pattern)
            elif index == 3:
                list_3200_points.append(pattern)
            elif index == 4:
                list_6400_points.append(pattern)
            elif index == 5:
                list_6400_points.append(pattern)
            elif index == 6:
                list_12800_points.append(pattern)
            elif index == 7:
                list_12800_points.append(pattern)
        index = index + 1

    index = 0
    for list in [list_12800_points,
                 list_6400_points,
                 list_3200_points,
                 list_1600_points,
                 list_800_points,
                 list_400_points]:
        print()

        if index == 0:
            print("list_12800_points (HAI VINTO):")
        elif index == 1:
            print("list_6400_points (UNA MOSSA PER VINCERE MA PIU' POSSIBILITA'):")
        elif index == 2:
            print("list_3200_points (DUE MOSSE PER VINCERE MA CASI SPECIALI):")
        elif index == 3:
            print("list_1600_points (UNA MOSSA PER VINCERE E UNA SOLA POSSIBILITA'):")
        elif index == 4:
            print("list_800_points: (DUE MOSSE PER VINCERE PIU' SAFE)")
        else:
            print("list_400_points: (DUE MOSSE PER VINCERE MENO SAFE)")

        print()

        for l in list:
            print(l)
            print()

        print("/----------------------/")

        index = index + 1