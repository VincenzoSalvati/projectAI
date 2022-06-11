import csv


def read_csv_player_vs_pc():
    with open('./log/Player_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def read_csv_pc_vs_pc():
    with open('./log/PC_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def write_csv_player_vs_pc(row):
    with open('./log/Player_VS_PC.csv', 'a+', newline='') as player_vs_pc_file:
        writer = csv.writer(player_vs_pc_file)
        if not read_csv_player_vs_pc():
            writer.writerow(['Bot main heuristic', 'Bot mean elapsed time', 'Bot win',
                             'Tie', 'Match elapsed time', 'Number moves'])
        writer.writerow(row)


def write_csv_pc_vs_pc(row):
    with open('./log/PC_VS_PC.csv', 'a+', newline='') as pc_vs_pc_file:
        writer = csv.writer(pc_vs_pc_file)
        if not read_csv_pc_vs_pc():
            writer.writerow(
                ['1° bot main heuristic', '1° bot mean elapsed time', '1° bot win',
                 '2° bot main heuristic', '2° bot mean elapsed time', '2° bot win',
                 'Tie', 'Match elapsed time', 'Number moves'])
        writer.writerow(row)

# def extract_sub_arrays(a, L, S=1):  # Window len = L, Stride len/step_size = S
#     a = np.array(a)
#     number_rows = ((a.size - L) // S) + 1
#     n = a.strides[0]
#     return np.lib.stride_tricks.as_strided(a, shape=(number_rows, L), strides=(S * n, n))
