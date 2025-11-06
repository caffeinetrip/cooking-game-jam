from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder


class Slime(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.SLIME.value, pos=(70, 158), z=1)
        
        
        self.slots = [
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(79,163)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(102,163)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(79,185)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(102,185)),
        ]
        
