import pygame, random
from enum import Enum
from scripts import pygpen as pp
from scripts.food.food import FoodTypes, Food

class ActivitiesTypes(Enum):
    STORAGE = 'storage'
    DESK = 'desk'
    GRILL = 'grill'
    PLATE_PLACE = 'plate_place'
    SLIME = 'slime'
    PLATES = 'plates'
    BAR_COUTER = 'bar_couter'
    DAY = 'day'

class Holder(pp.Element):
    def __init__(self, activity_type, size, pos, index=None, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        
        self.data = {
            'activity_type': activity_type,
            'size': size,
            'pos': pos,
            'index': index
        }
       
        self.pos = pos
        self.size = size
        self.activity_type = activity_type
        self.item = []
        self.held = False
        self.last_holder = None
        self.original_pos = None
        self.plate_left_behind = None
        self.index = index
        
        if index != None:
            self.remover_animation_speed = 2
    
    def reset(self):
        self.__init__(self.data['activity_type'], self.data['size'], self.data['pos'], index=self.data['index'])

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    @property
    def food_rect(self):
        if len(self.item) == 2:
            food = self.item[1]
            return pygame.Rect(food.pos[0] + 8, food.pos[1] + 8, 
                             food.size[0] - 1, food.size[1] - 1)
        return None
    
    @property
    def has_item(self):
        return len(self.item) > 0

    def get_item(self, new_item):
    
        if self.activity_type == ActivitiesTypes.PLATE_PLACE or self.activity_type == ActivitiesTypes.BAR_COUTER:
            if new_item.food_type != FoodTypes.PLATE:
                return False
            if len(self.item) > 0:
                return False
        else:
            if len(self.item) > 0:
                return False
            if new_item.food_type == FoodTypes.PLATE:
                return False
        
        self.item.append(new_item)
        if new_item.food_type == FoodTypes.PLATE:
            new_item.z = 10
        else:
            new_item.z = 11
        new_item.pos = [self.pos[0] - new_item.size[0]//2 + 2.5,
                       self.pos[1] - new_item.size[1]//2 + 2.5]

        return True

    def eat(self, npc):

        for item in self.item:
            item.on_eat(npc)
                
        self.item = []
        self.held = False
        self.last_holder = None
        self.plate_left_behind = None
        self.original_pos = None
        
    def get_food_on_plate(self, food):
        if self.activity_type != ActivitiesTypes.PLATE_PLACE and self.activity_type != ActivitiesTypes.BAR_COUTER:
            return False
        if len(self.item) == 0 or self.item[0].food_type != FoodTypes.PLATE:
            return False
        if len(self.item) == 2:
            return False
        
        self.item.append(food)
        food.on_plate = True
        food.plate_item = self.item[0]
        food.z = self.item[0].z + 1
        food.update_position_on_plate()
        return True

    def give_item(self):
        if len(self.item) == 0:
            return None
        item = self.item[0]
        self.item.pop(0)
        
        return item

    def give_food_from_plate(self):
        if len(self.item) != 2:
            return None
        food = self.item[1]
        self.item.pop(1)
        food.on_plate = False
        food.plate_item = None
        return food

    def give_plate_with_food(self):
        if len(self.item) != 2:
            return None, None
        plate = self.item[0]
        food = self.item[1]
        self.item = []
        return plate, food

    def pickup_item(self):
        if len(self.item) == 0 or self.held:
            return
        
        self.held = True
        self.original_pos = self.item[0].pos.copy()
        self.last_holder = self
        self.item[0].taken = True
        self.item[0].z = 1000
        self.plate_left_behind = None

    def pickup_food_from_plate(self):
        if len(self.item) != 2 or self.held:
            return
        
        self.held = True
        food = self.item[1]
        plate = self.item[0]
        self.original_pos = food.pos.copy()
        self.last_holder = self
        self.plate_left_behind = plate
        
        self.item = [food]
        food.on_plate = False
        food.plate_item = None
        food.taken = True
        food.z = 1000

    def pickup_plate_with_food(self):
        if len(self.item) != 2 or self.held:
            return
        
        self.held = True
        self.original_pos = self.item[0].pos.copy()
        self.last_holder = self
        self.item[0].taken = True
        self.item[0].z = 1000
        self.item[1].z = 1001
        self.plate_left_behind = None

    def drop_item(self, mpos):
        if not self.held:
            return
        self.held = False
        target = None
        is_plate_with_food = len(self.item) == 2

        if len(self.item) > 0 and self.item[0].food_type == FoodTypes.PLATE:
            for slot in self.e['Game'].plate_place.slots:
                if slot.rect.collidepoint(mpos):
                    if len(slot.item) == 0:
                        target = slot
                        break
            
            if is_plate_with_food:
                for slot in self.e['Game'].bar_couter.slots:
                    if slot.rect.collidepoint(mpos):
                        if len(slot.item) == 0:
                            target = slot
                            break
                    
        else:
            for acts in [self.e['Game'].desk.slots, self.e['Game'].grill.slots, self.e['Game'].slime.slots]:
                for slot in acts:
                    if slot.rect.collidepoint(mpos):
                        if len(slot.item) == 0:
                            target = slot
                            break
            
            if not target:
                for slot in self.e['Game'].plate_place.slots:
                    if slot.rect.collidepoint(mpos):
                        if len(slot.item) == 1 and slot.item[0].food_type == FoodTypes.PLATE:
                            target = slot
                            break
        
        if not target or (target.activity_type == ActivitiesTypes.BAR_COUTER and not self.e['NPCPlacement'].chek(target.index)):
            if self.last_holder:
                if is_plate_with_food:
                    plate, food = self.give_plate_with_food()
                    self.last_holder.get_item(plate)
                    self.last_holder.get_food_on_plate(food)
                else:
                    item = self.give_item()
                    if self.plate_left_behind:
                        self.last_holder.item.insert(0, self.plate_left_behind)
                        self.last_holder.item.append(item)
                        item.on_plate = True
                        item.plate_item = self.plate_left_behind
                        item.z = self.plate_left_behind.z + 1
                        item.update_position_on_plate()
                    else:
                        self.last_holder.get_item(item)
            else:
                self.item = []
            self.plate_left_behind = None
            
        else:
            if target.activity_type == ActivitiesTypes.PLATE_PLACE and len(self.item) > 0 and self.item[0].food_type != FoodTypes.PLATE:
                item = self.give_item()
                target.get_food_on_plate(item)
                if self.plate_left_behind and self.last_holder:
                    self.last_holder.item.append(self.plate_left_behind)
                self.last_holder = target
                
            elif target.activity_type == ActivitiesTypes.BAR_COUTER:
                plate, food = self.give_plate_with_food()
                target.get_item(plate)
                target.get_food_on_plate(food)

            else:
                if is_plate_with_food:
                    plate, food = self.give_plate_with_food()
                    target.get_item(plate)
                    target.get_food_on_plate(food)
                    
                else:
                    item = self.give_item()
                    target.get_item(item)
                    if self.plate_left_behind and self.last_holder:
                        self.last_holder.item.append(self.plate_left_behind)
                self.last_holder = target
                
            self.plate_left_behind = None


    def update(self, mpos, dt):

        if self.activity_type == ActivitiesTypes.BAR_COUTER and len(self.item) > 0:
            self.remover_animation_speed -= dt
            
            if self.e['NPCPlacement'].time(self.index):
                self.remover_animation_speed = 0
                    
            if self.remover_animation_speed <= 0:
                self.eat(self.e['NPCPlacement'].chek(self.index))
                self.remover_animation_speed = 2
                

            
            return False
        
        if not self.rect.collidepoint(mpos):
            if self.held and not self.e['Input'].holding('left_click'):
                self.drop_item(mpos)
            return
        
        if self.e['Input'].pressed('left_click'):

            if len(self.item) == 2:

                if self.food_rect and self.food_rect.collidepoint(mpos):
                    self.pickup_food_from_plate()
                else:
                    self.pickup_plate_with_food()
                    
            elif len(self.item) == 1:
                self.pickup_item()

        elif self.held and not self.e['Input'].holding('left_click'):

            self.drop_item(mpos)

class Generator(Holder):
    def __init__(self, activity_type, size, pos, food_type):
        super().__init__(activity_type, size, pos)
        self.food_type = food_type

    @property
    def has_item(self):
        return True

    def get_item(self, item):
        return False

    def give_item(self):
        food = Food(food_type=self.food_type, pos=self.pos, z=10)
        self.e['EntityGroups'].add(food, group='food')
        return food

    def pickup_item(self):
        if self.held:
            return
        self.held = True
        self.original_pos = self.pos
        self.last_holder = None
        self.plate_left_behind = None
        item = self.give_item()
        item.taken = True
        item.z = 1000
        self.item = [item]

    def drop_item(self, mpos):
        if not self.held:
            return
        self.held = False
        
        target = None
        is_food = self.item[0].food_type != FoodTypes.PLATE
        

        if is_food:
            
            for acts in [self.e['Game'].desk.slots, self.e['Game'].grill.slots, self.e['Game'].slime.slots]:
                for slot in acts:
                    if slot.rect.collidepoint(mpos):
                        if len(slot.item) == 0:
                            target = slot
                            break
            
            if not target:
                for slot in self.e['Game'].plate_place.slots:
                    if slot.rect.collidepoint(mpos):
                        if len(slot.item) == 1 and slot.item[0].food_type == FoodTypes.PLATE:
                            target = slot
                            break
        else:
            for slot in self.e['Game'].plate_place.slots:
                if slot.rect.collidepoint(mpos):
                    if len(slot.item) == 0:
                        target = slot
                        break

        if target:
            self.e['EntityGroups'].groups['food'].pop()
            if is_food and target.activity_type == ActivitiesTypes.PLATE_PLACE:
                target.get_food_on_plate(self.give_item())
            else:
                target.get_item(self.give_item())
        else:
            self.e['EntityGroups'].groups['food'].pop()
        
        self.item = []

    def update(self, mpos, dt):
        if not self.rect.collidepoint(mpos):
            if self.held and not self.e['Input'].holding('left_click'):
                self.drop_item(mpos)
                
            return
        
        if self.e['Input'].pressed('left_click'):
            if not self.held:
                self.pickup_item()


        elif self.held and not self.e['Input'].holding('left_click'):
            self.drop_item(mpos)