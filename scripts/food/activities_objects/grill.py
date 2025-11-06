
from scripts import pygpen as pp
from scripts.food.activities import Activities, ActivitiesTypes

class Grill(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.GRILL.value, pos=(200, 150), z=2)
        
        self.activities = Activities()

        
        