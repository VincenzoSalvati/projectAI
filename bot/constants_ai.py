"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file constants_graphics.py


PURPOSE OF THE FILE: bot constants.
"""

PLAYER_BLACK = 1
PLAYER_WHITE = 2

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
    "FiveInRow": (20, 20),

    "FourInRow": (9, 7),
    "BrokenFour": (9, 7),

    "ThreeInRow": (2, 5),
    "BrokenThree": (2, 5),

    "TwoInRow": (1, .5),
    "BrokenTwo": (1, .5)
}
