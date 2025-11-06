
from scripts import pygpen as pp

class Activities(pp.ElementSingleton):
    def __init__(self, custom_id=None):
        super().__init__(custom_id)
