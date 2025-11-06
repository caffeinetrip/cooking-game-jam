from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder

class Grill(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.GRILL.value, pos=(200, 150), z=2)
        
        self.slots = [
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(205,155)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(233,155)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(205,183)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(233,183)),
        ]
        
