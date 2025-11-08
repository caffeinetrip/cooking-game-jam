import pygame
import scripts.pygpen as pp
from scripts.default.settings import Settings
from scripts.default.transition import Transition
from scripts.default.state import State
from scripts.food.food import Food, FoodTypes
from scripts.food.activities_objects import *
from scripts.npc.npc import NPC, NPCPlacement
from scripts.default.hud import HUD
from scripts.dialogue_system.dialogue_system import DialogueCharacter, DialogueSystem
from scripts.default.const import dialogues
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
            fps_cap=60,
            opengl=True,
            frag_path='data/shaders/main.frag',
        )
        
        self.display = pygame.Surface(base_resolution, pygame.SRCALPHA)
        
        self.hud_surf = self.display.copy()
        
        self.state = State()
        
        self.npc_placemant = NPCPlacement()
        
        self.e['Assets'].load_folder('data/images/misc', colorkey=(0, 0, 0), alpha=True)
        self.e['Assets'].load_folder('data/images/food', colorkey=(0, 0, 0), alpha=True)
        self.e['Assets'].load_folder('data/images/activities', colorkey=(0, 0, 0), alpha=True)
        
        self.e['Text'].add_ttf('font', 'data/fonts/desert_v1/Desert 6.ttf', 16)
        
        self.e['Renderer'].set_groups(['default', 'ui'])
        self.e['Window'].background_img = pygame.image.load('data/images/background/background.png')
        
        self.mpos = (0, 0)
        self.freeze_stack = []

        self.dialogue_system = DialogueSystem()
        self.dialogue_system.load_dialogues(dialogues)
        
        self.hud = HUD()
        
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
        self.e['EntityDB'].load('data/images/npc')

        self.load_activities()

    def load_activities(self):
        self.storage = Storage()
        self.grill = Grill()
        self.slime = Slime()
        self.desk = Desk()
        self.plate_place = PlatePlace()
        self.plates = Plates()
        self.bar_couter = BarCouter()
        self.day = Day()

        self.e['EntityGroups'].add([self.storage, self.slime, self.grill, self.desk, self.plate_place, self.plates, self.bar_couter, self.day], group='activities')

    def update(self):
        self.hud_surf.fill((0, 0, 0, 0))
        self.display.blit(self.e['Window'].background_img)
        
        self.e['Sounds'].update()
        dt_scale = 1
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
        self.mpos = (relative_mpos[0] * self.display.get_width(), relative_mpos[1] * self.display.get_height())
        
        if not self.e['State'].gameplay_stop:
            self.npc_placemant.update(self.e['Window'].dt, self.hud_surf)
        
        self.camera.update()
        self.state.update(self.e['Window'].dt)
                
        self.hud.render(self.hud_surf)
        
        self.e['DialogueSystem'].update(self.e['Window'].dt)
        self.e['DialogueSystem'].render(self.hud_surf)
        
        if not self.e['State'].gameplay_stop:
            self.plate_place.update()
            self.bar_couter.update()
            self.slime.update()
            self.desk.update(self.mpos)
            self.grill.update(self.e['Window'].dt)
        
        for act in self.storage.slots + self.slime.slots + self.grill.slots + self.desk.slots + self.plate_place.slots + self.plates.slots + self.bar_couter.slots:
            act.update(self.mpos, self.e['Window'].dt)

        self.e['EntityGroups'].renderz(offset=self.camera)
        
        
        for act in self.storage.slots + self.slime.slots + self.grill.slots + self.desk.slots + self.plate_place.slots + self.plates.slots + self.bar_couter.slots:
            if act.held and len(act.item) > 0:
                for item in act.item:
                    item.pos = [self.mpos[0]-16, self.mpos[1]-16]
                    item.render(self.display, offset=self.camera)

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