import os
import time
import re
import speech_recognition as sr
from fuzzywuzzy import fuzz

from playsound import playsound
from gtts import gTTS
from schedle_search import Search
from updateDB import API

import schedule_notification, work_with_json
from opts import opts, faculties, langs, days


APP_LANGUAGE = work_with_json.read_from_file()['language']

class Recognize():
    def __init__(self, options, lang):
        self.language = lang
        self.opts = options
        r = sr.Recognizer()
        micro = sr.Microphone()

        with micro as source:
            r.adjust_for_ambient_noise(source)  
                    
        self.speak(self.opts[self.language]['answers'][4] + self.opts[self.language]['answers'][5])

        STOP_LISTENING = r.listen_in_background(micro, self.callback)
    
    def speak(self, what):
        speak_engine = gTTS(text=what, lang=self.language[:2]) 

        file_name = 'answer.mp3'

        speak_engine.save(file_name)
        playsound(file_name, True)
        os.remove(file_name)
        print(what)

    def callback(self, recognizer, audio):
        try:
            voice = recognizer.recognize_google(audio, language=self.language).lower()
            # LOG
            print('[log] Распознано: ' + voice)

            if voice.startswith(self.opts[self.language]['alias']):
                cmd = voice

                for name in self.opts[self.language]['alias']:
                    cmd = cmd.replace(name, '').strip()
                for verb in self.opts[self.language]['tbr']:
                    cmd = cmd.replace(verb, '').strip()
                
                temp_cmd = cmd

                cmd = self.recognize_cmd(cmd)

                Execution(self).execute_cmd(cmd['cmd'], temp_cmd)
        except sr.UnknownValueError:
            # LOG
            print('[log] Голос не распознан!')
        except sr.RequestError:
            # LOG
            print('[log] Неизвесная ошибка, проверьте интернет!')


    def recognise_day(self, temp_cmd):
        RC = {'day': '', 'percent': 0}
        for key, value in days[self.language].items():
            for item in value:
                vrt = fuzz.partial_ratio(temp_cmd, item)
                if vrt > RC['percent']:
                    RC['day'] = key
                    RC['percent'] = vrt
        return RC

    # check for what day find schedule
    def recognise_new_lang(self, temp_cmd):
        RC = {'lang': '', 'percent': 0}
        for key, value in langs.items():
            for item in value:
                vrt = fuzz.partial_ratio(temp_cmd, item)
                if vrt > RC['percent']:
                    RC['lang'] = key
                    RC['percent'] = vrt
        return RC

    # recognition of command to do
    def recognize_cmd(self, cmd):
        RC = {'cmd': '', 'percent': 0}
        for key, value in self.opts[self.language]['cmds'].items():
            for item in value:
                vrt = fuzz.partial_ratio(cmd, item)
                if vrt > RC['percent']:
                    RC['cmd'] = key
                    RC['percent'] = vrt
        return RC

    def recognise_grp_fac(self, temp_cmd):
        temp_cmd = temp_cmd.split()
        group, fac = None, None
        
        for item in temp_cmd:
            if re.match(r"факуль[\w]+", item):
                fac = temp_cmd[temp_cmd.index(item) + 1]
            if re.match(r"[\d]+", item):
                group = item
        if fac is None: 
            return None, group
        RC = {'fac': '', 'percent': 0}
        for item in faculties:
            vrt = fuzz.partial_ratio(fac.upper(), item)
            if vrt > RC['percent']:
                RC['fac'] = item
                RC['percent'] = vrt
        return RC["fac"], group



class Execution(Recognize):
    def __init__(self, data):
        self.data = data

    # start execution of command
    def execute_cmd(self, cmd, temp_cmd):
        command_dict = {
            "update": self.update_db,
            "user": self.change_user_data,
            "lang": self.change_lang,
            "schedule": self.get_scheudle,

        }
        if cmd != "":
            command_dict[cmd](temp_cmd)
        

    def change_user_data(self, temp_cmd):
        fac, group = self.data.recognise_grp_fac(temp_cmd)

        if fac not in faculties or (fac is None or group is None):
            self.data.speak(opts[APP_LANGUAGE]['answers'][10])
            return None
        
        data = work_with_json.read_from_file()
        data["department"] = fac
        data["group"] = group

        work_with_json.write_to_file(data)

        self.data.speak(self.data.opts[self.data.language]['answers'][11] + fac + " " + group)

    def change_lang(self, temp_cmd):
        new_lang = self.data.recognise_new_lang(temp_cmd)['lang']
        self.data.language = new_lang
        content = work_with_json.read_from_file()
        content['language'] = self.data.language
        work_with_json.write_to_file(content)
        global langs
        self.data.speak("{0} {1}".format(self.data.opts[self.data.language]['answers'][3], langs[new_lang][2] ))



    def get_scheudle(self, temp_cmd):
        try:
            day = self.data.recognise_day(temp_cmd)
            content = work_with_json.read_from_file()
            res = Search().find_file(content['group'], content['department'], day['day'])
            if res == -1:
                raise Exception()
            message = schedule_notification.notification()
            text = self.parse_schedule_result(res)
            self.data.speak(text)
            message.send_schedule(text)
        except Exception as e:
            print(e)
            self.data.speak(self.data.opts[self.data.language]['answers'][10])

    # transform result to readable view
    def parse_schedule_result(self, schedule):
        lang = self.data.language
        opts1 = self.data.opts
        if len(schedule) == 0:
            
            return opts1[lang]['answers'][0]
        result = """{count}{count_number};\n""".format(count=opts1[lang]['answers'][8],
                                                    count_number=len(schedule))

        for lesson in schedule:
            res = """{number}.   {name},  {clas} {cabinet};                      
    {teacher}   {teacher_name};""".format(number=lesson[0][-1],  
                                        name=lesson[1], cabinet=lesson[2], 
                                        clas=opts1[lang]['answers'][1],
                                        teacher=opts1[lang]['answers'][2],
                                        teacher_name=lesson[3])
            result += '\n{0}'.format(res)
        return result


    def update_db(self, temp_cmd):
        try:
            self.data.speak(self.data.opts[self.data.language]['answers'][6])
            rezult = API().update()
            if rezult == 0:
                self.data.speak(self.data.opts[self.data.language]['answers'][9])
        except Exception as exception:
            exception.msg = "asdasd"
            self.data.speak(self.data.opts[self.data.language]['answers'][10])


if __name__ == "__main__":
    r = Recognize(opts, APP_LANGUAGE)


    while True:
        time.sleep(0.1)
