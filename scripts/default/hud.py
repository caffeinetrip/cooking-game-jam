import pygame
from scripts import pygpen as pp

class HUD(pp.ElementSingleton):
    def __init__(self):
        super().__init__()
        self.scrap_spin = 0
        self.flash = 0
        self.swap_offset = 0
        
        self.e['DialogueSystem'].register_character('grandmother', 'data/images/hud/saya.png', (0, 0), 'right', (384, 216))
        self.e['DialogueSystem'].register_character('akiko', 'data/images/hud/sen.png', (0, 0), 'left', (384, 216))
                
        self.heart_hud = pygame.image.load('data/images/hud/heart.png')
        self.points_hud = pygame.image.load('data/images/hud/points.png')
        
        self.font = self.e['Text']['font']
        
        if self.e['State'].act == 0:
            self.e['DialogueSystem'].start_dialogue('intro')

    def render(self, surf):
        
        if self.e['State'].show_hud:
            self.swap_offset += -self.swap_offset * self.e['Window'].dt * 10
            if self.swap_offset < 0.5:
                self.swap_offset = 0
            
            for i in range(self.e['State'].health):
                surf.blit(self.heart_hud, (2 + (i*7), 2))
            
            for i in range(self.e['State'].points):
                surf.blit(self.points_hud, (370, 2 + (i*7)))
            
            self.font.render(surf, f'Week: {self.e['State'].week}', (180, 5), color=(255, 255, 255))
            self.font.render(surf, f'{self.e['State'].day}', (340, 120), color=(255, 255, 255))
        
        if self.e['State'].act == 1 and self.e['State'].dialogue_count == 1:
            self.e['DialogueSystem'].start_dialogue('act1')
            self.e['State'].dialogue_count += 1
        
        if self.e['State'].act == 2 and self.e['State'].dialogue_count == 2:
            self.e['DialogueSystem'].start_dialogue('act2')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 3 and self.e['State'].dialogue_count == 3:
            self.e['DialogueSystem'].start_dialogue('guide_complete')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 'miss_dish':
            self.e['DialogueSystem'].start_dialogue('miss_dish')
            self.e['State'].act = self.e['State'].dialogue_count - 1
            self.e['EntityGroups'].groups['food'] = []