import math
import random
import pygame
import scripts.pygpen as pp
from scripts.default.const import DEFAULT_SAVE, BUFFS

EFFECTS = {
    'todo': 0
}

class State(pp.ElementSingleton):
    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        self.reset()
        self.playable = True
        self.kill_streak = 0
        self.health = 5
        self.base_health = 1 
        self.time = 0
        self.week = 1   
        self.dayt = 1
        self.day = ''
        self.hour = 0
        self.minute = 0
        self.points = 0
        self.time_speed = 200
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

        self.selected_buffs = []
        self.available_gameplay_buffs = [b for b in BUFFS if b['type'] == 'gameplay']
        self.available_lore_buffs = [b for b in BUFFS if b['type'] == 'lore']

        self.cooking_speed_multiplier = 1.0
        self.damage_bonus = 0
        self.fried_damage_multiplier = 1.0
        self.extra_wait_time = 0
        self.bonus_points_active = False
        self.extra_hearts = 0  

        self.week_end_pending = False
        self.week_end_timer = 0.0

        self.has_knife = False
        self.has_heart = False
        self.heart_unlock_pending = True
        self.npc_spawn_pause_timer = 0.0

        self.game_over = False
        self.game_complete = False

        self.grandmother_order_completed = {0: False, 1: False, 2: False}
        
        self.h_scene = False

        
    def get_time_str(self):
        return f"0{self.dayt}day/07"
    
    def apply_buff(self, buff_id):
        if buff_id == 'speed_cooking':
            self.cooking_speed_multiplier = 1.5
        elif buff_id == 'extra_damage':
            self.damage_bonus += 5
        elif buff_id == 'bonus_points':
            self.bonus_points_active = True
        elif buff_id == 'fried_bonus':
            self.fried_damage_multiplier = 1.2
        elif buff_id == 'extra_heart':
            self.health += 1
            self.extra_hearts += 1
        elif buff_id == 'extra_second':
            self.extra_wait_time += 1
        elif buff_id == 'time_slow':
            self.time_speed = 100
    
    def restart_from_death(self):
        self.health = self.base_health + self.extra_hearts
        self.game_over = False
        self.act = 3
        self.week = 1
        self.dayt = 1
        self.time = 0
        self.points = 0
        self.gameplay_stop = False
        self.show_hud = True
        self.e['NPCPlacement'].reset_all_npcs()
        self.e['Game'].load_activities()
        
        for group_name, group in self.e['EntityGroups'].groups.items():
            for item in list(group):
                if hasattr(item, 'food_type'):
                    item.kill()
        
    def save(self):
        save_data = {
            'todo': 0
        }
        pp.utils.io.write_json('save/save.json', save_data)
    
    def reset_save(self):
        pp.utils.io.write_json('save/save.json', DEFAULT_SAVE)
    
    def reset(self):
        pass
    
    def check_all_npcs_dead(self):
        if 'npc' not in self.e['EntityGroups'].groups:
            return True
        npcs = self.e['EntityGroups'].groups.get('npc', [])
        if len(npcs) == 0:
            return True
        for npc in npcs:
            if hasattr(npc, 'alive') and npc.alive:
                return False
        return True
    
    def update(self, dt):
        
        if self.h_scene:
            self.e['NPCPlacement'].reset_all_npcs()
            self.e['Game'].load_activities()
            self.e['NPCPlacement'].stop_spawning = True
            
            for group_name, group in self.e['EntityGroups'].groups.items():
                for item in list(group):
                    if hasattr(item, 'food_type'):
                        item.kill()
        
        if self.health <= 0 and not self.game_over:
            self.game_over = True
            self.gameplay_stop = True
            self.show_hud = False
            return
            
        if self.act == -2:
            self.intro_timer += dt
            if self.intro_timer >= 1.5:
                self.act = -1
                self.intro_timer = 0.0
                
        if isinstance(self.act, int):
            if self.act < 3 and self.act >= 0:
                self.show_hud = False

            if self.act == 11:
                self.game_complete = True
                self.gameplay_stop = True
                self.show_hud = False
            
        if self.act_complete:
            self.gameplay_stop = True
            
            for food in self.e['EntityGroups'].groups.get('food', []):
                food.kill()
                
            self.act_complete = False
        
        if self.npc_spawn_pause_timer > 0:
            self.npc_spawn_pause_timer -= dt
            if self.npc_spawn_pause_timer <= 0:
                self.e['NPCPlacement'].stop_spawning = False
    
        if self.heart_unlock_pending:
            if isinstance(self.act, int) and self.act == 5:  
                if self.week == 2 and self.dayt >= 4:
                    self.npc_spawn_pause_timer = 5
                    if self.check_all_npcs_dead():
                        self.heart_unlock_pending = False
                        self.e['NPCPlacement'].stop_spawning = True
                        self.npc_spawn_pause_timer = 2.0
                            
                        for group_name, group in self.e['EntityGroups'].groups.items():
                            for item in list(group):
                                if hasattr(item, 'food_type'):
                                    item.kill()
                                    
                        self.e['Transition'].transition(lambda: (
                            self.e['DialogueSystem'].start_dialogue('yuki_heart'),
                            self.e['State'].__setattr__('has_heart', True),
                            self.e['Game'].storage.add_heart_slot(),
                            self.e['State'].__setattr__('gameplay_stop', True),
                            self.e['NPCPlacement'].reset_all_npcs()
                        ))
                        
                        self.e['Game'].load_activities()
        
        if self.week_end_pending:
            self.week_end_timer += dt
            if self.week_end_timer >= 0.5:
                if self.check_all_npcs_dead():
                    self.week_end_pending = False
                    self.week_end_timer = 0.0
                    self.e['NPCPlacement'].stop_spawning = True
                    
                    if self.act == 3: 
                        self.e['Transition'].transition(lambda: (
                            self.e['State'].__setattr__('act', 4),
                            self.e['State'].__setattr__('show_buff_selection', True),
                            self.e['State'].__setattr__('gameplay_stop', True),
                            self.e['NPCPlacement'].reset_all_npcs(),

                        ))
                        
                    elif self.act == 5: 
                        self.e['Transition'].transition(lambda: (
                            self.e['State'].__setattr__('act', 6),
                            self.e['State'].__setattr__('show_buff_selection', True),
                            self.e['State'].__setattr__('gameplay_stop', True),
                            self.e['NPCPlacement'].reset_all_npcs()
                        ))
                        
                    elif self.act == 8:  
                        self.e['Transition'].transition(lambda: (
                            self.e['State'].__setattr__('act', 9),
                            self.e['State'].__setattr__('show_buff_selection', True),
                            self.e['State'].__setattr__('gameplay_stop', True),
                            self.e['NPCPlacement'].reset_all_npcs()
                        ))
                    
                    for food in self.e['EntityGroups'].groups.get('food', []):
                        food.kill()

                    self.e['Game'].load_activities()
                
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
                                
                                if isinstance(self.act, int):

                                    if self.act in [3, 5, 8]:
                                        if self.week > self.last_act_change_week:
                                            self.last_act_change_week = self.week
                                            self.week_end_pending = True
                                            self.e['NPCPlacement'].stop_spawning = True