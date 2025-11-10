from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Generator, Holder
from scripts.food.food import FoodTypes, Food
import pygame

class Storage(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.STORAGE.value, pos=(10,130), z=1)
        
        self.heart_slot = None
        
        self.slots = [
            Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(19,151), food_type=FoodTypes.MEAT),
            Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(19,172), food_type=FoodTypes.EYE),
            Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(19,193), food_type=FoodTypes.BRAIN),
        ]
    
    def add_heart_slot(self):
        heart_slot = Generator(ActivitiesTypes.STORAGE, size=(42,17), pos=(19,128), food_type=FoodTypes.HEART)
        self.slots.insert(0, heart_slot)