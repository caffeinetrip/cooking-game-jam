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

BUFFS = [
    {
        'id': 'speed_cooking',
        'name': {
            'russian': 'Быстрая готовка',
            'english': 'Fast Cooking'
        },
        'description': {
            'russian': 'Еда готовится на гриле в 1.5 раза быстрее',
            'english': 'Food cooks 1.5x faster on the grill'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'extra_damage',
        'name': {
            'russian': 'Острые ножи',
            'english': 'Sharp Knives'
        },
        'description': {
            'russian': 'Вся еда наносит на 5 единиц урона больше',
            'english': 'All food deals 5 extra damage'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'bonus_points',
        'name': {
            'russian': 'Щедрые клиенты',
            'english': 'Generous Customers'
        },
        'description': {
            'russian': 'Получайте дополнительные очки за убийство посетителей',
            'english': 'Gain bonus points for killing visitors'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'fried_bonus',
        'name': {
            'russian': 'Мастер жарки',
            'english': 'Frying Master'
        },
        'description': {
            'russian': 'Жареная еда наносит на 20% больше урона',
            'english': 'Fried food deals 20% more damage'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'extra_heart',
        'name': {
            'russian': 'Дополнительная жизнь',
            'english': 'Extra Life'
        },
        'description': {
            'russian': 'Получите дополнительное сердце здоровья',
            'english': 'Gain an extra heart of health'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'extra_second',
        'name': {
            'russian': 'Больше времени',
            'english': 'More Time'
        },
        'description': {
            'russian': 'Посетители ждут на 1 секунду дольше',
            'english': 'Visitors wait 1 second longer'
        },
        'type': 'gameplay',
        'repeatable': True
    },
    {
        'id': 'time_slow',
        'name': {
            'russian': 'Замедление времени',
            'english': 'Time Slowdown'
        },
        'description': {
            'russian': 'Недели проходят медленнее (x2 время)',
            'english': 'Weeks pass slower (x2 time)'
        },
        'type': 'gameplay',
        'repeatable': False
    },
    {
        'id': 'lore_positive',
        'name': {
            'russian': 'Позитивная карта',
            'english': 'Positive Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_negative',
        'name': {
            'russian': 'Негативная карта',
            'english': 'Negative Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_hard',
        'name': {
            'russian': 'Карта прогрессии',
            'english': 'Progression Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_suicide',
        'name': {
            'russian': 'Опасная карта',
            'english': 'Dangerous Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_lefthand',
        'name': {
            'russian': 'Карта левой руки',
            'english': 'Left Hand Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_vibe',
        'name': {
            'russian': 'Карта вайба',
            'english': 'Vibe Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_sunflower',
        'name': {
            'russian': 'Карта подсолнуха',
            'english': 'Sunflower Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_album',
        'name': {
            'russian': 'Карта альбома',
            'english': 'Album Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_int',
        'name': {
            'russian': 'Карта интеллекта',
            'english': 'Intelligence Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_bass',
        'name': {
            'russian': 'Карта баса',
            'english': 'Bass Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_drill',
        'name': {
            'russian': 'Карта дрели',
            'english': 'Drill Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_pringles',
        'name': {
            'russian': 'Карта принглс',
            'english': 'Pringles Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_cards',
        'name': {
            'russian': 'Карта карт',
            'english': 'Cards Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
    {
        'id': 'lore_potato',
        'name': {
            'russian': 'Карта картошки',
            'english': 'Potato Card'
        },
        'description': {
            'russian': 'Загадочная карта. Детали неизвестны.',
            'english': 'Mysterious card. Details unknown.'
        },
        'type': 'lore',
        'repeatable': False
    },
]

GAME_OVER_TEXTS = {
    'russian': [
        'Акико был зарезан одним из клиентов...',
        'Безумный посетитель расправился с Акико.',
        'Акико не смог выжить в этом кошмаре.',
        'Клиент оказался быстрее. Акико мертв.',
        'История Акико закончилась трагически.'
    ],
    'english': [
        'Akiko was killed by one of the customers...',
        'A mad visitor dealt with Akiko.',
        'Akiko could not survive this nightmare.',
        'The customer was faster. Akiko is dead.',
        'Akiko\'s story ended tragically.'
    ]
}

KNIFE_WARNING = {
    'russian': 'У тебя нет ножа для резки',
    'english': 'You don\'t have a knife for cutting'
}

dialogues = {
    'intro': {
        'russian': [
            ('akiko', 'Акико. 32 года, не женат, девственник и безработный.'),
            ('akiko', 'Я так давно не выбирался из дома... бездушные предки.'),
            ('akiko', 'Выгнали меня работать в общепит к бабушке.'),
            ('grandmother', 'Идиот.'),
            ('akiko', '*Спасибо.'),
            ('grandmother', 'С сегодняшнего дня ты у меня работаешь.'),
            ('grandmother', 'Ты будешь выполнять всю работу.'),
            ('akiko', 'А можно... домой?'),
            ('grandmother', 'Ну, попробуй... что-ж.'),
            ('grandmother', 'Для начала.. обслужи меня.'),
        ],
        'english': [
            ('akiko', 'Akiko. 32 years old, unmarried, virgin and unemployed.'),
            ('akiko', 'I haven\'t left the house in so long... soulless ancestors.'),
            ('akiko', 'They kicked me out to work at grandma\'s diner.'),
            ('grandmother', 'Idiot.'),
            ('akiko', '*Thank you.'),
            ('grandmother', 'From today, you work for me.'),
            ('grandmother', 'You will do all the work.'),
            ('akiko', 'Can I... go home?'),
            ('grandmother', 'Well, try... alright then.'),
            ('grandmother', 'First... serve me.'),
        ]
    },

    'miss_dish': {
        'russian': [
            ('grandmother', 'До чего же ты тупой!'),
            ('grandmother', 'Ещё раз — дай то, что я прошу.'),
            ('grandmother', 'Либо ты УМРЁШЬ.'),
        ],
        'english': [
            ('grandmother', 'How stupid you are!'),
            ('grandmother', 'Once again — give me what I ask for.'),
            ('grandmother', 'Or you will DIE.'),
        ]
    },

    'act1': {
        'russian': [
            ('grandmother', 'Нуу, вроде справился, сойдет.'),
            ('grandmother', 'Теперь добавь слизь в это.'),
            ('grandmother', 'Местные жители терпеть её не могут.'),
            ('akiko', 'Тогда зачем она здесь?'),
            ('grandmother', 'Ты правда хочешь это узнать?'),
            ('grandmother', 'Работай, придурок.'),
        ],
        'english': [
            ('grandmother', 'Well, seems you managed, acceptable.'),
            ('grandmother', 'Now add slime to this.'),
            ('grandmother', 'Locals can\'t stand it.'),
            ('akiko', 'Then why is it here?'),
            ('grandmother', 'Do you really want to know?'),
            ('grandmother', 'Get to work, moron.'),
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
        ],
        'english': [
            ('grandmother', 'Tastes like complete shit.'),
            ('akiko', '*Thank you!'),
            ('grandmother', 'Try frying something on the grill.'),
            ('grandmother', 'A few seconds.'),
            ('grandmother', 'And, by the way, thank you so much...'),
            ('akiko', 'Huh? You liked it after all?'),
            ('grandmother', 'I can finally...'),
            ('grandmother', 'Go on...'),
            ('grandmother', 'Vacation.'),
            ('grandmother', '*FOREVER.'),
            ('akiko', '*WHAT!?'),
            ('grandmother', 'Start frying, idiot!'),
            ('akiko', 'BUT...'),
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
        ],
        'english': [
            ('grandmother', 'Probably tasty. And by the way, for the future...'),
            ('grandmother', 'You should know something'),
            ('grandmother', 'This is not just a restaurant'),
            ('grandmother', 'These are not just visitors'),
            ('grandmother', 'Your life will also become complicated.'),
            ('grandmother', 'At any moment visitors can...'),
            ('grandmother', '*kill you.'),
            ('grandmother', 'Goodbye! I\'ll tell mom you did well!'),
            ('grandmother', 'You have 10 seconds to kill a visitor.'),
            ('grandmother', '*Either you or them!'),
            ('grandmother', 'To escape, you need to kill the owner.'),
            ('grandmother', '*Thank you for saving me.'),
            ('akiko', 'WHAT DO YOU MEAN!?'),
            ('grandmother', '*Children grow up so fast...'),
        ]
    },

    'kazu_knife': {
        'russian': [
            ('kazu', 'Эй, Акико!'),
            ('kazu', 'Бабушка передала тебе это.'),
            ('kazu', 'Теперь ты можешь резать ингредиенты на доске.'),
            ('akiko', 'Нож? Спасибо...'),
        ],
        'english': [
            ('kazu', 'Hey, Akiko!'),
            ('kazu', 'Grandma sent you this.'),
            ('kazu', 'Now you can cut ingredients on the board.'),
            ('akiko', 'A knife? Thanks...'),
        ]
    },

    'yuki_heart': {
        'russian': [
            ('yuki', 'Акико, у меня для тебя кое-что есть.'),
            ('yuki', 'Это... особый ингредиент.'),
            ('yuki', 'Сердца. Свежие сердца.'),
            ('akiko', 'Откуда ты это взял?'),
            ('yuki', '*Лучше не спрашивай.'),
        ],
        'english': [
            ('yuki', 'Akiko, I have something for you.'),
            ('yuki', 'This is... a special ingredient.'),
            ('yuki', 'Hearts. Fresh hearts.'),
            ('akiko', 'Where did you get this?'),
            ('yuki', '*Better not ask.'),
        ]
    },

    'act4': {
        'russian': [
            ('akiko', 'Первая неделя позади...'),
            ('akiko', 'Что за чертовщина происходит?'),
        ],
        'english': [
            ('akiko', 'First week behind...'),
            ('akiko', 'What the hell is going on?'),
        ]
    },

    'act7': {
        'russian': [
            ('akiko', 'Ещё одна неделя...'),
            ('akiko', 'Я всё ближе к свободе.'),
        ],
        'english': [
            ('akiko', 'Another week...'),
            ('akiko', 'I\'m getting closer to freedom.'),
        ]
    },

    'act10': {
        'russian': [
            ('akiko', 'Владелец... наконец-то.'),
            ('akiko', 'Пора заканчивать этот кошмар.'),
        ],
        'english': [
            ('akiko', 'The owner... finally.'),
            ('akiko', 'Time to end this nightmare.'),
        ]
    },
    
    'disclaimer': {
        'russian': 'Все действия выдуманы, и проходят в альтернативной Японии.',
        'english': 'All events are fictional and take place in an alternative Japan.'
    },
    
    'creator': {
        'russian': 'GAME CREATED BY SOMA    ',
        'english': 'GAME CREATED BY SOMA'
    }
}