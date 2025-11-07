import random, pygame
from enum import Enum
import scripts.pygpen as pp
from scripts.food.food import FoodTypes

class NPCsTypes(Enum):
    MADCAT = 'madcat'
    MADBEAR = 'madbear'
    MADDOVE = 'maddove'
    MADELEPHANT = 'madelephant'
class OrderDisplay(pp.Entity):
    def __init__(self, food_type: FoodTypes, pos, z=100):
        super().__init__(type=food_type.value, pos=pos, z=z)
        self.food_type = food_type

class NPC(pp.Entity):
    def __init__(self, npc_type: NPCsTypes, complexity, pos, order, z=-1):
        super().__init__(type=npc_type, pos=pos, z=z)
        
        self.type = npc_type
        self.health = 10
        
        self.order = order
        
        if random.random() < complexity * 0.1:
            self.health += 10
            
        self.timer = 10.0
        self.pos = pos
        self.alive = True
        self.order_display = None

    def take_dmg(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.timer = -1

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False

class NPCPlacement(pp.ElementSingleton):
    SLOTS = 6
    POS = {i: (79 + i*40, 55) for i in range(SLOTS)}
    GUI_POS = {i: (61 + i*40, 75) for i in range(SLOTS)}
    WEIGHTS = [40, 30, 20, 10]
    TOTAL_W = sum(WEIGHTS)

    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        
        self.npcs = [None] * self.SLOTS
        self.spawn_timer = 0.0
        self.kill_streak = 0
        
        self.base_spawn_delay = 6.0
        self.spawn_delay_time = 6.0
        
        self.order_icon = None

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
        
    def feed(self, slot, dmg=5):
        npc = self.npcs[slot]
        if npc and npc.alive:
            npc.take_dmg(dmg)
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
        
    def ping(self, pos):
        print(f'pong {pos}')
        
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
                    
    def update(self, dt, surf):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_npc()
            self.spawn_timer = self.spawn_delay()

        self.draw_timer(surf)

        for i in range(self.SLOTS):
            npc = self.npcs[i]
            if npc and npc.alive:
                npc.update(dt)
                if not npc.alive:
                    if npc.order_display:
                        self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                    self.npcs[i] = None
                    self.e['EntityGroups'].groups['npc'].remove(npc)