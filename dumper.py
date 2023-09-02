import json
import random, string


def load_accs(file:str):
    '''Loads all text from a json file.'''
    with open(file) as jsonfile:
        return json.load(jsonfile)
    
def update_accs(file:str,data:dict):
    '''
    Rewrites the json file by dumping data into it.
    '''
    with open(file, 'w') as jsonfile:
        json.dump(data,jsonfile, indent=4)

def get_rand_id() -> str:
    '''
    Generates a random id for account and returns it.
    '''
    id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    return id

def get_online_id() -> str:
    '''
    Generates a random id for online status and returns it.
    '''
    id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(12))
    return id

def get_id(name:str, accs:dict) -> str:
    '''Gets the id of a name'''
    for ids in accs:
        if accs[ids]["username"] == name:
            return ids
    return "0"

def name_exists(name:str, accs:dict) -> bool:
    '''Checks if name has already been taken.'''
    for ids in accs:
        if accs[ids]["username"] == name:
            return True
    return False

def add_nickname(id:str, accs:dict, nickname:str):
    '''Adds a nickname. By default, the nickname is username.'''
    pass
    
def all_online_clients(clients:dict, orig_sid) -> dict:
    '''
    Returns a dictionary containing details about all online clients.
    '''
    online_clients = {}
    online_clients["status"] = 2
    online_clients["clients"] = []
    for sid in clients:
        if sid == orig_sid:
            continue
        client_id = clients[sid]["online-id"]
        client_name = clients[sid]["name"]
        client_pfp = clients[sid]["pfp"]
        online_clients["clients"].append({"name":client_name, "pfp":client_pfp, "id":client_id})
    return online_clients
