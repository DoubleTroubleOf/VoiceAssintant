import datetime
import os,copy, os.path
import json
import sqlite3

class Search():
    week_dictionary = {
        0:'Пнд',
        1:'Втр',
        2:'Срд',
        3:'Чтв',
        4:'Птн',    
        5:'' ,   
        6:''    
    }

    #calculate if the week is odd or even
    def calculate_week(self, day='today'):
        if day == 'tommorow':
            time_now = datetime.date.today() + datetime.timedelta(days=1)  
        elif day == 'after tommorow':
            time_now = datetime.date.today() + datetime.timedelta(days=2)  
        else:
            time_now = datetime.date.today()
        time_old = datetime.date(2019,9,1)
        diff = (time_now - time_old).days // 7
        week = 1 if int(diff)%2==0 else 2
        week_day = self.week_dictionary[time_now.weekday()]
        return week, week_day
    

    # funcrion to find needed file with schedule
    # and read it. After this function find needed
    # lessons to current day
    def find_file(self, group, depart, when='today'):
        week, day_week = self.calculate_week(when)

        reg = "{0}.{1}.".format(week, day_week)

        content = ''
        try:
            conn = sqlite3.connect('database.db')
            conn.text_factory = lambda b: b.decode(errors = 'ignore')

            cur = conn.cursor()

            sql = "SELECT * FROM Shedules WHERE group_number=? AND faculty=?"

            vals = (int(group), depart)
            cur.execute(sql, vals)
            data = cur.fetchone()
            if data:
                content = data[2]
            else:
                raise Exception("Something goes wrong! \nTry again later.")    #розклад не знайдено
            datastore = json.loads(content)
            res = {}
            #get one day`s lessons
            for key in datastore.keys():
                if key.startswith(reg):
                    res[key] = datastore[key]
                    continue
            #print the rezult of search
            result = []
            for key, value in res.items():
                result.append( (key, value['discipline'], value['classroom'], value['teacher']) )
            return result
        except Exception as e:
            return -1


