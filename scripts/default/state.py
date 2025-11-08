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
        if self.playable:
            self.time += dt * self.time_speed
            
            while self.time >= 1:
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