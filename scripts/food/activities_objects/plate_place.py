
from scripts import pygpen as pp
from scripts.food.activities import Activities, ActivitiesTypes

class PlatePlace(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.PLATE_PLACE.value, pos=(265, 160), z=1)
        
        self.activities = Activities()

        
        