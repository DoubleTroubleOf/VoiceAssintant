import json, os

def write_to_file(data):
    with open('search_opts.dat', 'w') as json_file:
        json_file.writelines(data.decode())

def read_from_file():
    content = ''
    with open(r'{0}\search_opts.dat'.format(os.getcwd() ), 'r') as json_file:
        content = json_file.read()
    
    datastore = json.loads(content)
    return datastore
