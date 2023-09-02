from aiohttp import web
import socketio
import logger
import dumper

sio = socketio.AsyncServer(max_http_buffer_size=17_000_000)
app = web.Application()
sio.attach(app)

online_clients = {} # will have sid as main key, acc-id, online-id, name, pfp

async def index(request):
    '''Serve the client side application.'''
    
    with open('./files/index.html') as file:
        return web.Response(text=file.read(), content_type='text/html')
    
    
    
@sio.event
def connect(sid, environ):
    print(sid, "has connected to the server.")

@sio.on('recieve')
async def chat_message(sid, data):
    #recieved message will be msg. must add name and pfp
    acc = online_clients[sid]
    id = acc["acc-id"]
    data["pfp"] = acc["pfp"]
    logger.makeLine(id,data["msg"],"log.txt")
    await send_msg(data)

async def send_msg(data):
    #data must be a dict of name, pfp, and msg
    await sio.emit('recieve', data)

@sio.on('login')
async def login_check(sid, data):
    name = data["username"]
    passw = data["password"]
    print(f"{sid} is trying to login with Username:{name} and Password:{passw}.")
    accs = dumper.load_accs("accs.json")
    for id in accs:
        if accs[id]["username"] == name:
            if accs[id]["password"] == passw:
                online_id = dumper.get_online_id()
                await sio.emit('login_result', (True, name, accs[id]["profile"]), sid) #sending success
                print(f"{sid} has successfully logged in using {name}.")
                await sio.emit('online-state', {"status":1, "name":name, "pfp":accs[id]["profile"],"id":online_id}) #sending client online status to all
                await sio.emit('online-state', {"status":3},sid) #m sending to let client create a header
                online_clients[sid] = {"online-id":online_id,"acc-id":id,"name":name,"pfp":accs[id]["profile"]} #adds the logged in client to a group of online clients
                curr_online_clients = dumper.all_online_clients(online_clients, sid) #creates a dict of all online clients except self
                await sio.emit('online-state',curr_online_clients,sid) #sends the list of online clients to the user that just logged in.
                return
    await sio.emit('login_result', (False), sid)
    print(f"Login failed for {sid}.")

@sio.on('signup')
async def signup_add(sid, data):
    try:
        name = data["username"]
        passw = data["password"]
        image_file = data["image"]
        user_id = ""

        accs = dumper.load_accs("accs.json")
        if dumper.name_exists(name, accs):
            print("Name already exists.")
            await sio.emit('signup',False,sid)    
            return
        while True:
            user_id = dumper.get_rand_id()
            if user_id in accs:
                continue #tries again and again till it gets a unique id.
            break
        img_name = "/pfp/"+user_id+".png"
        print(img_name)
        with open("files/"+img_name, 'wb') as img:
            img.write(image_file)
        accs[user_id] = {"username":name, "password":passw, "profile":img_name}
        dumper.update_accs("accs.json", accs)
        print("Account added.")
        await sio.emit('signup',True,sid)
    except:
        print("Failed to add account.")
        await sio.emit('signup',False,sid)

@sio.on('loadlog')
async def load_log(sid): #sends the parsed log to client
    log = logger.loadLog("log.txt")
    accs = dumper.load_accs("accs.json")
    parsed_logs = logger.parseLog(log, accs)
    await sio.emit('load',parsed_logs,sid) 

@sio.event
async def disconnect(sid):
    print(f"{sid} has disconnected from the server.")
    online_id = online_clients[sid]["online-id"]
    await sio.emit("online-state", {"status":0,"id":online_id})
    del online_clients[sid]

app.router.add_static('/static', './files')
app.router.add_get('/', index)

web.run_app(app)