import random, pygame
from enum import Enum
import scripts.pygpen as pp
from scripts.food.food import FoodTypes

class NPCsTypes(Enum):
    MADCAT = 'madcat'
    MADBEAR = 'madbear'
    MADDOVE = 'maddove'
    MADELEPHANT = 'madelephant'
    GRANDMOTHER = 'grandmother'
    
class OrderDisplay(pp.Entity):
    def __init__(self, food_type: FoodTypes, pos, z=100):
        super().__init__(type=food_type.value, pos=pos, z=z)
        self.food_type = food_type

class NPC(pp.Entity):
    def __init__(self, npc_type: NPCsTypes, complexity, pos, order, z=-1, is_grandmother=False):
        super().__init__(type=npc_type, pos=pos, z=z)
        
        self.type = npc_type
        self.health = 15
        
        self.order = order
        
        self.is_grandmother = is_grandmother
        
        if not is_grandmother and random.randint(1,15) == 5:
            self.health += 5
            
        self.timer = 10.0 if not is_grandmother else -1
        self.pos = pos
        self.alive = True
        self.order_display = None
        
        self.killed = False

    def take_dmg(self, dmg):
        self.health -= dmg
        
        if self.health <= 0:
            self.timer = -1
            self.killed = True
            self.e['State'].points += 1

    def update(self, dt):

        if self.timer > 0:
            self.timer -= dt
            
        elif self.timer <= 0:
            if not self.killed:
                self.e['State'].health -= 1
            self.alive = False

class NPCPlacement(pp.ElementSingleton):
    SLOTS = 6
    POS = {i: (79 + i*40, 55) for i in range(SLOTS)}
    GUI_POS = {i: (61 + i*40, 75) for i in range(SLOTS)}
    WEIGHTS = [40, 30, 20, 10]
    TOTAL_W = sum(WEIGHTS)
    GRANDMOTHER_SLOT = 2

    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        
        self.npcs = [None] * self.SLOTS
        self.spawn_timer = 0.0
        self.kill_streak = 0
        
        self.base_spawn_delay = 10.0
        self.spawn_delay_time = 10.0
        
        self.order_icon = None
        
        self.health_hud = pygame.image.load('data/images/hud/madheart.png')
        
        self.grandmother_spawned = False

    def load_assets(self):
        try:
            self.order_icon = pygame.image.load('data/images/activities/hud/order.png').convert_alpha()
        except:
            self.order_icon = None

    def rand_type(self):
        r = random.randint(1, self.TOTAL_W)
        for i, w in enumerate(self.WEIGHTS):
            r -= w
            if r <= 0:
                return list(NPCsTypes)[i].value

    def spawn_delay(self):
        base = self.spawn_delay_time
        speed = self.kill_streak * 0.4
        return max(4.0, base - speed)

    @property
    def complexity(self):
        week = self.e['State'].week
        time = self.e['State'].time 
        week_progress = (week - 1) + (time / 100.0)

        base_complexity = int(week_progress * 2)

        streak_bonus = self.kill_streak // 5

        return max(0, base_complexity + streak_bonus)
    
    def get_grandmother_order(self):
        act = self.e['State'].act
        
        if act == 0:
            options = [FoodTypes.HEART, FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN]
        elif act == 1:
            options = [FoodTypes.GREEN_HEART, FoodTypes.GREEN_MEAT, FoodTypes.GREEN_EYE, FoodTypes.GREEN_BRAIN]
        elif act == 2:
            options = [FoodTypes.FRIED_GREEN_HEART, FoodTypes.FRIED_GREEN_MEAT, 
                      FoodTypes.FRIED_GREEN_EYE, FoodTypes.FRIED_GREEN_BRAIN]
        else:
            return None
            
        return random.choice(options)
    
    def spawn_grandmother(self):
        if self.grandmother_spawned:
            return
        
        order = self.get_grandmother_order()
        if order is None:
            return
            
        npc = NPC(NPCsTypes.GRANDMOTHER.value, 0, self.POS[self.GRANDMOTHER_SLOT], order, is_grandmother=True)
        self.npcs[self.GRANDMOTHER_SLOT] = npc
        self.e['EntityGroups'].add(npc, group='npc')
        
        order_display = OrderDisplay(order, self.GUI_POS[self.GRANDMOTHER_SLOT], z=100)
        npc.order_display = order_display
        self.e['EntityGroups'].add(order_display, group='ui')
        
        self.grandmother_spawned = True
                
    def spawn_npc(self):
        empty_slots = [i for i, n in enumerate(self.npcs) if n is None]
        if not empty_slots:
            return
        
        slot = random.choice(empty_slots)
        order = random.choice([ft for ft in list(FoodTypes) if ft != FoodTypes.PLATE])
        npc = NPC(self.rand_type(), self.complexity, self.POS[slot], order)
        self.npcs[slot] = npc
        self.e['EntityGroups'].add(npc, group='npc')
        
        order_display = OrderDisplay(order, self.GUI_POS[slot], z=100)
        npc.order_display = order_display
        self.e['EntityGroups'].add(order_display, group='ui')

        jitter = random.uniform(-2.0, 2.0)
        self.spawn_delay_time = self.base_spawn_delay - self.complexity + jitter
        self.spawn_delay_time = max(4.0, self.spawn_delay_time)
        
    def feed(self, food_type, slot):
        if food_type == FoodTypes.PLATE: return
        
        npc = self.npcs[slot]

        if npc and npc.alive:
            if npc.is_grandmother:
                if food_type == npc.order:
                    self.e['State'].act_complete = True
                    self.grandmother_spawned = False
                    self.e['State'].gameplay_stop = True
                    self.e['State'].act += 1
                    
                else:
                    self.e['State'].act = 'miss_dish'
                    self.e['State'].act_complete = False
                    self.grandmother_spawned = False
                    self.e['State'].gameplay_stop = True
                    
                if npc.order_display:
                    self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                self.e['EntityGroups'].groups['npc'].remove(npc)
                self.npcs[slot] = None
            else:
                npc.take_dmg(5)
                if not npc.alive:
                    self.kill_streak += 1
                    if npc.order_display:
                        self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                    self.npcs[slot] = None
                
    def chek(self, pos):
        if self.npcs[pos]:
            return self.npcs[pos]
        return False
    
    def time(self, pos):
        if self.npcs[pos]:
            return self.npcs[pos].timer < 2
        return False
        
    def draw_timer(self, surface):
        for i in range(self.SLOTS):
            npc = self.npcs[i]
            if npc and npc.alive and npc.timer > 0:
                center = (int(self.POS[i][0] + 34), int(self.POS[i][1]))
                radius = 5
                progress = max(0, npc.timer / 10.0)
                angle = -2 * 3.1415926535 * progress
                pygame.draw.circle(surface, (2, 2, 2), center, radius + 2)
                pygame.draw.circle(surface, (255, 255, 255), center, radius, 3)
                if progress > 0:
                    start_angle = 1.57079632679
                    pygame.draw.arc(surface, (200, 200, 200), 
                                    (center[0] - radius, center[1] - radius, radius*2, radius*2),
                                    start_angle, start_angle + angle, 3)
                
                for j in range(npc.health//5):
                    pos = (int(self.POS[i][0] + 37), int(self.POS[i][1])+10 + (j * 8))
                    surface.blit(self.health_hud, pos)
                    
    def update(self, dt, surf):
        act = self.e['State'].act
        
        if act in [0, 1, 2] and not self.grandmother_spawned:
            self.spawn_grandmother()
        
        if act == 3:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_npc()
                self.spawn_timer = self.spawn_delay()

        self.draw_timer(surf)

        for i in range(self.SLOTS):
            npc = self.npcs[i]
            if npc and npc.alive:
                if not npc.is_grandmother:
                    npc.update(dt)
                    if not npc.alive:
                        if npc.order_display:
                            self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                            
                        self.npcs[i] = None
                        self.e['EntityGroups'].groups['npc'].remove(npc)