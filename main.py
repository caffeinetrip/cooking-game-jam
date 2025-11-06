import pygame
import scripts.pygpen as pp
from scripts.default.settings import Settings
from scripts.default.transition import Transition
from scripts.food.food import Food, FoodTypes
from scripts.food.activities_objects import *
class Game(pp.PygpenGame):
    def load(self):
        base_resolution = (384, 216)
        
        pygame.mixer.pre_init(channels=2, allowedchanges=pygame.AUDIO_ALLOW_FREQUENCY_CHANGE)
        pygame.init()
        
        self.settings = Settings()
        
        pp.init(
            self.settings.resolution,
            sounds_path='data/sfx',
            caption='BLOOD PLATE SPECIAL',
            input_path='data/config/key_mappings_default.json',
            font_path='data/fonts',
            fps_cap=60,
            opengl=True,
            frag_path='data/shaders/main.frag',
        )
        
        self.display = pygame.Surface(base_resolution, pygame.SRCALPHA)
        
        self.hud_surf = self.display.copy()
        
        self.e['Assets'].load_folder('data/images/misc', colorkey=(0, 0, 0), alpha=True)
        self.e['Assets'].load_folder('data/images/food', colorkey=(0, 0, 0), alpha=True)
        self.e['Assets'].load_folder('data/images/activities', colorkey=(0, 0, 0), alpha=True)
        
        self.e['Renderer'].set_groups(['default', 'ui'])
        
        self.mpos = (0, 0)
        self.freeze_stack = []
        
        self.noise_tex = self.e['MGL'].pg2tx(self.e['Assets'].images['misc']['noise'])
        self.noise_tex.repeat_x = True
        self.noise_tex.repeat_y = True
        self.crt_filter_tex = self.e['MGL'].pg2tx(self.e['Assets'].images['misc']['crt_filter'])
        self.crt_filter_tex.repeat_x = True
        self.crt_filter_tex.repeat_y = True
        
        self.transition = Transition()
        self.camera = pp.Camera(base_resolution, slowness=0.2)
        
        self.restart()

    def restart(self):
        self.e['EntityDB'].load('data/images/food')
        self.e['EntityDB'].load('data/images/activities')
        self.spawn_food(FoodTypes.BRAIN, (200, 150))
        self.load_activities()

    def load_activities(self):
        self.storage = Storage()
        self.grill = Grill()
        self.slime = Slime()
        self.desk = Desk()
        self.plate_place = PlatePlace()
        self.plates = Plates()

        self.e['EntityGroups'].add([self.storage, self.slime, self.grill, self.desk, self.plate_place, self.plates], group='activities')

    def spawn_food(self, food_type: FoodTypes, pos):
        food = Food(food_type=food_type, pos=pos, z=10)
        self.e['EntityGroups'].add(food, group='food')
        return food

    def update(self):
        self.hud_surf.fill((0, 0, 0, 0))
        self.display.fill((0, 0, 0, 0))
        self.e['Sounds'].update()
        dt_scale = 1
        self.e['Window'].dt = min(self.e['Window'].dt * dt_scale, 0.1)

        if self.e['Input'].pressed('fullscreen'):
            if self.settings.fullscreen:
                self.settings.update('fullscreen', 'disabled')
            else:
                self.settings.update('fullscreen', 'enabled')
                
        if self.e['Input'].pressed('test'):
            self.slime.slots[0].get_item(self.e['EntityGroups'].groups['food'][0])

        window_aspect = self.e['Window'].dimensions[0] / self.e['Window'].dimensions[1]
        intended_aspect = 16 / 9
        
        if window_aspect >= intended_aspect:
            playable_area = pygame.Rect(0, 0, self.e['Window'].dimensions[1] * intended_aspect, self.e['Window'].dimensions[1])
            
        else:
            playable_area = pygame.Rect(0, 0, self.e['Window'].dimensions[0], self.e['Window'].dimensions[0] / intended_aspect)
            
        playable_area.x = (self.e['Window'].dimensions[0] - playable_area.width) / 2
        playable_area.y = (self.e['Window'].dimensions[1] - playable_area.height) / 2
        relative_mpos = ((self.e['Mouse'].pos[0] - playable_area.x) / playable_area.width, (self.e['Mouse'].pos[1] - playable_area.y) / playable_area.height)
        self.mpos = (relative_mpos[0] * self.display.get_width(), relative_mpos[1] * self.display.get_height())

        self.camera.update()

        for act in self.slime.slots + self.grill.slots + self.desk.slots + self.plate_place.slots:
            act.update(self.mpos)

        self.e['EntityGroups'].renderz(offset=self.camera)
        
        for act in self.slime.slots + self.grill.slots + self.desk.slots + self.plate_place.slots:
            if act.held and act.item:
                act.item.pos = [self.mpos[0]-8, self.mpos[1]-8]
                act.item.render(self.display, offset=self.camera)

        self.transition.update()
        self.transition.render()

        self.e['Renderer'].cycle({'default': self.display, 'ui': self.hud_surf})
        
        self.e['Window'].cycle({
            'surface': self.display,
            'hud_surf': self.hud_surf,
            'time': self.e['Window'].runtime,
            'scroll': self.camera.int_pos,
            'border_discard': self.e['Window'].border_discard,
            'saturation': self.e['Settings'].saturation,
            'crt_filter_tex': self.crt_filter_tex,
            'dimensions': self.e['Window'].dimensions,
            'crt_effect': self.e['Settings'].crt_effect,
        })

Game().run()