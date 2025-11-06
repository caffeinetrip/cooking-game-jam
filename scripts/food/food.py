
import random
from enum import Enum
from scripts import pygpen as pp

class FoodTypes(Enum):
    HEART = 'heart'
    MEAT = 'meat'
    EYE = 'eye'
    BRAIN = 'brain'

class Food(pp.Entity):
    def __init__(self, food_type: FoodTypes, pos, z=0, custom_id=None):
        super().__init__(type=food_type.value, pos=pos, z=z)
        self.food_type = food_type
        self.base_dmg = 5

    def damage(self):
        dmg = self.base_dmg
        if random.random() < 0.2:
            dmg *= 2
        return dmg

    def on_eat(self, eater):
        damage = self.damage()
        eater.take_damage(damage)
        self.kill()