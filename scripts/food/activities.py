import pygame
from enum import Enum
from scripts import pygpen as pp

class ActivitiesTypes(Enum):
    STORAGE = 'storage'
    DESK = 'desk'
    GRILL = 'grill'
    PLATE_PLACE = 'plate_place'
    SLIME = 'slime'
    PLATES = 'plates'

class Holder(pp.Element):
    def __init__(self, activity_type, size, pos, custom_id=None, singleton=False, register=False):
        super().__init__(custom_id, singleton, register)
        self.pos = pos
        self.size = size
        self.activity_type = activity_type
        self.item = None
        self.held = False
        self.last_holder = None
        self.original_pos = None

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def get_item(self, item):
        if self.item:
            return False
        self.item = item
        if item:
            item.pos = [self.pos[0] - item.size[0]//2 + 2.5,
                        self.pos[1] - item.size[1]//2 + 2.5]
            self.e['EntityGroups'].add(item, group='activities')
            
        return True

    def give_item(self):
        if not self.item:
            return None
        
        item = self.item
        self.item = None
        return item

    def pickup_item(self):
        if not self.item or self.held:
            return
        
        self.held = True
        self.original_pos = self.item.pos.copy()
        
        self.last_holder = self
        self.item.taken = True
        self.item.z = 100

    def drop_item(self, mpos):
        if not self.held:
            return

        self.held = False

        target = None
        for acts in [self.e['Game'].desk.slots, self.e['Game'].grill.slots,
                    self.e['Game'].plate_place.slots, self.e['Game'].slime.slots]:
            for slot in acts:
                if slot.rect.collidepoint(mpos):
                    if not slot.item:
                        target = slot
                        break
        if target:
            target.get_item(self.give_item())
            self.last_holder = target
            
        else:
            self.get_item(self.give_item())
            self.last_holder = self

    def update(self, mpos):
        
        if not self.rect.collidepoint(mpos):

            if self.held and not self.e['Input'].holding('left_click'):
                self.drop_item(mpos)
            return
        
        if self.e['Input'].pressed('left_click'):
            if self.item and not self.held:
                self.pickup_item()

        elif self.held and not self.e['Input'].holding('left_click'):
            self.drop_item(mpos)