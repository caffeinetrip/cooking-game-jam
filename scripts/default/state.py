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
        self.health = 100
        
        self.round_end = 100
        self.time = 0
        self.week = 1
        
        self.money = 0

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
            
            
            if self.round_end <= self.time:
                self.week += 1
                self.time = 0
            
            else:
                self.time += dt
