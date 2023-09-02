import datetime

dt = datetime.datetime.now()

def appendLog(file:str, data:str):
    '''
    Appends a log line to the end of file.
    '''
    with open(file, '+at') as fil:
        fil.write(data)

def makeLine(id:str, msg:str, file:str):
    '''
    Creates a log line and appends it.
    '''
    curr_time = dt.strftime("%H:%M:%S")
    curr_time = "[" + curr_time + "]"
    data = curr_time+"#~%"+id+"~=>"+msg+"\n"
    appendLog(file,data)

def loadLog(file:str)->list:
    '''
    Loads the log and returns it
    '''
    with open(file) as fil:
        return fil.readlines()
    
def parseLog(log:list, accs:dict)->dict:
    '''Parses log and returns a dictionary containing the name, pfp, msg, and time of conversation.
    Could potentially be upgraded to only have unique names+pfp, with the pos of msg/time attached to name'''
    cached_accs = dict()
    data = {"name":[],"msg":[],"time":[],"pfp":[]}
    for line in log:
        line_data = line.split("~=>")
        log_msg = line_data[1]
        log_time_id = line_data[0].split("#~%")
        log_time = log_time_id[0]
        log_id = log_time_id[1]
        if log_id not in cached_accs: #caches an id if it was not already. data is always extracted from cache to make it faster
            print(f'Cacheing {log_id}.')
            cached_accs[log_id] = accs[log_id]    
        data["name"].append(cached_accs[log_id]["username"])
        data["pfp"].append(cached_accs[log_id]["profile"])
        data["msg"].append(log_msg.replace("\n",""))
        data["time"].append(log_time)
    
    return data

