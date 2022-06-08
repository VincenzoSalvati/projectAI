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
        csvwriter = csv.writer(player_vs_pc_file)
        if not read_csv_player_vs_pc():
            csvwriter.writerow(['Bot main heuristic', 'Bot mean elapsed time', 'Bot win',
                                'Tie', 'Match elapsed time'])
        csvwriter.writerow(row)


def write_csv_pc_vs_pc(row):
    with open('./log/PC_VS_PC.csv', 'a+', newline='') as pc_vs_pc_file:
        csvwriter = csv.writer(pc_vs_pc_file)
        if not read_csv_pc_vs_pc():
            csvwriter.writerow(
                ['1° bot main heuristic', '1° bot mean elapsed time', '1° bot win',
                 '2° bot main heuristic', '2° bot mean elapsed time', '2° bot win',
                 'Tie', 'Match elapsed time'])
        csvwriter.writerow(row)

