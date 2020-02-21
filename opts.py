#TOKEN TO GET CONTROL OF TELEGRAM BOT
TOKEN = '1031615541:AAHzP4D7w7fhk5jhpsONRQgqShrfcP-y2Dw'

#TODO 
"""
========================

обновити словник 'opts' в якому будуть збережені всі фрази відповідей на різних мовах.

"""

#DICTIONARY WHICH IS MAIN TO CONTROL VOICE ASSISTANT
opts = {
    "ru-Ru": 
    {
        'alias': ('вася', 'василий', 'друг мой', 'друг', 'василиос', 'васька', 'василиса', 'васёк', 'васек', 'васенька', 'васян', 'слуга'),

        'tbr': ('скажи', 'розкажи', 'покажи', 'сколько', 'произнеси', 'включи', 'поищи', 'включи' , 'покажи', 'поменяй','измени', 'переведи',
                'обнови', 'обновить', 'загрузи', 'загрузить'),

        'cmds': 
        {
            'find': ('найди песню', 'найди клип','найди группу','найди групу', 'найди', 'ютуб', 'песня', 
                    'песню', 'группа', 'група', 'группу', 'групу', 'клип', 'видео', 'youtube', 'музыка', 'музика','музыку','музику'),

            'update': ('базу данных', 'база данных', 'база', 'базу', 'обнови рассписание', 'хранилище', 'данные', 'данние'),

            'lang': ('измени язык', 'поменяй язик', 'переведи интерфейс', 'переведи содержание', 'переведи','язик','язык'),

            'schedule': ('рассписание', 'пары', 'пари', 'занятия', 'пара', 'какие пары', 'какие пари'),
            
            'ctime': ('текущее время', 'сейчас времени', 'который час', 'время', 'посмотри на часы')       
        }
    },
    
    "uk-Uk" : 
    {
        'alias': ('вася', 'василь', 'друг мій', 'друг', 'друже', 'васька', 'василіса', 'васян'),

        'tbr': ('скажи', 'розкажи', 'покажи', 'скільки', 'промов','включи', 'пошукай','знайди', 
                'включи' , 'покажи', 'онови', 'оновити', 'завантажити', 'завантаж', 'загрузи'),

        'cmds': 
        {
            'find': ('знайди пісню', 'знайди кліп', 'знайди группу', 'знайди групу', 'знайди', 'ютуб', 'пісня',
                     'пісню', 'група','групу', 'кліп', 'відео', 'youtube'),
        
            'update': ('базу даних', 'база даних', 'база', 'базу', 'онови рассписание', 'сховище', 'дані', 'данні'),

            'lang': ('зміни мову', 'переклади інтерфейс', 'переклади вміст', 'переклади','поміняй мову','мову','мова',),

            'schedule': ('розклад', 'пари', 'заняття', 'пара', 'які пари', 'какие заняття'),
    
        }
    },

    "en-En" :
    {
        'alias': ('vasya', 'vasyl', 'my friend', 'friend', 'bro', 'brother', 'vaska', 'vasilisa'),

        'tbr': ('tell', 'show', 'speak', 'turn on', 'search', 'find', 'look for', 'demonstrate', 'update', 'download'),

        'cmds': 
        {
            'find': ('track', 'videoclip', 'group', 'youtube', 'music', 'song', 'soundа', 'band', 'artist'),

            'update': ('database', 'data', 'base', 'update data', 'update database', 'storage', 'update storage'),

            'lang': ('change language', 'language', 'languages', 'interface', 'translate interface', 'translate content', 'content'),

            'schedule': ('schedule', 'lessons', 'lesson', 'which lesson')
    
        }
    }

}
