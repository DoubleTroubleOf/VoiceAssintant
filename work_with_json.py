import json, os

def write_to_file(data):
    #json_data = json.dumps(data)
    with open('search_opts.json', 'w', encoding='utf-8') as json_file:
        #json.dump(data, json_file, ensure_ascii=False)
        data = json.dumps(data, ensure_ascii=False)
        json_file.write(data)

def read_from_file():
    content = ''
    with open('{0}\search_opts.json'.format(os.getcwd(), encoding='windows1251'), 'r') as json_file:
        content = json_file.read()
    
    datastore = json.loads(content, encoding='windows1251')
    return datastore
