from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder


class Desk(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.DESK.value, pos=(135, 160), z=1)
        
        self.slots = [
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(143,163)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(168,163)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(143,187)),
            Holder(ActivitiesTypes.DESK, size=(19,19), pos=(168,187)),
        ]
        