import requests
import collections, json, codecs
import os,datetime,time
import sqlite3

#убираем дублирование групп в словаре по департаментах
def get_unique_items(list_of_dicts, key="NAME"):
    # Count how many times each key occurs.
    key_count = collections.defaultdict(lambda: 0)
    for d in list_of_dicts:
        key_count[d[key]] += 1

    return [d for d in list_of_dicts if key_count[d[key]] == 1]

# получаем коды всех подразделений университета
def get_dep_codes():
    response1 = requests.get('http://rozklad.nau.edu.ua/api/v1/departments')
    d = dict(response1.json())['departments']
    dep_codes = []
    for i in range(len(d)):
        dep_codes.append(d[i]['CODE'])
    return dep_codes

#получаем словарь групп готовый для дальнейшей обработки
def get_groups_by_deps(codes):
    groups = dict()
    for code in codes:
        response2 = requests.get('http://rozklad.nau.edu.ua/api/v1/groups/{0}'.format(code))
        group = response2.json()
        if group['status'] == True:
            groups[code] = group['groups']

    #список групп по департаментах
    grp = dict()
    for key in list(groups.keys()):
        grp[key] = get_unique_items(groups[key])
    return grp


def write_to_db(grp):
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        i = 0
        for values in grp.values():
            for v in values:
                response = requests.get('http://rozklad.nau.edu.ua/api/v1/schedule/{department_code}/{course}/{stream}/{group_code}'.format(department_code=v['DEP'],
                                                                                                                                            course=v['COURSE'], 
                                                                                                                                            stream=v['STRM'], 
                                                                                                                                            group_code=v['GRP'], 
                                                                                                                                            subgroup=1)
                                                                                                                                        )
                time.sleep(0.2)
                if response.ok == True and dict(response.json())['status'] == True:
                    shed = json.dumps(dict(response.json())["schedule"] , ensure_ascii=False).encode('utf-8')
                    fac, group =  v["NAME"].split()
                    group = int(group)
                    sql = "SELECT * FROM Shedules WHERE group_number = ? AND faculty = ?"
                    vals = (group, fac)
                    cur.execute(sql, vals)
                    
                    if cur.fetchone():
                        sql = "UPDATE Shedules SET shedule = ? WHERE group_number = ? AND faculty = ?"
                        vals = (shed.decode(), group, fac)
                    else:
                        sql = "INSERT INTO Shedules (group_number, faculty, shedule) VALUES (?, ?, ?)"
                        vals = (group, fac, shed.decode())

                    cur.execute(sql, vals)
                    conn.commit()
                i+=1
            i+=1
        print(i)
        conn.close()
    except Exception as e:
        print(e)

"""
===================================================================
"""

def update():
    try:
        dep_codes = get_dep_codes()

        ready_groups = get_groups_by_deps(dep_codes)

        write_to_db(ready_groups)
    except:
        raise Exception("Something goes wrong! \nTry again later.")
    return 0
