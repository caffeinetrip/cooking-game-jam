from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder

class PlatePlace(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.PLATE_PLACE.value, pos=(265, 160), z=1)
        
        self.slots = [
            Holder(ActivitiesTypes.PLATE_PLACE, size=(20,20), pos=(270,164)),
            Holder(ActivitiesTypes.PLATE_PLACE, size=(20,20), pos=(300,164)),
            Holder(ActivitiesTypes.PLATE_PLACE, size=(20,20), pos=(270,187)),
            Holder(ActivitiesTypes.PLATE_PLACE, size=(20,20), pos=(300,187)),
        ]
        
