"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file constants_ai.py


PURPOSE OF THE FILE: ai constants.
"""

PLAYER_BLACK = 1
PLAYER_WHITE = 2

MASKING_ELEMENT = -1

LENGTH_VICTORY = 5

BOT_WEIGHTS_MAIN = {
    "FiveInRow": (27000, 26999),

    "FourInRow": (905, 900),
    "BrokenFour": (905, 900),

    "ThreeInRow": (25, 30),
    "BrokenThree": (25, 30),

    "TwoInRow": (1, .5),
    "BrokenTwo": (1, .5)
}

BOT_WEIGHTS_2 = {
    "FiveInRow": (20, 19),

    "FourInRow": (12, 10),
    "BrokenFour": (12, 10),

    "ThreeInRow": (3, 5),
    "BrokenThree": (3, 5),

    "TwoInRow": (2.5, 1),
    "BrokenTwo": (2.5, 1)
}

WEIGHT_TERMINAL_STATE = 0.8
