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
    BOSS = 'boss'
   
class OrderDisplay(pp.Entity):
    def __init__(self, food_type: FoodTypes, pos, z=100):
        super().__init__(type=food_type.value, pos=pos, z=z)
        self.food_type = food_type

class NPC(pp.Entity):
    def __init__(self, npc_type: NPCsTypes, complexity, pos, order, wait_time=10.0, z=-1, is_grandmother=False):
        super().__init__(type=npc_type, pos=pos, z=z)
       
        self.type = npc_type
        self.health = 15
       
        self.order = order
       
        self.is_grandmother = is_grandmother
       
        if not is_grandmother and random.randint(1,15) == 5:
            self.health += 5
           
        base_timer = wait_time + self.e['State'].extra_wait_time
        self.timer = base_timer if not is_grandmother else -1
        self.pos = pos
        self.alive = True
        self.order_display = None
       
        self.killed = False

    def take_dmg(self, dmg):
        self.health -= dmg
       
        if self.health <= 0:
            self.timer = -1
            self.killed = True
            points_to_add = 1
            if self.e['State'].bonus_points_active:
                points_to_add = 2
            self.e['State'].points += points_to_add

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt
           
        elif self.timer <= 0:
            if not self.killed:
                self.e['State'].health -= 1
            self.alive = False

class Boss(pp.Entity):
    def __init__(self):
        super().__init__(type='boss', pos=(0, 0), z=-10)
       
        self.max_health = 45
        self.health = self.max_health
        self.alive = True
        self.damage_timer = 20.0
        self.attack_interval = 20.0
        self.orders = [None] * 5
        self.order_displays = []
        
        self.generate_initial_orders()
       
    def generate_initial_orders(self):
        for display in self.order_displays:
            if display in self.e['EntityGroups'].groups.get('ui', []):
                self.e['EntityGroups'].groups['ui'].remove(display)
        self.order_displays = []
       
        gui_positions = {
            0: (82, 80),
            1: (122, 80),
            2: (162, 80),
            3: (202, 80),
            4: (242, 80)
        }
       
        all_food_types = [ft for ft in list(FoodTypes) if ft != FoodTypes.PLATE]
        if self.e['State'].has_heart:
            pass
        else:
            all_food_types = [ft for ft in all_food_types if 'HEART' not in ft.name]
            
        for i in range(5):
            self.orders[i] = random.choice(all_food_types)
            order_display = OrderDisplay(self.orders[i], gui_positions[i], z=100)
            self.order_displays.append(order_display)
            self.e['EntityGroups'].add(order_display, group='ui')
            
    def generate_order_for_slot(self, slot):
        if self.orders[slot] is not None:
            return 
            
        gui_positions = {
            0: (82, 80),
            1: (122, 80),
            2: (162, 80),
            3: (202, 80),
            4: (242, 80)
        }
        
        all_food_types = [ft for ft in list(FoodTypes) if ft != FoodTypes.PLATE]
        if not self.e['State'].has_heart:
            all_food_types = [ft for ft in all_food_types if 'HEART' not in ft.name]
            
        self.orders[slot] = random.choice(all_food_types)
        
        if slot < len(self.order_displays) and self.order_displays[slot]:
            if self.order_displays[slot] in self.e['EntityGroups'].groups.get('ui', []):
                self.e['EntityGroups'].groups['ui'].remove(self.order_displays[slot])
        
        order_display = OrderDisplay(self.orders[slot], gui_positions[slot], z=100)
        if slot < len(self.order_displays):
            self.order_displays[slot] = order_display
        else:
            while len(self.order_displays) <= slot:
                self.order_displays.append(None)
            self.order_displays[slot] = order_display
        self.e['EntityGroups'].add(order_display, group='ui')
   
    def take_dmg(self, food_type, slot):
        if self.orders[slot] is None:
            return
        
        if food_type != self.orders[slot]:
            return

        damage = 5
        self.health -= damage
        self.health = max(0, self.health)

        self.orders[slot] = None
        if slot < len(self.order_displays) and self.order_displays[slot]:
            if self.order_displays[slot] in self.e['EntityGroups'].groups.get('ui', []):
                self.e['EntityGroups'].groups['ui'].remove(self.order_displays[slot])

        self.generate_order_for_slot(slot)

        if self.health <= 0:
            self.alive = False
            for display in self.order_displays:
                if display and display in self.e['EntityGroups'].groups.get('ui', []):
                    self.e['EntityGroups'].groups['ui'].remove(display)
            self.e['State'].boss_defeated = True
            self.e['State'].h_scene = True

           
    def update(self, dt):
        if not self.alive:
            self.e['State'].h_scene = True
        
        self.damage_timer -= dt
        if self.damage_timer <= 0:
            self.e['State'].health -= 1
            self.damage_timer = self.attack_interval

class NPCPlacement(pp.ElementSingleton):
    SLOTS = 5
    POS = {i: (79 + i*40, 55) for i in range(SLOTS)}
    GUI_POS = {i: (61 + i*40, 75) for i in range(SLOTS)}
    WEIGHTS = [40, 30, 20, 10]
    TOTAL_W = sum(WEIGHTS)
    GRANDMOTHER_SLOT = 2

    ACT_SPAWN_DELAYS = {
        3: 7.0,
        5: 8.0,
        8: 9.0, 
        10: 10.0,
    }
    
    ACT_WAIT_TIMES = {
        3: 20.0, 
        5: 15.0,  
        8: 10.0,
    }
   
    ACT_FOOD_POOLS = {
        3: {
            'pools': [
                [FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN],
                [FoodTypes.GREEN_MEAT, FoodTypes.GREEN_EYE, FoodTypes.GREEN_BRAIN],
            ],
            'weights': [80, 20]
        },
        5: {
            'pools': [
                [FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN],
                [FoodTypes.GREEN_MEAT, FoodTypes.GREEN_EYE, FoodTypes.GREEN_BRAIN],
                [FoodTypes.CUT_MEAT, FoodTypes.CUT_EYE, FoodTypes.CUT_BRAIN],
                [FoodTypes.FRIED_MEAT, FoodTypes.FRIED_GREEN_MEAT, FoodTypes.FRIED_CUT_MEAT,
                 FoodTypes.FRIED_EYE, FoodTypes.FRIED_GREEN_EYE, FoodTypes.FRIED_CUT_EYE,
                 FoodTypes.FRIED_BRAIN, FoodTypes.FRIED_GREEN_BRAIN, FoodTypes.FRIED_CUT_BRAIN],
            ],
            'weights': [10, 40, 40, 10]
        },
        8: {
            'pools': [
                [FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN],
                [FoodTypes.GREEN_MEAT, FoodTypes.GREEN_EYE, FoodTypes.GREEN_BRAIN],
                [FoodTypes.CUT_MEAT, FoodTypes.CUT_EYE, FoodTypes.CUT_BRAIN],
                [FoodTypes.FRIED_MEAT, FoodTypes.FRIED_GREEN_MEAT, FoodTypes.FRIED_CUT_MEAT,
                 FoodTypes.FRIED_EYE, FoodTypes.FRIED_GREEN_EYE, FoodTypes.FRIED_CUT_EYE,
                 FoodTypes.FRIED_BRAIN, FoodTypes.FRIED_GREEN_BRAIN, FoodTypes.FRIED_CUT_BRAIN],
            ],
            'weights': [10, 10, 10, 70]
        },
    }

    def __init__(self, custom_id=None):
        super().__init__(custom_id)
       
        self.npcs = [None] * self.SLOTS
        self.spawn_timer = 0.0
        self.kill_streak = 0
       
        self.order_icon = None
       
        self.health_hud = pygame.image.load('data/images/hud/madheart.png')
       
        self.grandmother_spawned = False
       
        self.boss = None
       
        self.stop_spawning = False
        self.yuki_pause_timer = 0.0

    def reset_all_npcs(self):
        for i in range(self.SLOTS):
            npc = self.npcs[i]
            if npc:
                if npc.order_display and npc.order_display in self.e['EntityGroups'].groups.get('ui', []):
                    self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                if npc in self.e['EntityGroups'].groups.get('npc', []):
                    self.e['EntityGroups'].groups['npc'].remove(npc)
                self.npcs[i] = None
       
        if self.boss:
            for display in self.boss.order_displays:
                if display and display in self.e['EntityGroups'].groups.get('ui', []):
                    self.e['EntityGroups'].groups['ui'].remove(display)
            if self.boss in self.e['EntityGroups'].groups.get('npc', []):
                self.e['EntityGroups'].groups['npc'].remove(self.boss)
            self.boss = None
       
        self.grandmother_spawned = False
        self.spawn_timer = 0.0
        self.stop_spawning = False

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

    def get_act_spawn_delay(self):
        act = self.e['State'].act
        return self.ACT_SPAWN_DELAYS.get(act, 10.0)
        
    def get_act_wait_time(self):
        act = self.e['State'].act
        return self.ACT_WAIT_TIMES.get(act, 10.0)
   
    def get_random_order_for_act(self):
        act = self.e['State'].act
       
        if act not in self.ACT_FOOD_POOLS:
            available_types = [ft for ft in list(FoodTypes) if ft != FoodTypes.PLATE]

            if not self.e['State'].has_heart:
                available_types = [ft for ft in available_types if 'HEART' not in ft.name]

            if not self.e['State'].has_knife:
                available_types = [ft for ft in available_types if 'CUT' not in ft.name]
            return random.choice(available_types) if available_types else FoodTypes.MEAT
       
        pool_data = self.ACT_FOOD_POOLS[act]
        total_weight = sum(pool_data['weights'])
        r = random.randint(1, total_weight)
       
        for i, weight in enumerate(pool_data['weights']):
            r -= weight
            if r <= 0:
                pool = pool_data['pools'][i]
                if not self.e['State'].has_heart:
                    pool = [ft for ft in pool if 'HEART' not in ft.name]
                    
                if not self.e['State'].has_knife:
                    pool = [ft for ft in pool if 'CUT' not in ft.name]
                if len(pool) == 0:
                    pool = [FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN]
                return random.choice(pool)
       
        return random.choice(pool_data['pools'][0])

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
            options = [FoodTypes.MEAT, FoodTypes.EYE, FoodTypes.BRAIN]
        elif act == 1:
            options = [FoodTypes.GREEN_MEAT, FoodTypes.GREEN_EYE, FoodTypes.GREEN_BRAIN]
        elif act == 2:
            options = [FoodTypes.FRIED_GREEN_MEAT,
                      FoodTypes.FRIED_GREEN_EYE, FoodTypes.FRIED_GREEN_BRAIN]
        else:
            return None
           
        return random.choice(options)
   
    def spawn_grandmother(self):
        if self.grandmother_spawned or self.e['State'].grandmother_order_completed.get(self.e['State'].act, False):
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
   
    def spawn_boss(self):
        if self.boss is not None:
            return
       
        self.boss = Boss()
        self.e['EntityGroups'].add(self.boss, group='npc')
        self.stop_spawning = True
               
    def get_valid_spawn_slots(self):
        empty_slots = [i for i, n in enumerate(self.npcs) if n is None]
        if not empty_slots:
            return []
       
        occupied_slots = [i for i, n in enumerate(self.npcs) if n is not None]
       
        valid_slots = []
        for slot in empty_slots:
            is_valid = True
            for occupied in occupied_slots:
                if abs(slot - occupied) < 2:
                    is_valid = False
                    break
            if is_valid:
                valid_slots.append(slot)
       
        if len(valid_slots) == 0:
            return empty_slots
       
        return valid_slots
   
    def spawn_npc(self):
        if self.stop_spawning:
            return
           
        valid_slots = self.get_valid_spawn_slots()
        if not valid_slots:
            return
       
        slot = random.choice(valid_slots)
        order = self.get_random_order_for_act()
        wait_time = self.get_act_wait_time()
        npc = NPC(self.rand_type(), self.complexity, self.POS[slot], order, wait_time)
        self.npcs[slot] = npc
        self.e['EntityGroups'].add(npc, group='npc')
       
        order_display = OrderDisplay(order, self.GUI_POS[slot], z=100)
        npc.order_display = order_display
        self.e['EntityGroups'].add(order_display, group='ui')
       
    def feed(self, food_type, slot):
        if food_type == FoodTypes.PLATE: 
            return
        
        if isinstance(self.e['State'].act, int) and self.e['State'].act == 10:
            if self.boss and self.boss.alive:
                self.boss.take_dmg(food_type, slot)

                for group_name, group in self.e['EntityGroups'].groups.items():
                    for item in list(group):
                        if hasattr(item, 'food_type'):
                            if not isinstance(item, OrderDisplay):
                                if item.food_type == food_type and item.on_plate == True:
                                    item.kill()
            return


        npc = self.npcs[slot]
        if npc and npc.alive:
            if npc.is_grandmother:
                if food_type == npc.order:
                    self.e['State'].grandmother_order_completed[self.e['State'].act] = True
                    
                    if npc.order_display and npc.order_display in self.e['EntityGroups'].groups.get('ui', []):
                        self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                    if npc in self.e['EntityGroups'].groups.get('npc', []):
                        self.e['EntityGroups'].groups['npc'].remove(npc)
                    self.npcs[slot] = None
                    
                    for group_name, group in self.e['EntityGroups'].groups.items():
                        for item in list(group):
                            if hasattr(item, 'food_type'):
                                item.kill()
                   
                    self.e['Transition'].transition(lambda: (
                        self.e['State'].__setattr__('act_complete', True),
                        self.e['State'].__setattr__('gameplay_stop', True),
                        self.e['State'].__setattr__('act', self.e['State'].act + 1)
                    ))
                    self.grandmother_spawned = False
                   
                else:
                    if npc.order_display and npc.order_display in self.e['EntityGroups'].groups.get('ui', []):
                        self.e['EntityGroups'].groups['ui'].remove(npc.order_display)
                    if npc in self.e['EntityGroups'].groups.get('npc', []):
                        self.e['EntityGroups'].groups['npc'].remove(npc)
                    self.npcs[slot] = None
                   
                    for group_name, group in self.e['EntityGroups'].groups.items():
                        for item in list(group):
                            if hasattr(item, 'food_type'):
                                item.kill()
                    
                    self.e['State'].act = 'miss_dish'
                    self.e['State'].act_complete = False
                    self.grandmother_spawned = False
                    self.e['State'].gameplay_stop = True
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
                wait_time = self.get_act_wait_time()
                progress = max(0, npc.timer / (wait_time + self.e['State'].extra_wait_time))
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
    
    def draw_boss_hud(self, surface):
        if not self.boss or not self.boss.alive:
            return
        
        font = self.e['Text']['font']
        
        health_text = f"HP: {self.boss.health}/{self.boss.max_health}"
        text_width = font.width(health_text)
        
        x = (surface.get_width() - text_width) // 2
        y = 10
        
        font.render(surface, health_text, (x, y), color=(255, 50, 50))
                   
    def update(self, dt, surf):
        act = self.e['State'].act
       
        if self.yuki_pause_timer > 0:
            self.yuki_pause_timer -= dt
            if self.yuki_pause_timer <= 0:
                self.stop_spawning = False
            return
       
        if isinstance(act, int):
            if act in [0, 1, 2]:
                self.spawn_grandmother()
       
            if act == 10:
                if self.boss is None:
                    self.e['Transition'].transition(lambda: self.spawn_boss())
                    
                elif self.boss.alive:
                    self.boss.update(dt)
                    self.draw_boss_hud(surf)
                    
                else:
                    if self.boss in self.e['EntityGroups'].groups.get('npc', []):
                        self.e['EntityGroups'].groups['npc'].remove(self.boss)
                    
                    self.boss = None
                    
                    self.e['Transition'].transition(lambda: (
                        self.e['State'].__setattr__('act_complete', True),
                        self.e['State'].__setattr__('gameplay_stop', True),
                        self.e['State'].__setattr__('act', self.e['State'].act + 1)
                    ))
                           
                    for food in self.e['EntityGroups'].groups.get('food', []):
                        food.kill()
                    self.e['Game'].load_activities()
                    self.e['NPCPlacement'].reset_all_npcs()
       
            if act in self.ACT_SPAWN_DELAYS and not self.stop_spawning and act != 10:
                self.spawn_timer -= dt
                if self.spawn_timer <= 0:
                    self.spawn_npc()
                    self.spawn_timer = self.get_act_spawn_delay()

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
                        
                        self.e['EntityGroups'].groups.get('npc', []).remove(npc)