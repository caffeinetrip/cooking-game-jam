import math
import random

import pygame

from scripts import pygpen as pp

from const import DEFAULT_SAVE

EFFECTS = {

}
            
class State(pp.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.reset()

    
    def save(self):
        save_data = {

        }
        pp.utils.io.write_json('save/save.json', save_data)

    def reset_save(self):
        pp.utils.io.write_json('save/save.json', DEFAULT_SAVE)


    def reset(self):
        pass
