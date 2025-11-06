
from scripts import pygpen as pp
from scripts.food.activities import Activities, ActivitiesTypes

class Plates(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.PLATES.value, pos=(330, 140), z=1)
        
        self.activities = Activities()

        
        