"""
Course: Artificial Intelligence 2021/2022

Lecturer:
Marcelli      Angelo      amarcelli@unisa.it
Della Cioppa  Antonio     adellacioppa@unisa.it

Group:
Salvati       Vincenzo    0622701550      v.salvati10@studenti.unisa.it
Mansi         Paolo       0622701542      p.mansi5@studenti.unisa.it

@file ButtonHome.py


PURPOSE OF THE FILE: deal with home's button.
"""

import pygame


class ButtonHome:
    """Object ButtonHome

    Attributes:
        top_rect (obj python): top rectangle
        top_color (string): color of top rectangle

        bottom_rect (obj python): bottom rectangle
        bottom_color (string): color of bottom rectangle

        text (string): button's text
        text_surf (obj pygame): text' font
        text_rect (obj pygame): text rectangle

        elevation (float): button's elevation
        position (Tuple[int, int]): button's position
        pressed (bool): button pressed
    """

    def __init__(self, position, dimension, text, gui_font, elevation):
        """Init button

        Args:
            position (Tuple[int, int]): button's position
            dimension (Tuple[int, int]): button's dimension

            text (string): button's text
            gui_font (obj pygame): text' font

            elevation (float): button's elevation
        """
        # Top rectangle
        self.top_rect = pygame.Rect(position, dimension)
        self.top_color = '#ff8635'

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(position, dimension)
        self.bottom_color = '#7a4019'

        # Text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        # Core attributes
        self.elevation = elevation
        self.position = position
        self.pressed = False

    def draw(self, screen):
        """Draw button

        Args:
            screen (obj pygame): home's window
        """
        # Set elevation
        self.elevation = 5

        # Set top rectangle
        self.top_rect.y = self.position[1] - self.elevation
        self.text_rect.center = self.top_rect.center

        # Set bottom rectangle
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation

        # Draw button
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

        # Check pressed button
        self.check_pass_on()

    def check_pass_on(self):
        """Animation pressed button

        """
        # Init parameter
        mouse_pos = pygame.mouse.get_pos()

        # Button animation
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#af5c25'
        else:
            self.top_color = '#ff8635'

    def check_click(self):
        """Animation clicked button

        """
        # Init parameter
        mouse_pos = pygame.mouse.get_pos()

        # Button animation
        if self.top_rect.collidepoint(mouse_pos):
            self.elevation = 0
            self.pressed = not self.pressed
