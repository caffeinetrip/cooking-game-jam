import pygame
import scripts.pygpen as pp

class DialogueCharacter:
    def __init__(self, sprite_path, position, p, sprite_size=(64, 64)):
        self.base_sprite_path = sprite_path
        self.position = position
        self.sprite_size = sprite_size
        self.p = p
        self.sprite = None
        self.current_emotion = 'default'
        self.load_sprite('default')
        
    def load_sprite(self, emotion='default'):
        if emotion == 'default':
            path = self.base_sprite_path
        else:
            base_path = self.base_sprite_path.rsplit('.', 1)[0]
            ext = self.base_sprite_path.rsplit('.', 1)[1]
            path = f"{base_path}_{emotion}.{ext}"
        
        try:
            self.sprite = pygame.image.load(path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, self.sprite_size)
            self.current_emotion = emotion
        except:
            if emotion != 'default':
                self.load_sprite('default')

class DialogueSystem(pp.ElementSingleton):
    def __init__(self):
        super().__init__()
        
        self.active = False
        self.current_dialogue = None
        self.current_index = 0
        self.current_text = ""
        self.full_text = ""
        self.char_index = 0
        self.char_timer = 0
        self.char_speed = 0.03
        self.text_finished = False
        self.auto_advance = False
        self.auto_advance_delay = 0.25
        self.auto_advance_timer = 0
        
        self.punctuation_pause = {
            '.': 0.15,
            '!': 0.15,
            '?': 0.15,
            ',': 0.08,
            ';': 0.08,
            ':': 0.08,
            '-': 0.05
        }
        self.space_speedup = 0.7
        
        self.characters = {}
        self.current_character = None
        
        self.box_left = pygame.image.load('data/images/hud/left_dialogue_bar.png')
        self.box_right = pygame.image.load('data/images/hud/right_dialogue_bar.png')
        
        self.dialogue_data = {}
        
        self.font = None
        
    def register_character(self, character_id, sprite_path, position, p, sprite_size=(64, 64)):
        self.characters[character_id] = DialogueCharacter(sprite_path, position, p, sprite_size)
    
    def load_dialogues(self, dialogues_dict):
        self.dialogue_data = dialogues_dict
    
    def start_dialogue(self, dialogue_id):
        if dialogue_id not in self.dialogue_data:
            return
                
        for group_name, group in self.e['EntityGroups'].groups.items():
            for item in list(group):
                if hasattr(item, 'food_type'):
                    item.kill()

        self.e['Game'].load_activities()
        self.e['NPCPlacement'].reset_all_npcs()
        
        if dialogue_id == 'miss_dish':
            self.char_speed = 0.1
        else: 
            self.char_speed = 0.03
        
        language = self.e['Settings'].language
        self.current_dialogue = self.dialogue_data[dialogue_id][language]
        self.current_index = 0
        self.active = True
        self.e['State'].gameplay_stop = True
        self.e['State'].show_hud = False
        
        self._load_current_line()
    
    def _load_current_line(self):
        if self.current_index >= len(self.current_dialogue):
            self.stop_dialogue()
            return
        
        line_data = self.current_dialogue[self.current_index]
        
        if len(line_data) == 3:
            character_id, text, emotion = line_data
        else:
            character_id, text = line_data
            emotion = 'default'
        
        self.current_character = self.characters.get(character_id, None)
        
        if self.current_character:
            self.current_character.load_sprite(emotion)
        
        self.auto_advance = text.startswith('*')
        if self.auto_advance:
            text = text[1:]
        
        if self.font and self.current_character:
            line_width = 149 if self.current_character.p == 'left' else 147
            prepped = self.font.prep_text(text, line_width=line_width)
            self.full_text = prepped.text
        else:
            self.full_text = text
            
        self.current_text = ""
        self.char_index = 0
        self.text_finished = False
        self.char_timer = 0
        self.auto_advance_timer = 0
    
    def stop_dialogue(self):
        def _stop():
            dialogue_id = None
            if self.current_dialogue:
                for key, value in self.dialogue_data.items():
                    if value.get(self.e['Settings'].language) == self.current_dialogue:
                        dialogue_id = key
                        break
            
            self.active = False
            self.current_dialogue = None
            self.current_index = 0
            self.current_text = ""
            self.full_text = ""
            self.char_index = 0
            self.text_finished = False
            self.current_character = None
            self.e['State'].gameplay_stop = False
            self.e['State'].show_hud = True
            
            if isinstance(self.e['State'].act, int):
                if self.e['State'].act == 4:
                    self.e['State'].act = 5
                    self.e['State'].dayt = 1
                    self.e['State'].week = 1
                    
                    for group_name, group in self.e['EntityGroups'].groups.items():
                        for item in list(group):
                            if hasattr(item, 'food_type'):
                                item.kill()
                        
                    self.e['Game'].load_activities()
                    self.e['NPCPlacement'].reset_all_npcs()
                    self.e['NPCPlacement'].stop_spawning = False
                    
                    
                elif self.e['State'].act == 7:
                    self.e['State'].act = 8
                    
                    for group_name, group in self.e['EntityGroups'].groups.items():
                        for item in list(group):
                            if hasattr(item, 'food_type'):
                                item.kill()
                        
                    self.e['Game'].load_activities()
                    self.e['NPCPlacement'].reset_all_npcs()
                    self.e['NPCPlacement'].stop_spawning = False
        
        self.e['Transition'].transition(_stop)
                
    def skip_typing(self):
        self.current_text = self.full_text
        self.char_index = len(self.full_text)
        self.text_finished = True
    
    def next_line(self):
        if not self.text_finished:
            self.skip_typing()
        else:
            self.current_index += 1
            self.char_timer = 0
            self._load_current_line()
    
    def _get_char_delay(self, char):
        if char == ' ':
            return self.char_speed * self.space_speedup
        elif char in self.punctuation_pause:
            return self.char_speed + self.punctuation_pause[char]
        else:
            return self.char_speed
    
    def update(self, dt):
        if not self.active:
            return
        
        if not self.font:
            self.font = self.e['Text']['font']
            if self.full_text and self.current_character:
                line_width = 149 if self.current_character.p == 'left' else 147
                prepped = self.font.prep_text(self.full_text, line_width=line_width)
                self.full_text = prepped.text
        
        if self.e['Input'].pressed('left_click') or self.e['Input'].pressed('test'):
            self.next_line()
            return
        
        if not self.text_finished:
            self.char_timer += dt
            
            while self.char_index < len(self.full_text):
                current_char = self.full_text[self.char_index]
                char_delay = self._get_char_delay(current_char)
                
                if self.char_timer >= char_delay:
                    self.current_text += current_char
                    self.char_index += 1
                    self.char_timer -= char_delay
                    
                    if self.char_index >= len(self.full_text):
                        self.text_finished = True
                        break
                else:
                    break
        
        if self.text_finished and self.auto_advance:
            self.auto_advance_timer += dt
            if self.auto_advance_timer >= self.auto_advance_delay:
                self.next_line()
    
    def render(self, surf):
        if not self.active or not self.current_character:
            return
        
        surf.blit(self.current_character.sprite, self.current_character.position)
        
        if self.current_character.p == 'left':
            box = self.box_left
            text_pos = (99, 172)
        else:
            box = self.box_right 
            text_pos = (98, 173)
        
        surf.blit(box, (0, 0))
        
        if self.font:
            self.font.render(surf, self.current_text, text_pos, color=(255, 255, 255))