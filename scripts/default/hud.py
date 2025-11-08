import pygame
from scripts import pygpen as pp
from scripts.default.const import BUFFS

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
        
        self.buff_boxes = [
            pygame.Rect(42, 73, 90, 90),
            pygame.Rect(147, 73, 90, 90),
            pygame.Rect(252, 73, 90, 90)
        ]
        
    def render(self, surf):
        if self.e['State'].act == -2:
            text = "GAME CREATED BY SOMA"
            text_width = self.font.width(text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() // 2
            self.font.render(surf, text, (x, y), color=(255, 255, 255))
            return
            
        if self.e['State'].act == -1:
            language = self.e['Settings'].language
            from scripts.default.const import dialogues
            text = dialogues['disclaimer'][language]
            
            text_width = self.font.width(text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() - 30
            self.font.render(surf, text, (x, y), color=(255, 255, 255))
            return
        
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
            
        if self.e['State'].show_buff_selection:
        
            pygame.draw.rect(surf, (20, 20, 20), (0, 0, surf.get_width(), surf.get_height()))
            print('select')
            title = "SELECT YOUR BUFF"
            title_width = self.font.width(title)
            self.font.render(surf, title, ((surf.get_width() - title_width) // 2, 30), color=(255, 255, 255))
            
            for i, buff in enumerate(BUFFS):
                box = self.buff_boxes[i]
                pygame.draw.rect(surf, (50, 50, 50), box)
                pygame.draw.rect(surf, (100, 100, 100), box, 2)
                
                mpos = self.e['Game'].mpos
                if box.collidepoint(mpos):
                    pygame.draw.rect(surf, (150, 150, 150), box, 3)
                    
                    if self.e['Input'].pressed('left_click'):
                        self.e['State'].selected_buff = buff['id']
                        self.e['State'].show_buff_selection = False
                        self.e['State'].gameplay_stop = False
                        
                        self.handle_buff_selection(buff['id'])
                        
                        if self.e['State'].act == 3:
                            self.e['Transition'].transition(lambda: self.e['State'].__setattr__('act', 5))
                        else:
                            self.e['State'].act += 1
                                            
                            for food in self.e['EntityGroups'].groups['food']:
                                food.kill()
                                
                            self.e['Game'].load_activities()
                            self.e['NPCPlacement'].reset_all_npcs()
                
                name_width = self.font.width(buff['name'])
                self.font.render(surf, buff['name'], 
                               (box.centerx - name_width // 2, box.centery - 10), 
                               color=(255, 255, 255))
                               
            return
            
        if self.e['State'].act == 1 and self.e['State'].dialogue_count == 1:
            self.e['DialogueSystem'].start_dialogue('act1')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 2 and self.e['State'].dialogue_count == 2:
            self.e['DialogueSystem'].start_dialogue('act2')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 3 and self.e['State'].dialogue_count == 3:
            self.e['DialogueSystem'].start_dialogue('guide_complete')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 4 and self.e['State'].dialogue_count == 4:
            self.e['DialogueSystem'].start_dialogue('act4')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 7 and self.e['State'].dialogue_count == 5:
            self.e['DialogueSystem'].start_dialogue('act7')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 10 and self.e['State'].dialogue_count == 6:
            self.e['DialogueSystem'].start_dialogue('act10')
            self.e['State'].dialogue_count += 1
            
        if self.e['State'].act == 'miss_dish':
            self.e['DialogueSystem'].start_dialogue('miss_dish')
            self.e['State'].act = self.e['State'].dialogue_count - 1
            self.e['EntityGroups'].groups['food'] = []
    
    def handle_buff_selection(self, buff_id):
        if buff_id == 'buff1':
            pass
        elif buff_id == 'buff2':
            pass
        elif buff_id == 'buff3':
            pass