from scripts import pygpen as pp
from scripts.food.activities import ActivitiesTypes, Holder
from scripts.food.food import FoodTypes, Food


class Slime(pp.Entity):
    def __init__(self):
        super().__init__(type=ActivitiesTypes.SLIME.value, pos=(70, 148), z=1)
        self.slots = [
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(79,153)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(102,153)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(79,175)),
            Holder(ActivitiesTypes.SLIME, size=(19,19), pos=(102,175)),
        ]
    
    def update(self):
        for slot in self.slots:
            if len(slot.item) == 1:
                food = slot.item[0]
                if food.food_type != FoodTypes.PLATE:
                    green_map = {
                        FoodTypes.HEART: FoodTypes.GREEN_HEART,
                        FoodTypes.MEAT: FoodTypes.GREEN_MEAT,
                        FoodTypes.EYE: FoodTypes.GREEN_EYE,
                        FoodTypes.BRAIN: FoodTypes.GREEN_BRAIN
                    }
                    if food.food_type in green_map:
                        new_type = green_map[food.food_type]
                        new_food = Food(food_type=new_type, pos=food.pos.copy(), z=food.z)
                        self.e['EntityGroups'].add(new_food, group='food')
                        if food in self.e['EntityGroups'].groups['food']:
                            self.e['EntityGroups'].groups['food'].remove(food)
                        slot.item[0] = new_food