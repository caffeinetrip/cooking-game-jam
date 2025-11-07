import random
from enum import Enum
import scripts.pygpen as pp

class NPCsTypes(Enum):
    MADCAT = 'madcat'
    MADBEAR = 'madbear'
    MADDOVE = 'maddove'
    MADELEPHANT = 'madelephant'

class NPC(pp.Entity):
    def __init__(self, npc_type: NPCsTypes, complexity, pos, z=-1):
        super().__init__(type=npc_type, pos=pos, z=z)
        
        self.type = npc_type
        self.health = 10
        
        if random.random() < complexity * 0.1:
            self.health += 10
            
        self.timer = 10.0
        self.pos = pos
        self.alive = True

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
    WEIGHTS = [40, 30, 20, 10]
    TOTAL_W = sum(WEIGHTS)

    def __init__(self, custom_id=None):
        super().__init__(custom_id)
        
        self.npcs = [None] * self.SLOTS
        self.spawn_timer = 0.0
        self.kill_streak = 0
        
        self.base_spawn_delay = 6.0
        self.spawn_delay_time = 6.0

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
        npc = NPC(self.rand_type(), self.complexity, self.POS[slot])
        self.npcs[slot] = npc
        self.e['EntityGroups'].add(npc, group='npc')
        
        jitter = random.uniform(-2.0, 2.0)
        self.spawn_delay_time = self.base_spawn_delay - self.complexity + jitter
        self.spawn_delay_time = max(4.0, self.spawn_delay_time)

    def feed(self, slot, dmg=5):
        npc = self.npcs[slot]
        if npc and npc.alive:
            npc.take_dmg(dmg)
            if not npc.alive:
                self.kill_streak += 1
                self.npcs[slot] = None
                
    def chek(self, pos):
        if self.npcs[pos]:
            return self.npcs[pos]
        return False
        
    def ping(self, pos):
        print(f'pong {pos}')
        
    def update(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_npc()
            self.spawn_timer = self.spawn_delay()

        for i in range(self.SLOTS):
            npc = self.npcs[i]
            
            if npc and npc.alive:
                npc.update(dt)
                if not npc.alive:

                    self.npcs[i] = None
                    self.e['EntityGroups'].groups['npc'].remove(npc)
        