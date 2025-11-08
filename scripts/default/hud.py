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
        
        self.font = self.e['Text']['font']
        
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
            
            self.font.render(surf, f'Week: {self.e['State'].week}', (180, 5), color=(255, 255, 255))
            self.font.render(surf, f'{self.e['State'].day}', (340, 120), color=(255, 255, 255))