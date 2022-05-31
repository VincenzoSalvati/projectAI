import pygame


# noinspection SpellCheckingInspection
class ButtonHome:
    def __init__(self, gui_font, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_election = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#ff8635'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#7a4019'
        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def change_text(self, gui_font, new_text):
        self.text_surf = gui_font.render(new_text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_election
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_election

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_pass_on()
        self.dynamic_election = 5

    def check_pass_on(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#af5c25'
        else:
            self.top_color = '#ff8635'

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.dynamic_election = 0
            self.pressed = not self.pressed
