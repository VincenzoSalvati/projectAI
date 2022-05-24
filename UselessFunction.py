#Could be cancelled
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


def end(self):
    for i in range(self.size):
        for j in range(self.size):

            # Orizzontale
            if self.board[i][j] == player:
                count_r += 1
                if count_r == 5:
                    self.win()
            else:
                count_r = 0

            # Verticale
            if self.board[j][i] == player:
                count_c += 1
                if count_c == 5:
                    self.win()
            else:
                count_c = 0

            # Diagonale 1
            if i + 5 < self.size and j + 5 < self.size:
                for k in range(5):
                    if self.board[i + k][j + k] == player:
                        count_d1 += 1
                    else:
                        count_d1 = 0
                        break

                if count_d1 == 5:
                    self.win()

            if i + 5 < self.size and j - 5 < self.size:
                for k in range(5):
                    if self.board[i + k][j - k] == player:
                        count_d2 += 1
                    else:
                        count_d2 = 0
                        break

                if count_d2 == 5:
                    self.win()


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


# Other heuristics
def generation_pattern_by_five(self):
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


def generation_pattern_by_six(self):
    # Fetch list of patterns by five
    lists_of_patterns = self.generation_pattern_by_five()

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


def generation_pattern_by_seven(self):
    # Fetch list of patterns by five
    lists_of_patterns = self.generation_pattern_by_five()

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


def generation_special_pattern(self):
    # Obtuse angle
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

    # Acute angle
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

    # List for each rotation of 90 degree
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
        list_pattern_V_three_acute_angle.append(np.flip(pattern_V_three_acute_angle, 1))
        pattern_V_four_acute_angle = np.rot90(pattern_V_four_acute_angle)
        list_pattern_V_four_acute_angle.append(pattern_V_four_acute_angle)
        list_pattern_V_four_acute_angle.append(np.flip(pattern_V_four_acute_angle, 1))

        pattern_V_three_acute_angle_central_one = np.rot90(pattern_V_three_acute_angle_central_one)
        list_pattern_V_three_acute_angle_central_one.append(pattern_V_three_acute_angle_central_one)
        list_pattern_V_three_acute_angle_central_one.append(np.flip(pattern_V_three_acute_angle_central_one, -1))
        pattern_V_four_acute_angle_central_one = np.rot90(pattern_V_four_acute_angle_central_one)
        list_pattern_V_four_acute_angle_central_one.append(pattern_V_four_acute_angle_central_one)
        list_pattern_V_four_acute_angle_central_one.append(np.flip(pattern_V_four_acute_angle_central_one, -1))

    return [list_pattern_V_four_obtuse_angle,
            list_pattern_V_four_acute_angle,
            list_pattern_V_three_obtuse_angle,
            list_pattern_V_three_acute_angle,
            list_pattern_V_three_obtuse_angle_central_one,
            list_pattern_V_three_acute_angle_central_one,
            list_pattern_V_four_obtuse_angle_central_one,
            list_pattern_V_four_acute_angle_central_one]


def list_of_pattern_per_score(self):
    list_12800_points = []
    list_6400_points = []
    list_3200_points = []
    list_1600_points = []
    list_800_points = []
    list_400_points = []

    index = 0
    for list in self.generation_pattern_by_five():
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
    for list in self.generation_pattern_by_six():
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
    for list in self.generation_pattern_by_seven():
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
    for list in self.generation_special_pattern():
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

    return [list_12800_points,
            list_6400_points,
            list_3200_points,
            list_1600_points,
            list_800_points,
            list_400_points]
