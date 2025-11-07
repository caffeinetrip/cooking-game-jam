from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder

class BarCouter(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.BAR_COUTER.value, pos=(67, 115), z=0)
        
        self.slots = [
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(87, 115)),
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(127, 115)),
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(167, 115)),
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(207, 115)),
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(247, 115)),
            Holder(ActivitiesTypes.BAR_COUTER, size=(20,20), pos=(287, 115))
        ]
        
    def update(self):
        for slot in self.slots:
            if len(slot.item) == 2:
                slot.item[1].update_position_on_plate()

