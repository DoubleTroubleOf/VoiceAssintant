import datetime
import os,copy, os.path
import json

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
def calculate_week(day='today'):
    if day == 'tommorow':
        time_now = datetime.date.today() + datetime.timedelta(days=1)  
    elif day == 'after tommorow':
        time_now = datetime.date.today() + datetime.timedelta(days=2)  
    else:
        time_now = datetime.date.today()
    time_old = datetime.date(2019,9,1)
    diff = (time_now - time_old).days // 7
    week = 1 if int(diff)%2==0 else 2
    week_day = week_dictionary[time_now.weekday()]
    return week, week_day


# funcrion to find needed file with schedule
# and read it. After this function find needed
# lessons to current day
def find_file(group, depart, when='today'):
    week, day_week = calculate_week(when)

    reg = "{0}.{1}.".format(week, day_week)

    content = ''
    # check if file exsists in directory
    if os.path.isfile(r'{0}\Folder\group{1} {2}.txt'.format(os.getcwd(),depart,group)):
        with open(r'{0}\Folder\group{1} {2}.txt'.format(os.getcwd(),depart,group), 'r') as file:   # read file to get data
            content = file.read()
    else:
        print ("File not exist")

    #get json format from string
    datastore = json.loads(content)
    res = {}
    #get one day`s lessons
    for key in datastore.keys():
        if key.startswith(reg):
            res[key] = datastore[key]
    #print the rezult of search
    result = []
    for key, value in res.items():
        result.append( (key, value['discipline'], value['classroom'], value['teacher']) )
    return result
 


