import pygame
import random
from scripts import pygpen as pp
from scripts.default.const import BUFFS, dialogues, GAME_OVER_TEXTS, KNIFE_WARNING

class HUD(pp.ElementSingleton):
    def __init__(self):
        super().__init__()
        self.scrap_spin = 0
        self.flash = 0
        self.swap_offset = 0
        
        self.e['DialogueSystem'].register_character('grandmother', 'data/images/hud/saya.png', (0, 0), 'right', (384, 216))
        self.e['DialogueSystem'].register_character('akiko', 'data/images/hud/sen.png', (0, 0), 'left', (384, 216))
        self.e['DialogueSystem'].register_character('kazu', 'data/images/hud/kazu.png', (0, 0), 'right', (384, 216))
        self.e['DialogueSystem'].register_character('yuki', 'data/images/hud/yuki.png', (0, 0), 'right', (384, 216))
        
        self.heart_hud = pygame.image.load('data/images/hud/heart.png')
        self.points_hud = pygame.image.load('data/images/hud/points.png')
        self.card_img = pygame.image.load('data/images/hud/card.png')
        
        try:
            self.hearts_unlocked_img = pygame.image.load('data/images/hud/hearts.png')
        except:
            self.hearts_unlocked_img = None
        
        self.font = self.e['Text']['font']
        self.small_font = self.e['Text']['small_font']
        
        self.buff_boxes = [
            pygame.Rect(42, 58, 90, 140),
            pygame.Rect(147, 58, 90, 140),
            pygame.Rect(252, 58, 90, 140)
        ]
        
        self.intro_text = ""
        self.intro_char_index = 0
        self.intro_timer = 0.0
        self.intro_char_speed = 0.05
        self.intro_full_text = ""
        self.intro_finished = False
        
        self.current_buff_options = []
        self.buff_selection_freeze = False
        
        self.game_over_text = ""
        
        self.knife_warning_text = ""
        self.knife_warning_alpha = 0
        self.knife_warning_timer = 0.0
        
        self.end_game_timer = 0.0
        self.end_game_text = ""
        
    def show_knife_warning(self):
        language = self.e['Settings'].language
        self.knife_warning_text = KNIFE_WARNING[language]
        self.knife_warning_alpha = 255
        self.knife_warning_timer = 3.0
        
    def start_intro_text(self, text_key):
        language = self.e['Settings'].language
        self.intro_full_text = dialogues[text_key][language]
        self.intro_text = ""
        self.intro_char_index = 0
        self.intro_timer = 0.0
        self.intro_finished = False
        
    def update_intro_text(self, dt):
        if self.intro_finished:
            return True
            
        self.intro_timer += dt
        
        while self.intro_char_index < len(self.intro_full_text):
            if self.intro_timer >= self.intro_char_speed:
                self.intro_text += self.intro_full_text[self.intro_char_index]
                self.intro_char_index += 1
                self.intro_timer -= self.intro_char_speed
                
                if self.intro_char_index >= len(self.intro_full_text):
                    self.intro_finished = True
                    return True
            else:
                break
        return False
    
    def generate_buff_options(self):
        self.current_buff_options = []
        
        available_gameplay = [b for b in self.e['State'].available_gameplay_buffs 
                            if b['id'] not in self.e['State'].selected_buffs or b['repeatable']]
        available_lore = [b for b in self.e['State'].available_lore_buffs 
                         if b['id'] not in self.e['State'].selected_buffs]
        
        repeatable_gameplay = [b for b in BUFFS if b['type'] == 'gameplay' and b['repeatable']]
        
        if len(available_gameplay) > 0:
            self.current_buff_options.append(random.choice(available_gameplay))
        elif len(repeatable_gameplay) > 0:
            self.current_buff_options.append(random.choice(repeatable_gameplay))
            
        if len(available_gameplay) > 1:
            second = random.choice([b for b in available_gameplay if b != self.current_buff_options[0]])
            self.current_buff_options.append(second)
        elif len(repeatable_gameplay) > 0:
            self.current_buff_options.append(random.choice(repeatable_gameplay))
        elif len(available_lore) > 0:
            self.current_buff_options.append(random.choice(available_lore))
            
        if len(self.current_buff_options) < 3:
            remaining = [b for b in available_lore if b not in self.current_buff_options]
            if len(remaining) > 0:
                self.current_buff_options.append(random.choice(remaining))
                
        while len(self.current_buff_options) < 3:
            all_available = available_gameplay + available_lore + repeatable_gameplay
            if len(all_available) > 0:
                choice = random.choice([b for b in all_available if b not in self.current_buff_options])
                self.current_buff_options.append(choice)
            else:
                break
    
    def render(self, surf, ui_surf):

        if self.e['State'].has_heart and self.hearts_unlocked_img:
            surf.blit(self.hearts_unlocked_img, (20,138))

        if self.e['State'].h_scene:
            surf.fill((0, 0, 0))
            
            if not self.end_game_text:
                language = self.e['Settings'].language
                if language == 'russian':
                    self.end_game_text = "СПАСИБО ЗА ИГРУ"
                else:
                    self.end_game_text = "THANKS FOR PLAYING"
            
            text_width = self.font.width(self.end_game_text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() // 2
            self.font.render(surf, self.end_game_text, (x, y), color=(255, 255, 255))
            
            subtitle = "GAME CREATED BY SOMA" if self.e['Settings'].language == 'english' else "ИГРУ СОЗДАЛ SOMA"
            subtitle_width = self.font.width(subtitle)
            self.font.render(surf, subtitle, ((surf.get_width() - subtitle_width) // 2, y + 30), color=(200, 200, 200))
            
            if self.e['Input'].pressed('left_click'):
                import sys
                sys.exit()
            return
            
        if self.e['State'].game_over:
            self.e['NPCPlacement'].reset_all_npcs()
            for group_name, group in self.e['EntityGroups'].groups.items():
                for item in list(group):
                    if hasattr(item, 'food_type'):
                        item.kill()
                        
            surf.fill((0, 0, 0))
            
            
            if not self.game_over_text:
                language = self.e['Settings'].language
                self.game_over_text = random.choice(GAME_OVER_TEXTS[language])
            
            text_width = self.font.width(self.game_over_text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() // 2
            self.font.render(surf, self.game_over_text, (x, y), color=(255, 255, 255))
            
            restart_text = "Click to restart" if self.e['Settings'].language == 'english' else "Нажмите для перезапуска"
            restart_width = self.font.width(restart_text)
            self.font.render(surf, restart_text, ((surf.get_width() - restart_width) // 2, y + 20), color=(200, 200, 200))
            
            if self.e['Input'].pressed('left_click'):
                

                self.e['State'].restart_from_death()
                self.game_over_text = ""
                
                self.e['Game'].load_activities()
                self.e['NPCPlacement'].reset_all_npcs()
                self.e['NPCPlacement'].stop_spawning = False
            return
        
        if self.e['State'].act == -2:
            surf.fill((0, 0, 0))
            if self.intro_full_text == "":
                self.start_intro_text('creator')
            self.update_intro_text(self.e['Window'].dt)
            text_width = self.font.width(self.intro_text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() // 2
            self.font.render(surf, self.intro_text, (x, y), color=(255, 255, 255))
            return
            
        if self.e['State'].act == -1:
            surf.fill((0, 0, 0))
            if self.intro_full_text == "" or self.intro_full_text == dialogues['creator'][self.e['Settings'].language]:
                self.start_intro_text('disclaimer')
            self.update_intro_text(self.e['Window'].dt)
            text_width = self.font.width(self.intro_text)
            x = (surf.get_width() - text_width) // 2
            y = surf.get_height() - 30
            self.font.render(surf, self.intro_text, (x, y), color=(255, 255, 255))
            
            if self.intro_finished:
                if self.e['Input'].pressed('left_click') or self.e['Input'].pressed('test'):
                    pass
            return
        
        if self.e['State'].show_buff_selection:
            if not self.buff_selection_freeze:
                for food in self.e['EntityGroups'].groups.get('food', []):
                    food.kill()
                self.e['NPCPlacement'].reset_all_npcs()

            self.e['State'].gameplay_stop = True
            
            if len(self.current_buff_options) == 0:
                self.generate_buff_options()
        
            pygame.draw.rect(surf, (20, 20, 20, 200), (0, 0, surf.get_width(), surf.get_height()))

            language = self.e['Settings'].language
            title = "ВЫБЕРИТЕ КАРТУ" if language == 'russian' else "SELECT YOUR CARD"
            title_width = self.font.width(title)
            self.font.render(surf, title, ((surf.get_width() - title_width) // 2, 30), color=(255, 255, 255))
            
            for i, buff in enumerate(self.current_buff_options):
                box = self.buff_boxes[i]
                
                surf.blit(self.card_img, (box.x, box.y))
                
                if not self.buff_selection_freeze:
                    mpos = self.e['Game'].mpos
                    if box.collidepoint(mpos):
                        pygame.draw.rect(surf, (255, 255, 255), box, 3)
                        
                        if self.e['Input'].pressed('left_click'):
                            buff_id = buff['id']
                            
                            if not buff['repeatable'] and buff['id'] not in self.e['State'].selected_buffs:
                                self.e['State'].selected_buffs.append(buff_id)
                                if buff['type'] == 'gameplay':
                                    self.e['State'].available_gameplay_buffs.remove(buff)
                                else:
                                    self.e['State'].available_lore_buffs.remove(buff)
                            
                            self.e['State'].apply_buff(buff_id)
                            
                            self.buff_selection_freeze = True
                            
                            if self.e['State'].act == 4:

                                self.e['Transition'].transition(lambda: (
                                    self.e['State'].__setattr__('show_buff_selection', False),
                                    self.e['State'].__setattr__('gameplay_stop', False),
                                    setattr(self, 'buff_selection_freeze', False),
                                    setattr(self, 'current_buff_options', []),
                                    self.e['Game'].load_activities(),
                                    self.e['NPCPlacement'].reset_all_npcs(),
                                    self.e['NPCPlacement'].__setattr__('stop_spawning', False),
                                    self.e['DialogueSystem'].start_dialogue('kazu_knife')
                                ))
                            
                            elif self.e['State'].act == 6:

                                self.e['Transition'].transition(lambda: (
                                    self.e['State'].__setattr__('show_buff_selection', False),
                                    setattr(self, 'buff_selection_freeze', False),
                                    setattr(self, 'current_buff_options', []),
                                    self.e['DialogueSystem'].start_dialogue('act7')
                                ))
                                
                            elif self.e['State'].act == 9:

                                self.e['Transition'].transition(lambda: (
                                    self.e['State'].__setattr__('show_buff_selection', False),
                                    setattr(self, 'buff_selection_freeze', False),
                                    setattr(self, 'current_buff_options', []),
                                    self.e['DialogueSystem'].start_dialogue('act10')
                                ))
                            
                            else:

                                self.e['Transition'].transition(lambda: (
                                    self.e['State'].__setattr__('show_buff_selection', False),
                                    self.e['State'].__setattr__('gameplay_stop', False),
                                    setattr(self, 'buff_selection_freeze', False),
                                    setattr(self, 'current_buff_options', []),
                                    self.e['Game'].load_activities(),
                                    self.e['NPCPlacement'].reset_all_npcs(),
                                    self.e['NPCPlacement'].__setattr__('stop_spawning', False)
                                ))
                                
                
                buff_name = buff['name'][language]
                buff_desc = buff['description'][language]
                
                name_y = box.centery - 20
                words = buff_name.split()
                if len(words) > 2:
                    line1 = ' '.join(words[:2])
                    line2 = ' '.join(words[2:])
                    name_width1 = self.font.width(line1)
                    name_width2 = self.font.width(line2)
                    self.font.render(surf, line1, (box.centerx - name_width1 // 2, name_y), color=(255, 255, 255))
                    self.font.render(surf, line2, (box.centerx - name_width2 // 2, name_y + 10), color=(255, 255, 255))
                else:
                    name_width = self.font.width(buff_name)
                    self.font.render(surf, buff_name, (box.centerx - name_width // 2, name_y), color=(255, 255, 255))
                
                desc_words = buff_desc.split()
                lines = []
                current_line = []
                for word in desc_words:
                    test_line = ' '.join(current_line + [word])
                    if self.font.width(test_line) <= box.width - 10:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))
                
                desc_y = box.centery + 10
                for line in lines[:3]:
                    line_width = self.font.width(line)
                    self.font.render(surf, line, (box.centerx - line_width // 2, desc_y), color=(200, 200, 200))
                    desc_y += 10
                               
            return
               
        elif self.e['State'].act == 1 and self.e['State'].dialogue_count == 1:
            self.e['Transition'].transition(lambda: self.e['DialogueSystem'].start_dialogue('act1'))
            self.e['State'].dialogue_count += 1
            
        elif self.e['State'].act == 2 and self.e['State'].dialogue_count == 2:
            self.e['Transition'].transition(lambda: self.e['DialogueSystem'].start_dialogue('act2'))
            self.e['State'].dialogue_count += 1
            
        elif self.e['State'].act == 3 and self.e['State'].dialogue_count == 3:
            self.e['Transition'].transition(lambda: self.e['DialogueSystem'].start_dialogue('guide_complete'))
            self.e['State'].dialogue_count += 1
            self.e['State'].dayt = 1
            self.e['State'].week = 1
            
        elif self.e['State'].act == 'miss_dish':
            self.e['Transition'].transition(lambda: (
                self.e['DialogueSystem'].start_dialogue('miss_dish'),
                self.e['State'].__setattr__('act', self.e['State'].dialogue_count - 1)
            ))
            self.e['EntityGroups'].groups['food'] = []
    
        elif self.e['State'].show_hud:
            self.swap_offset += -self.swap_offset * self.e['Window'].dt * 10
            if self.swap_offset < 0.5:
                self.swap_offset = 0
                
            for i in range(self.e['State'].health):
                surf.blit(self.heart_hud, (6 + (i*7), 4))
                
            for i in range(self.e['State'].points):
                surf.blit(self.points_hud, (370, 2 + (i*7)))
                
            self.font.render(surf, f'Week: {self.e['State'].week}', (180, 3), color=(255, 5, 5))
            self.small_font.render(surf, f'{4-self.e['State'].week} weeks until boss', (160, 14), color=(160, 0, 0))
            self.font.render(surf, f'{self.e['State'].day}', (302, 71), color=(180, 5, 5))
        
        if self.knife_warning_timer > 0:
            self.knife_warning_timer -= self.e['Window'].dt
            self.knife_warning_alpha = max(0, int(255 * (self.knife_warning_timer / 3.0)))
            
            warning_surf = pygame.Surface((200, 20))
            warning_surf.fill((0, 0, 0))
            warning_surf.set_alpha(self.knife_warning_alpha)
            
            text_width = self.font.width(self.knife_warning_text)
            self.font.render(warning_surf, self.knife_warning_text, (100 - text_width // 2, 5), color=(255, 10, 10))
            
            warning_surf.set_colorkey((0,0,0))
            
            surf.blit(warning_surf, (85, 130))
    