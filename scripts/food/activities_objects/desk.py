from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder
from scripts.food.food import Food, FoodTypes
import pygame

class Desk(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.DESK.value, pos=(135, 160), z=1)
        
        self.slots = [
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(143,163)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(168,163)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(143,187)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(168,187)),
        ]

    def update(self, mpos):
        if self.e['Input'].pressed('right_click'):
            for slot in self.slots:
                if slot.rect.collidepoint(mpos) and len(slot.item) == 1:
                    food = slot.item[0]
                    
                    if food.food_type != FoodTypes.PLATE:
                        
                        cut_map = {
                            FoodTypes.HEART: FoodTypes.CUT_HEART,
                            FoodTypes.MEAT: FoodTypes.CUT_MEAT,
                            FoodTypes.EYE: FoodTypes.CUT_EYE,
                            FoodTypes.BRAIN: FoodTypes.CUT_BRAIN,
                        }
                        
                        if food.food_type in cut_map:
                            new_type = cut_map[food.food_type]
                            new_food = Food(food_type=new_type, pos=food.pos.copy(), z=food.z)
                            
                            self.e['EntityGroups'].add(new_food, group='food')
                            
                            if food in self.e['EntityGroups'].groups['food']:
                                self.e['EntityGroups'].groups['food'].remove(food)
                                
                            slot.item[0] = new_food