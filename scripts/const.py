import os


VERSION = '0.0.1'


CWD = os.getcwd()

DEFAULT_SAVE = {
    'todo': 0
}

SETTINGS = {
    'fps_cap': {
        'name': 'FPS Cap',
        'options': ['30', '60', '90', '120', '144', '165', '240', 'uncapped'],
        'submenu': 'graphics',
    },
    'fullscreen': {
        'name': 'Fullscreen',
        'options': ['disabled', 'enabled'],
        'submenu': 'video',
    },
    'windowed_resolution': {
        'name': 'Windowed Resolution',
        'options': ['384x216', '768x432', '1152x648', '1536x864', '1920x1080', '2560x1440', '3840x2160', 'native'],
        'submenu': 'video',
    },
    'master_volume': {
        'name': 'Master Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },
    'sfx_volume': {
        'name': 'SFX Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },
    'music_volume': {
        'name': 'Music Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
        'submenu': 'audio',
    },

    'show_fps': {
        'name': 'Show FPS',
        'options': ['disabled', 'enabled'],
        'submenu': 'graphics',
    },
    'screenshake': {
        'name': 'Screenshake',
        'options': ['disabled', 'enabled'],
        'submenu': 'accessibility',
    },
    'saturation': {
        'name': 'Saturation',
        'options': ['70%', '80%', '90%', '95%', '100%'],
        'submenu': 'graphics',
    },
    'crt_effect': {
        'name': 'CRT Screen Effect',
        'options': ['0%', '25%', '50%', '75%', '100%'],
        'submenu': 'accessibility',
    }
}
