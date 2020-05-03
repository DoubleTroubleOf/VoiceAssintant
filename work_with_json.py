import json, os

def write_to_file(data):
    #json_data = json.dumps(data)
    with open('search_opts.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)

def read_from_file():
    content = ''
    with open(r'{0}\search_opts.json'.format(os.getcwd() ), 'r', encoding='utf-8') as json_file:
        content = json_file.read()
    
    datastore = json.loads(content)
    return datastore
