from enum import Enum
from scripts import pygpen as pp

class ActivitiesTypes(Enum):
    STORAGE = 'storage'
    DESK = 'desk'
    GRILL = 'grill'
    PLATE_PLACE = 'plate_place'
    SLIME = 'slime'
    PLATES = 'plates'
    
class Activities(pp.ElementSingleton):
    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        
