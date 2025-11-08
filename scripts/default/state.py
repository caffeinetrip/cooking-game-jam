import math
import random
import pygame
import scripts.pygpen as pp
from scripts.default.const import DEFAULT_SAVE

EFFECTS = {
    'todo': 0
}

class State(pp.ElementSingleton):
    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        self.reset()
        self.playable = True
        self.kill_streak = 0
        self.health = 7
        self.time = 0
        self.week = 1   
        self.dayt = 1
        self.day = ''
        self.hour = 0
        self.minute = 0
        self.points = 0
        self.time_speed = 100
        self.scene = ""
        self.gameplay_stop = False
        self.show_hud = True
        self.dialogue = False
        self.dialogue_count = 1
        self.act = -2
        self.act_complete = False
        self.boss_defeated = False
        self.show_buff_selection = False
        self.selected_buff = None
        self.intro_timer = 0.0
        self.disclaimer_shown = False
        self.last_act_change_week = 0
        
    def get_time_str(self):
        return f"0{self.dayt}day/07"
    
    def save(self):
        save_data = {
            'todo': 0
        }
        pp.utils.io.write_json('save/save.json', save_data)
    
    def reset_save(self):
        pp.utils.io.write_json('save/save.json', DEFAULT_SAVE)
    
    def reset(self):
        pass
    
    def update(self, dt):
        print(self.act)
        if self.act == -2:
            self.intro_timer += dt
            if self.intro_timer >= 1.5:
                self.act = -1
                self.intro_timer = 0.0
                
        if isinstance(self.act, int):
            if self.act < 3 and self.act >= 0:
                self.show_hud = False
            
        if self.act_complete:
            self.gameplay_stop = True
            
            for food in self.e['EntityGroups'].groups['food']:
                food.kill()
                
            self.act_complete = False
                
        if self.playable and not self.gameplay_stop:
            self.time += dt * self.time_speed
            
            while self.time >= 1:
                if not self.gameplay_stop:
                    self.time -= 1
                    self.minute += 1
                    self.day = self.get_time_str()
                    
                    if self.minute >= 60:
                        self.minute = 0
                        self.hour += 1
                        
                        if self.hour >= 24:
                            self.hour = 0
                            self.dayt += 1
                            
                            if self.dayt > 7:
                                self.dayt = 1
                                self.week += 1
                                
                                if self.act >= 3 and self.act not in [4, 7, 10]:
                                    if self.week > self.last_act_change_week:
                                        self.last_act_change_week = self.week
                                        
                                        if self.act == 3:
                                            self.act = 4
                                            self.show_buff_selection = True
                                            
                                            for food in self.e['EntityGroups'].groups['food']:
                                                food.kill()

                                            self.e['Game'].load_activities()
                                            self.e['NPCPlacement'].reset_all_npcs()
                                            
                                        elif self.act == 5:
                                            self.act = 6
                                            self.show_buff_selection = True
                                            
                                        elif self.act == 6:
                                            self.act = 7
                                            self.show_buff_selection = True
                                            
                                            for food in self.e['EntityGroups'].groups['food']:
                                                food.kill()

                                            self.e['Game'].load_activities()
                                            self.e['NPCPlacement'].reset_all_npcs()
                                            
                                        elif self.act == 8:
                                            self.act = 9
                                            self.show_buff_selection = True
                                            
                                            for food in self.e['EntityGroups'].groups['food']:
                                                food.kill()

                                            self.e['Game'].load_activities()
                                            self.e['NPCPlacement'].reset_all_npcs()
                                            
                                        elif self.act == 9:
                                            self.act = 10
                                            self.show_buff_selection = True
                                            
                                            for food in self.e['EntityGroups'].groups['food']:
                                                food.kill()

                                            self.e['Game'].load_activities()
                                            self.e['NPCPlacement'].reset_all_npcs()
                                            