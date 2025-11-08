
from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes

class Day(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.DAY.value, pos=(333, 114), z=1)
        