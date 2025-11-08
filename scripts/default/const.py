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
    },
    'fullscreen': {
        'name': 'Fullscreen',
        'options': ['disabled', 'enabled'],
    },
    'windowed_resolution': {
        'name': 'Windowed Resolution',
        'options': ['384x216', '768x432', '1152x648', '1536x864', '1920x1080', '2560x1440', '3840x2160', 'native'],
    },
    'master_volume': {
        'name': 'Master Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
    },
    'sfx_volume': {
        'name': 'SFX Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
    },
    'music_volume': {
        'name': 'Music Volume',
        'options': ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
    },
    'show_fps': {
        'name': 'Show FPS',
        'options': ['disabled', 'enabled'],
    },
    'screenshake': {
        'name': 'Screenshake',
        'options': ['disabled', 'enabled'],
    },
    'saturation': {
        'name': 'Saturation',
        'options': ['70%', '80%', '90%', '95%', '100%'],
    },
    'crt_effect': {
        'name': 'CRT Screen Effect',
        'options': ['0%', '25%', '50%', '75%', '100%'],
    },
    'language': {
        'name': 'Language',
        'options': ['english', 'russian'],
    }
}

dialogues = {
    'intro': {
        'russian': [
            ('akiko', 'Акико. 32 года, не женат, девственник и безработный.'),
            ('akiko', 'Я так давно не выбирался из дома... грёбаные предки.'),
            ('akiko', 'Выгнали меня работать к бабушке... В ресторан.'),
            ('grandmother', 'Идиот.'),
            ('akiko', '*Спасибо.'),
            ('grandmother', 'С сегодняшнего дня ты у нас работаешь.'),
            ('grandmother', 'Ты будешь выполнять всю работу.'),
            ('akiko', 'А можно... домой?'),
            ('grandmother', 'Ну, попробуй... что ж.'),
            ('grandmother', 'Для начала обслужи меня.'),
        ]
    },

    'miss_dish': {
        'russian': [
            ('grandmother', 'До чего же ты тупой!'),
            ('grandmother', 'Ещё раз — дай то, что я прошу.'),
            ('grandmother', 'Либо ты УМРЁШЬ.'),
        ]
    },

    'act1': {
        'russian': [
            ('grandmother', 'Ого, молодец, ты справился.'),
            ('grandmother', 'Теперь соедини это со слизью.'),
            ('grandmother', 'Местные жители больше всего её ненавидят.'),
            ('akiko', 'А зачем она здесь?'),
            ('grandmother', 'Ты правда хочешь это узнать?'),
            ('grandmother', 'Работай, придурок.'),
        ]
    },

    'act2': {
        'russian': [
            ('grandmother', 'На вкус полное дерьмо.'),
            ('akiko', '*Спасибо!'),
            ('grandmother', 'Попробуй ещё что-то на гриле пожарить.'),
            ('grandmother', 'Несколько секунд.'),
            ('grandmother', 'И, кстати, спасибо большое...'),
            ('akiko', 'А? Всё-таки понравилось?'),
            ('grandmother', 'Я наконец смогу...'),
            ('grandmother', 'Пойти в...'),
            ('grandmother', 'Отпуск.'),
            ('grandmother', '*НАВСЕГДА.'),
            ('akiko', '*ЧТО!?'),
            ('grandmother', 'Жарь давай, идиот!'),
            ('akiko', 'НО...'),
            ('grandmother', '*...'),
        ]
    },

    'guide_complete': {
        'russian': [
            ('grandmother', 'Наверное, это вкусно. И, кстати, на будущее...'),
            ('grandmother', 'Ты должен кое-что знать'),
            ('grandmother', 'Это не просто ресторан'),
            ('grandmother', 'Это не просто посетители'),
            ('grandmother', 'Твоя жизнь тоже станет не простой.'),
            ('grandmother', 'В любой момент посетители могут...'),
            ('grandmother', '*тебя убить.'),
            ('grandmother', 'Прощай! Я передам маме, что ты молодец!'),
            ('grandmother', 'У тебя есть 10 секунд, чтобы убить посетителя.'),
            ('grandmother', '*Либо ты, либо они!'),
            ('grandmother', 'Чтобы выбраться, тебе нужно убить владельца.'),
            ('grandmother', '*Спасибо, что спас меня.'),
            ('akiko', 'В СМЫСЛЕ!?'),
            ('grandmother', '*Так быстро дети растут...'),
        ]
    },
}
