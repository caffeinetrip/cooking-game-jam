
from scripts import pygpen as pp
from scripts.food.activities import Activities, ActivitiesTypes

class Slime(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.SLIME.value, pos=(70, 158), z=1)
        
        self.activities = Activities()

        
        