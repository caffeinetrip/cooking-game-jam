import random
from enum import Enum
from scripts import pygpen as pp

class NPCsTypes(Enum):
    MADCAT = 'madcat'
    MADBEAR = 'madbear'
    MADDOVE = 'maddove'
    MADELEPHANT = 'madelephant'
        
class NPC(pp.Entity):
    def __init__(self, npc_type: NPCsTypes, order, complexity, pos, z=0, custom_id=None):
        super().__init__(type=npc_type.value, pos=pos, z=z)
        self.food_type = npc_type
        self.health = 5 + complexity * 5
        
        self.order = order
        
        self.timer = 10

    def kill(self):
        pass
        
    def take_dmg(self, dmg):
        
        if self.health > dmg:
            self.health -= dmg
        
        else:
            self.kill()