
from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Generator
from scripts.food.food import FoodTypes

class Storage(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.STORAGE.value, pos=(5,120), z=1)

        self.slots = [
                    Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(14,125), food_type=FoodTypes.HEART),
                    Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(14,146), food_type=FoodTypes.MEAT),
                    Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(14,167), food_type=FoodTypes.EYE),
                    Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(14,188), food_type=FoodTypes.BRAIN),
                ]