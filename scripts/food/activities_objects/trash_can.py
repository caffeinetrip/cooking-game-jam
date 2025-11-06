
from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes

class TrashCan(pp.Entity):
    def __init__(self):
        super().__init__(type='trash_can', pos=(170, 20), z=1)
