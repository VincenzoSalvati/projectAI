"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file utils.py


PURPOSE OF THE FILE: useful function.
"""

import csv


def read_csv_player_vs_pc():
    """Read Player_VS_PC.csv

    """
    with open('./log/Player_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def read_csv_pc_vs_pc():
    """Read PC_VS_PC.csv

    """
    with open('./log/PC_VS_PC.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for _ in csv_reader:
            return True
        return False


def write_csv_player_vs_pc(row):
    """Write Player_VS_PC.csv

    Args:
        row (List[bool, float, bool, bool, float, int]): data to be written
    """
    with open('./log/Player_VS_PC.csv', 'a+', newline='') as player_vs_pc_file:
        writer = csv.writer(player_vs_pc_file)
        if not read_csv_player_vs_pc():
            writer.writerow(['Bot main heuristic', 'Bot mean elapsed time', 'Bot win',
                             'Tie', 'Match elapsed time', 'Number moves'])
        writer.writerow(row)


def write_csv_pc_vs_pc(row):
    """Write PC_VS_PC.csv

    Args:
        row (List[bool, float, bool, bool, float, bool, bool, float, int]): data to be written
    """
    with open('./log/PC_VS_PC.csv', 'a+', newline='') as pc_vs_pc_file:
        writer = csv.writer(pc_vs_pc_file)
        if not read_csv_pc_vs_pc():
            writer.writerow(
                ['1° bot main heuristic', '1° bot mean elapsed time', '1° bot win',
                 '2° bot main heuristic', '2° bot mean elapsed time', '2° bot win',
                 'Tie', 'Match elapsed time', 'Number moves'])
        writer.writerow(row)
