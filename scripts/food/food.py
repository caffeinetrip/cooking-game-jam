import random
from enum import Enum
from scripts import pygpen as pp

class FoodTypes(Enum):
    HEART = 'heart'
    GREEN_HEART = 'green_heart'
    CUT_HEART = 'cut_heart'
    FRIED_HEART = 'fried_heart'
    FRIED_GREEN_HEART = 'fried_green_heart'
    FRIED_CUT_HEART = 'fried_cut_heart'

    MEAT = 'meat'
    GREEN_MEAT = 'green_meat'
    CUT_MEAT = 'cut_meat'
    FRIED_MEAT = 'fried_meat'
    FRIED_GREEN_MEAT = 'fried_green_meat'
    FRIED_CUT_MEAT = 'fried_cut_meat'

    EYE = 'eye'
    GREEN_EYE = 'green_eye'
    CUT_EYE = 'cut_eye'
    FRIED_EYE = 'fried_eye'
    FRIED_GREEN_EYE = 'fried_green_eye'
    FRIED_CUT_EYE = 'fried_cut_eye'

    BRAIN = 'brain'
    GREEN_BRAIN = 'green_brain'
    CUT_BRAIN = 'cut_brain'
    FRIED_BRAIN = 'fried_brain'
    FRIED_GREEN_BRAIN = 'fried_green_brain'
    FRIED_CUT_BRAIN = 'fried_cut_brain'

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

    def reset(self, food_type, pos, z):
        super().__init__(type=food_type, pos=pos, z=z)
    
    def damage(self):
        
        dmg = self.base_dmg
        
        if random.random() < 0.2:
            dmg *= 2
        return dmg

    def on_eat(self, eater):
        if self.food_type != FoodTypes.PLATE:
            damage = self.damage()
            if eater.order == self.food_type: damage *= 3
            eater.take_dmg(damage)
        self.kill()
        
    def kill(self):
            
        if self.on_plate and self.plate_item:
            self.plate_item.kill()
            self.on_plate = False
        
        for name, group in self.e['EntityGroups'].groups.items():
            
            for item in group:
                if item == self:
                    self.e['EntityGroups'].groups[name].remove(self)
                    
        del self


    def update_position_on_plate(self):
        if self.on_plate and self.plate_item:
            self.pos = [self.plate_item.pos[0] + (self.plate_item.size[0] - self.size[0]) / 2,
                        self.plate_item.pos[1] + (self.plate_item.size[1] - self.size[1]) / 2 - 2]