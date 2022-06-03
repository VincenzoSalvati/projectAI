import os

import pygame

from graphics.BoardGomoku import init_home_gomoku

if __name__ == '__main__':
    pygame.init()

    if not os.path.exists("./log"):
        os.mkdir("./log")

    init_home_gomoku()
