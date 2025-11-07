
from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Generator
from scripts.food.food import FoodTypes

class Plates(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.PLATES.value, pos=(330, 140), z=1)
        
        self.slots = [
            Generator(ActivitiesTypes.PLATES, size=(45, 70), pos=(330, 140), food_type=FoodTypes.PLATE),
        ]
        