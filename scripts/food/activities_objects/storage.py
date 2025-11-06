
from scripts import pygpen as pp
from scripts.food.activities import Activities, ActivitiesTypes

class Storage(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.STORAGE.value, pos=(5,120), z=1)
        
        self.activities = Activities()

        
        