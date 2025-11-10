
from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Generator
from scripts.food.food import FoodTypes

class Plates(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.PLATES.value, pos=(317, 125), z=1)
        self.slots = [
            Generator(ActivitiesTypes.PLATES, size=(60, 80), pos=(317, 125), food_type=FoodTypes.PLATE),
        ]