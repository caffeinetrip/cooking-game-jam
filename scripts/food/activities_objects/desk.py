
from scripts import pygpen as pp
from scripts.food.activities import Activities

class Desk(pp.Element):
    def __init__(self, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        
        self.activities = Activities()

        
        