
import pygame

import scripts.pygpen as pp
from scripts.default.settings import Settings
from scripts.default.transition import Transition
from scripts.food.food import Food, FoodTypes

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

        #self.e['Sounds'].play('ambience', times=-1, volume=self.e['Settings'].sfx_volume * 0.6)
        
        self.restart()

    def restart(self):
        self.e['EntityDB'].load('data/images/food')
        self.spawn_food(FoodTypes.BRAIN, (200, 150))
        self.spawn_food(FoodTypes.HEART, (100, 150))

    def spawn_food(self, food_type: FoodTypes, pos):
        food = Food(food_type=food_type, pos=pos, z=10)
        self.e['EntityGroups'].add(food, group='food')
        return food
    
    def update(self):
        self.hud_surf.fill((0, 0, 0, 0))
        self.display.fill((0, 0, 0, 0))

        self.e['Sounds'].update()
        
        dt_scale = 1
        
        # if self.e['State'].effect_active('slow_motion'):
        #     dt_scale *= 0.65

        self.e['Window'].dt = min(self.e['Window'].dt * dt_scale, 0.1)
        
        if self.e['Input'].pressed('fullscreen'):
            if self.settings.fullscreen:
                self.settings.update('fullscreen', 'disabled')
            else:
                self.settings.update('fullscreen', 'enabled')
            
        window_aspect = self.e['Window'].dimensions[0] / self.e['Window'].dimensions[1]
        intended_aspect = 16 / 9
        if window_aspect >= intended_aspect:
            playable_area = pygame.Rect(0, 0, self.e['Window'].dimensions[1] * intended_aspect, self.e['Window'].dimensions[1])
        else:
            playable_area = pygame.Rect(0, 0, self.e['Window'].dimensions[0], self.e['Window'].dimensions[0] / intended_aspect)
        playable_area.x = (self.e['Window'].dimensions[0] - playable_area.width) / 2
        playable_area.y = (self.e['Window'].dimensions[1] - playable_area.height) / 2
        relative_mpos = ((self.e['Mouse'].pos[0] - playable_area.x) / playable_area.width, (self.e['Mouse'].pos[1] - playable_area.y) / playable_area.height)
        self.mpos = (relative_mpos[0] * self.e['Game'].display.get_width(), relative_mpos[1] * self.e['Game'].display.get_height())

        self.camera.update()

        self.e['EntityGroups'].renderz(offset=self.camera)
        
        self.transition.update()
        self.transition.render()

        # self.hud.update()
        # self.hud.render()

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
