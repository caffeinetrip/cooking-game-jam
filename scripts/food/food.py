import random
from enum import Enum
from scripts import pygpen as pp

class FoodTypes(Enum):
    HEART = 'heart'
    MEAT = 'meat'
    EYE = 'eye'
    BRAIN = 'brain'
    PLATE = 'plate'

class Food(pp.Entity):
    def __init__(self, food_type: FoodTypes, pos, base_dmg=5, z=0, custom_id=None):
        super().__init__(type=food_type.value, pos=pos, z=z)
        self.food_type = food_type
        self.base_dmg = base_dmg
        self.taken = False
        self.in_holder = False
        self.on_holder = False
        self.original_z = z
        self.on_plate = False
        self.plate_item = None

    def damage(self):
        dmg = self.base_dmg
        if random.random() < 0.2:
            dmg *= 2
        return dmg

    def on_eat(self, eater):
        damage = self.damage()
        eater.take_damage(damage)
        self.kill()

    def update_position_on_plate(self):
        if self.on_plate and self.plate_item:
            self.pos = [self.plate_item.pos[0] + (self.plate_item.size[0] - self.size[0]) / 2,
                       self.plate_item.pos[1] + (self.plate_item.size[1] - self.size[1]) / 2 - 2]