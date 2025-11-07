from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder
from scripts.food.food import Food, FoodTypes

class Grill(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.GRILL.value, pos=(200, 150), z=2)
        
        self.slots = [
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(205,155)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(233,155)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(205,183)),
            Holder(ActivitiesTypes.GRILL, size=(22,22), pos=(233,183)),
        ]
        
        for slot in self.slots:
            slot.fry_timer = 0.0

    def update(self, dt):
        for slot in self.slots:
            if len(slot.item) == 1:
                food = slot.item[0]
                if food.food_type != FoodTypes.PLATE:
                    slot.fry_timer += dt
                    
                    if slot.fry_timer >= 3.0:
                        
                        fry_map = {
                            FoodTypes.HEART: FoodTypes.FRIED_HEART,
                            FoodTypes.GREEN_HEART: FoodTypes.FRIED_GREEN_HEART,
                            FoodTypes.CUT_HEART: FoodTypes.FRIED_CUT_HEART,
                            FoodTypes.MEAT: FoodTypes.FRIED_MEAT,
                            FoodTypes.GREEN_MEAT: FoodTypes.FRIED_GREEN_MEAT,
                            FoodTypes.CUT_MEAT: FoodTypes.FRIED_CUT_MEAT,
                            FoodTypes.EYE: FoodTypes.FRIED_EYE,
                            FoodTypes.GREEN_EYE: FoodTypes.FRIED_GREEN_EYE,
                            FoodTypes.CUT_EYE: FoodTypes.FRIED_CUT_EYE,
                            FoodTypes.BRAIN: FoodTypes.FRIED_BRAIN,
                            FoodTypes.GREEN_BRAIN: FoodTypes.FRIED_GREEN_BRAIN,
                            FoodTypes.CUT_BRAIN: FoodTypes.FRIED_CUT_BRAIN,
                        }
                        
                        if food.food_type in fry_map:
                            new_type = fry_map[food.food_type]
                            
                            temp_data = [food.pos, food.z]
                            
                            food.reset(new_type.value, temp_data[0], temp_data[1])
                            food.food_type = new_type
                            print(1)
                                
                            slot.fry_timer = 0.0
                else:
                    slot.fry_timer = 0.0
                    
            else:
                slot.fry_timer = 0.0