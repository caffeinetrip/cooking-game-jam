import pygame

from scripts import pygpen as pp

TRACK_VOLUMES = {
    'todo': 0.3
}

TRACK_LENGTHS = {
    'todo': 100
}

class Music(pp.ElementSingleton):
    def __init__(self):
        super().__init__()

        self.fading = [0, 0]
        self.last_volume = 1.0
        self.last_track = None

    def update(self):
        last_volume = 0.5
        if self.last_track:
            last_volume = TRACK_VOLUMES[self.last_track] * self.e['Settings'].music_volume
        if self.fading[1]:
            self.fading[0] = max(0, self.fading[0] - self.e['Window'].dt)
            pygame.mixer.music.set_volume(last_volume * (self.fading[0] / self.fading[1])) 
        else:
            pygame.mixer.music.set_volume(last_volume) 

    def play(self, track, start=0, fadein=0):
        self.fading = [0, 0]
        start = start % TRACK_LENGTHS[track]
        pygame.mixer.music.load(f'data/music/{track}.wav')
        self.last_volume = TRACK_VOLUMES[track] * self.e['Settings'].music_volume
        self.last_track = track
        pygame.mixer.music.set_volume(self.last_volume)
        pygame.mixer.music.play(-1, start=start, fade_ms=int(fadein * 1000))

    def fadeout(self, duration):
        self.fading = [duration, duration]