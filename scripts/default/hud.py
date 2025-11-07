import math

import pygame

from scripts import pygpen as pp

class HUD(pp.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.scrap_spin = 0
        self.flash = 0

        self.swap_offset = 0

        self.hide_ui = False
        
        self.heart_hud = pygame.image.load('data/images/hud/heart.png')
        self.points_hud = pygame.image.load('data/images/hud/points.png')
        
    def update(self):
        if self.e['Input'].pressed('hide_ui'):
            self.hide_ui = not self.hide_ui

    def render(self, surf):
        if not self.hide_ui:

            self.swap_offset += -self.swap_offset * self.e['Window'].dt * 10
            if self.swap_offset < 0.5:
                self.swap_offset = 0

            for i in range(self.e['State'].health):
                surf.blit(self.heart_hud, (2 + (i*7), 2))

            for i in range(self.e['State'].points):
                surf.blit(self.points_hud, (370, 2 + (i*7)))
                
            # self.flash = max(0, self.flash - self.e['Window'].dt * 4)
            # if self.flash:
            #     white = pygame.Surface(self.e['Game'].display.get_size())
            #     white.fill((254, 252, 211))
            #     white.set_alpha(int(min(1, self.flash) * 255))
            #     self.e['Renderer'].blit(white, (0, 0), z=10011, group='ui')