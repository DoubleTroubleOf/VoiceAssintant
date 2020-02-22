import os, time, datetime
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import webbrowser
from  googleapiclient.discovery import build

import schedle_search, schedule_notification, work_with_json, updateDB
from opts import opts



app_language = work_with_json.read_from_file()['language']



langs = {
    'uk-Uk':('ukrainian', 'украинский'),
    'ru-Ru':('російська', 'russian'),
    'en-En':('англійська', 'английский' ),
}

days = {
    "uk-UK":
    {
        'today': ('сьогодні','зараз'),
        'after tommorow': ('післязавтра','після','через день'),
        'tommorow': ('завтра','потім'),
    },
    "ru-Ru":
    {
        'today': ('сегодня','сейчас'),
        'after tommorow': ('послезавтра','после','через день'),
        'tommorow': ('завтра','потом'),
    },
    "en-En":
    {
        'today': ('today','now'),
        'after tommorow': ('after tommorow','after','in one day'),
        'tommorow': ('tommorow','later'),
    },
}



# play audio
def speak(what):
    speak_engine = pyttsx3.init()

    voices = speak_engine.getProperty('voices')
    speak_engine.setProperty('voice', voices[5].id)
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


# check for what day find schedule
def recognise_day(temp_cmd):
    RC = {'day': '', 'percent': 0}
    for key, value in days[app_language].items():
        for x in value:
            vrt = fuzz.partial_ratio(temp_cmd,x)
            if vrt > RC['percent']:
                RC['day'] = key
                RC['percent'] = vrt
    return RC

# check for what day find schedule
def recognise_new_lang(temp_cmd):
    RC = {'lang': '', 'percent': 0}
    for key, value in langs.items():
        for x in value:
            vrt = fuzz.partial_ratio(temp_cmd,x)
            if vrt > RC['percent']:
                RC['lang'] = key
                RC['percent'] = vrt
    return RC

# transform result to readable view
def parse_schedule_result(schedule):
    if len(schedule) == 0:
        return opts[app_language]['answers'][0]
    result = """"""
    for lesson in schedule:
        res = """
{number}   {name}  {clas} {cabinet}
{teacher}   {teacher_name}""".format(number=lesson[0][-1],  
                                    name=lesson[1], cabinet=lesson[2], 
                                    clas=opts[app_language]['answers'][1],
                                    teacher=opts[app_language]['answers'][2],
                                    teacher_name=lesson[3])
        result += '\n{0}'.format(res)
    return result

def callback(recognizer, audio):
    global app_language
    name = day = new_lang = ''
    try:
        voice = recognizer.recognize_google(audio, language=app_language ).lower()
        
        # LOG
        print('[log] Распознано: ' + voice)

        if voice.startswith(opts[app_language]['alias']):
            cmd = voice

            for x in opts[app_language]['alias']:
                cmd = cmd.replace(x,'').strip()
            for x in opts[app_language]['tbr']:
                cmd = cmd.replace(x,'').strip()
            
            name = cmd
            
            day = recognise_day(name)
            for i in days[app_language][day['day']]:
                name = name.replace(i,'').strip()
            new_lang = recognise_new_lang(name)
            for i in langs[new_lang['lang']]:
                name = name.replace(i,'').strip()

            cmd = recognize_cmd(cmd)

            execute_cmd(cmd['cmd'], name, day, new_lang['lang'])
    
    except sr.UnknownValueError:
        # LOG
        print('[log] Голос не распознан!')
    except sr.RequestError:
        # LOG
        print('[log] Неизвесная ошибка, проверьте интернет!')


# recognition of command to do
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts[app_language]['cmds'].items():
        for x in v:
            vrt = fuzz.partial_ratio(cmd,x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


# start execution of command
def execute_cmd(cmd, name='', day = '', lang = ''):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'schedule':
        try:
            content = work_with_json.read_from_file()
            res = schedle_search.find_file(content['group'],content['department'],day['day'])
            print(res)
            message = schedule_notification.notification()
            message.send_schedule(parse_schedule_result(res))
        except Exception:
            print('Oooops!')

    elif cmd == 'find': # find music in Youtube
        speak('Сейчас включаю... Подождите')
        find_Music(name)
    elif cmd == 'update':
        speak('opts[app_language]['answers'][6]')
        rezult = updateDB.update()
        speak(rezult)
    elif cmd == 'lang':
        change_lang(lang)
    else:
        speak(opts[app_language]['answers'][6])

    return

def change_lang(new_lang):
    global app_language 
    app_language = new_lang
    content = work_with_json.read_from_file()
    content['language'] = app_language
    work_with_json.write_to_file(content)
    
    speak("{0} {1}".format(opts[app_language]['answers'][3], new_lang))

# function to find and play music
def find_Music(name):
    api_key = 'AIzaSyCAMGs2dO8TakW4zpSFgTV0OvBgvWO5mV8'

    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(  part="snippet",
        maxResults=1,
        q=name,
        type='video')

    res = req.execute()
    videoId = res['items'][0]['id']['videoId']
            #open new tab in browser
    url = "https://www.youtube.com/watch?v=" + videoId
    webbrowser.open_new_tab(url)

#start
r = sr.Recognizer()
micro = sr.Microphone(device_index=1)

with micro as source:
    r.adjust_for_ambient_noise(source)

speak(opts[app_language]['answers'][4])
speak(opts[app_language]['answers'][5])
r.listen_in_background(micro, callback)
while True:
    time.sleep(0.1)