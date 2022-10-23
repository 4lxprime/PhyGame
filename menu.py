from tkinter import *
import threading
import socket
import json
import time
import random
import os
import requests

api_url="http://127.0.0.1/phygame"
allsrv=[]

def stop():
    root.destroy()
    exit(0)

class Server():
    def __init__(self):
        self.ADDR="0.0.0.0"
        self.PORT=8000
        self.MAX_PLAYERS = 10
        self.MSG_SIZE = 2048
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ADDR, self.PORT))
        self.s.listen(self.MAX_PLAYERS)
        self.players = {}
        self.main()


    def generate_id(self, player_list: dict, max_players: int):
        while True:
            unique_id = str(random.randint(1, max_players))
            if unique_id not in player_list:
                return unique_id


    def handle_messages(self, identifier: str):
        client_info = self.players[identifier]
        conn: socket.socket = client_info["socket"]
        username = client_info["username"]

        while True:
            try:
                msg = conn.recv(self.MSG_SIZE)
            except ConnectionResetError:
                break

            if not msg:
                break

            msg_decoded = msg.decode("utf8")

            try:
                left_bracket_index = msg_decoded.index("{")
                right_bracket_index = msg_decoded.index("}") + 1
                msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
            except ValueError:
                continue

            try:
                msg_json = json.loads(msg_decoded)
            except Exception as e:
                print(e)
                continue

            if msg_json["object"] == "player":
                self.players[identifier]["position"] = msg_json["position"]
                self.players[identifier]["rotation"] = msg_json["rotation"]
                self.players[identifier]["health"] = msg_json["health"]

            for player_id in self.players:
                if player_id != identifier:
                    player_info = self.players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.sendall(msg_decoded.encode("utf8"))
                    except OSError:
                        pass

        # Tell other players about player leaving
        for player_id in self.players:
            if player_id != identifier:
                player_info = self.players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.send(json.dumps({"id": identifier, "object": "player", "joined": False, "left": True}).encode("utf8"))
                except OSError:
                    pass

        print(f"Player {username} with ID {identifier} has left the game...")
        del self.players[identifier]
        conn.close()


    def main(self):
        print("Server started, listening for new connections...")

        while True:
            conn, addr = self.s.accept()
            new_id =self.generate_id(self.players, self.MAX_PLAYERS)
            conn.send(new_id.encode("utf8"))
            username = conn.recv(self.MSG_SIZE).decode("utf8")
            new_player_info = {"socket": conn, "username": username, "position": (0, 1, 0), "rotation": 0, "health": 100}

            for player_id in self.players:
                if player_id != new_id:
                    player_info = self.players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.send(json.dumps({
                            "id": new_id,
                            "object": "player",
                            "username": new_player_info["username"],
                            "position": new_player_info["position"],
                            "health": new_player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                    except OSError:
                        pass

            for player_id in self.players:
                if player_id != new_id:
                    player_info = self.players[player_id]
                    try:
                        conn.send(json.dumps({
                            "id": player_id,
                            "object": "player",
                            "username": player_info["username"],
                            "position": player_info["position"],
                            "health": player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                        time.sleep(0.1)
                    except OSError:
                        pass

            self.players[new_id] = new_player_info

            msg_thread = threading.Thread(target=self.handle_messages, args=(new_id,), daemon=True)
            msg_thread.start()

            print(f"New connection from {addr}, assigned ID: {new_id}...")

class Bullet_Server():
    def __init__(self):
        self.ADDR="0.0.0.0"
        self.PORT=8001
        self.MAX_PLAYERS = 10
        self.MSG_SIZE = 2048
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ADDR, self.PORT))
        self.s.listen(self.MAX_PLAYERS)
        self.players = {}
        self.main()


    def generate_id(self, player_list: dict, max_players: int):
        while True:
            unique_id = str(random.randint(1, max_players))
            if unique_id not in player_list:
                return unique_id


    def handle_messages(self, identifier: str):
        client_info = self.players[identifier]
        conn: socket.socket = client_info["socket"]
        username = client_info["username"]

        while True:
            try:
                msg = conn.recv(self.MSG_SIZE)
            except ConnectionResetError:
                break

            if not msg:
                break

            msg_decoded = msg.decode("utf8")

            try:
                left_bracket_index = msg_decoded.index("{")
                right_bracket_index = msg_decoded.index("}") + 1
                msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
            except ValueError:
                continue

            try:
                msg_json = json.loads(msg_decoded)
            except Exception as e:
                print(e)
                continue

            if msg_json["object"] == "player":
                self.players[identifier]["position"] = msg_json["position"]
                self.players[identifier]["rotation"] = msg_json["rotation"]
                self.players[identifier]["health"] = msg_json["health"]

            for player_id in self.players:
                if player_id != identifier:
                    player_info = self.players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.sendall(msg_decoded.encode("utf8"))
                    except OSError:
                        pass

        for player_id in self.players:
            if player_id != identifier:
                player_info = self.players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.send(json.dumps({"id": identifier, "object": "player", "joined": False, "left": True}).encode("utf8"))
                except OSError:
                    pass

        print(f"Player {username} with ID {identifier} has left the game...")
        del self.players[identifier]
        conn.close()


    def main(self):
        print("Server started, listening for new connections...")

        while True:
            conn, addr = self.s.accept()
            new_id =self.generate_id(self.players, self.MAX_PLAYERS)
            conn.send(new_id.encode("utf8"))
            username = conn.recv(self.MSG_SIZE).decode("utf8")
            new_player_info = {"socket": conn, "username": username, "position": (0, 1, 0), "rotation": 0, "health": 100}

            self.players[new_id] = new_player_info

            msg_thread = threading.Thread(target=self.handle_messages, args=(new_id,), daemon=True)
            msg_thread.start()

            print(f"New connection from {addr}, assigned ID: {new_id}...")

def get_serv():
    url=f"{api_url}/getserv.php"
    try:
        r=requests.get(url).json()
        print(r)
        if r!="error":
            return r
        else:
            return False
    except Exception as e:
        pass

root=Tk()

root.geometry("800x500")
root.minsize(800, 500)
root.title("  PhyGame 1.2")

canvas=Canvas(root, 
    bg="#23272e", 
    width=800,
    height=500
)

top=canvas.create_rectangle(
    0, 0, 
    root.maxsize()[0], 80,
    outline="black", 
    fill="#1c1c1c"
)

root.update()

Tt=canvas.create_text(root.winfo_width()/2, 40, 
    text="PhyGame", 
    font=('Helvetica 30 bold'), 
    fill="white"
)

cred=canvas.create_window(
    root.winfo_width()-60, root.winfo_height()-30, 
    window=Button(root, 
        font=("Arial", 15), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=7, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Credits"
    )
)

def getServ():
    url=f"{api_url}/get/dispatch.php"
    r=requests.get(url).json()
    if r!="error":
        return list(r)
    else:
        return False

def STG():
    for i in allsrv:
        canvas.itemconfigure(globals()[i], state="hidden")
    But1B['bg']="#1a1d21"
    But2B['bg']="#1e2227"
    But3B['bg']="#1e2227"
    canvas.itemconfigure(Auto, state="normal")
    canvas.itemconfigure(Manual, state="normal")
    canvas.itemconfigure(HostPub, state="hidden")
    canvas.itemconfigure(HostPrv, state="hidden")
    canvas.itemconfigure(Ti, state="hidden")
    canvas.itemconfigure(IPc, state="hidden")
    canvas.itemconfigure(PORTc, state="hidden")
    canvas.itemconfigure(VldIP, state="hidden")
    canvas.itemconfigure(MSTxt, state="hidden", text="")

def HTG():
    for i in allsrv:
        canvas.itemconfigure(globals()[i], state="hidden")
    But1B['bg']="#1e2227"
    But2B['bg']="#1a1d21"
    But3B['bg']="#1e2227"
    canvas.itemconfigure(Auto, state="hidden")
    canvas.itemconfigure(Manual, state="hidden")
    canvas.itemconfigure(HostPub, state="normal")
    canvas.itemconfigure(HostPrv, state="normal")
    canvas.itemconfigure(Ti, state="hidden")
    canvas.itemconfigure(IPc, state="hidden")
    canvas.itemconfigure(PORTc, state="hidden")
    canvas.itemconfigure(VldIP, state="hidden")
    canvas.itemconfigure(MSTxt, state="hidden", text="")

def GI():
    for i in allsrv:
        canvas.itemconfigure(globals()[i], state="hidden")
    But1B['bg']="#1e2227"
    But2B['bg']="#1e2227"
    But3B['bg']="#1a1d21"
    canvas.itemconfigure(Auto, state="hidden")
    canvas.itemconfigure(Manual, state="hidden")
    canvas.itemconfigure(HostPub, state="hidden")
    canvas.itemconfigure(HostPrv, state="hidden")
    canvas.itemconfigure(Ti, state="normal")
    canvas.itemconfigure(IPc, state="hidden")
    canvas.itemconfigure(PORTc, state="hidden")
    canvas.itemconfigure(VldIP, state="hidden")
    canvas.itemconfigure(MSTxt, state="hidden", text="")


def MS():
    for i in allsrv:
        canvas.itemconfigure(globals()[i], state="hidden")
    canvas.itemconfigure(Auto, state="hidden")
    canvas.itemconfigure(Manual, state="hidden")
    canvas.itemconfigure(IPc, state="normal")
    canvas.itemconfigure(PORTc, state="normal")
    canvas.itemconfigure(VldIP, state="normal")
    canvas.itemconfigure(MSTxt, state="hidden", text="")

def ConnMS():
    canvas.itemconfigure(MSTxt, state="normal", text="")
    canvas.itemconfigure(VldIP, state="normal")
    ip=IPe.get()
    port=PORTe.get()
    if not ip=="" or not port=="":
        if "." in ip:
            if int(port):
                print("ok")
            else:
                canvas.itemconfigure(MSTxt, text=f"Bad Port: {port}")
        else:
            canvas.itemconfigure(MSTxt, text=f"Bad Ip: {ip}")
    else:
        canvas.itemconfigure(MSTxt, text=f"Bad Ip or Port: {ip}:{port}")
        
    if os.path.exists(f"{os.path.realpath(os.path.dirname(__file__))}/player/game.exe"):
        os.startfile(f"{os.path.realpath(os.path.dirname(__file__))}/player/game.exe")
        canvas.itemconfigure(MSTxt, text=f"Connecting To: {ip}:{port}")
    else:
        canvas.itemconfigure(MSTxt, text=f"Error: The games files is not in:\n{os.path.realpath(os.path.dirname(__file__))}/player/game.exe")

def startGame(srv: dict):
    ip=srv["server_ip"]
    port=srv["server_port"]
    plr=srv["servers_players"]
    bull_ip=srv["bullet_server_ip"]
    bull_port=srv["bullet_server_port"]
    print(srv)
    canvas.itemconfigure(MSTxt, state="normal", text="")
    if os.path.exists(f"{os.path.realpath(os.path.dirname(__file__))}/player/game.exe"):
        os.startfile(f"{os.path.realpath(os.path.dirname(__file__))}/player/game.exe")
        canvas.itemconfigure(MSTxt, text=f"Connecting To: {ip}:{port}")
    else:
        canvas.itemconfigure(MSTxt, text=f"Error: The games files is not in:\n{os.path.realpath(os.path.dirname(__file__))}/player/game.exe")

def ConnPS():
    canvas.itemconfigure(MSTxt, state="normal", text="")
    canvas.itemconfigure(Auto, state="hidden")
    canvas.itemconfigure(Manual, state="hidden")
    res=getServ()
    if res!=False:
            ong=[]
            if res!=False:
                for i in res:
                    ong.append("x")
                    l=(len(ong)*60)-60
                    globals()[f'srv_{i}']=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2)+l, 
                        window=Button(root, 
                            text=f"Address: {i['server_ip']}:{i['server_port']}, Players: {i['servers_players']}", 
                            width=35, 
                            font=("Arial", 20), 
                            bg="#1c1c1c", 
                            height=1, 
                            relief="flat", 
                            borderwidth=0, 
                            fg="#6b6a6a", 
                            activebackground="#3e4552",
                            command=lambda m=dict(i): startGame(m)
                        )
                    )
                    allsrv.append(f'srv_{i}')
            else:
                canvas.itemconfigure(MSTxt, text=f"Error")
    else:
        canvas.itemconfigure(MSTxt, text=f"Error")

def HSPRV():
    canvas.itemconfigure(MSTxt, text=f"the server has been launched but if you don't open\n your ports, you will host on your local network.")
    t0=threading.Thread(target=Server)
    t0.setDaemon(True)
    t0.start()
    t1=threading.Thread(target=Bullet_Server)
    t1.setDaemon(True)
    t1.start()
    
def HSPUB():
    canvas.itemconfigure(MSTxt, text=f"the server has been launched but if you don't open\n your ports, you will host on your local network.")
    t0=threading.Thread(target=Server)
    t0.setDaemon(True)
    t0.start()
    t1=threading.Thread(target=Bullet_Server)
    t1.setDaemon(True)
    t1.start()

def login():
    usr=USRe.get()
    passw=PASSe.get()
    if usr=="Username" or passw=="Password":
        print("nope")
    else:
        print("ok")
        canvas.itemconfigure(USRc, state="hidden")
        canvas.itemconfigure(PASSc, state="hidden")
        canvas.itemconfigure(VldCONN, state="hidden")
        canvas.itemconfigure(But1, state="normal")
        canvas.itemconfigure(But2, state="normal")
        canvas.itemconfigure(But3, state="normal")
        canvas.itemconfigure(Manual, state="normal")
        canvas.itemconfigure(Auto, state="normal")

But1B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1a1d21", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Start Game",
    command=STG
)

But2B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1e2227", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Host Game",
    command=HTG
)

But3B=Button(root, 
    font=("Arial", 20), 
    relief="flat", borderwidth=0, 
    bg="#1e2227", 
    width=round(root.winfo_width()/49), 
    height=1, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white", 
    text="Game Infos",
    command=GI
)

But1=canvas.create_window(
    ((root.winfo_width()*(1/3))-root.winfo_width()/6), 107,
    window=But1B,
    state="normal"
)

But2=canvas.create_window(
    ((root.winfo_width()*(2/3))-root.winfo_width()/6), 107, 
    window=But2B,
    state="normal"
)

But3=canvas.create_window(
    ((root.winfo_width()*(3/3))-root.winfo_width()/6), 107, 
    window=But3B,
    state="normal"
)

Auto=canvas.create_window(root.winfo_width()/2-150, root.winfo_height()/2, 
    window=Button(root, 
        font=("Arial", 20),
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=15, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Publics Servers",
        state="normal",
        command=ConnPS
    )
)

Manual=canvas.create_window(root.winfo_width()/2+150, root.winfo_height()/2, 
    window=Button(root,
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=15, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Manual Servers",
        state="normal",
        command=MS
    )
)

HostPub=canvas.create_window(root.winfo_width()/2-160, root.winfo_height()/2, 
    window=Button(root, 
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=18, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Host Public Game",
        state="normal",
        command=HSPUB
    )
)

HostPrv=canvas.create_window(root.winfo_width()/2+160, root.winfo_height()/2, 
    window=Button(root, 
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=18, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Host Private Game",
        state="normal",
        command=HSPRV
    )
)

Ti=canvas.create_text(root.winfo_width()/2, root.winfo_height()/2, 
    text="PhyGame is a free multiplayer FPS\n(First Person Shooter) game\ndeveloped by 4lxprime", 
    font=("Arial", 25), 
    fill="white",
    state="normal"
)

IPe=Entry(root, 
    text="Server IP", 
    font=("Arial", 20), 
    relief="flat", 
    borderwidth=0, 
    bg="#1e2227", 
    width=20, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white"
)

PORTe=Entry(root, 
    text="Server PORT", 
    font=("Arial", 20), 
    relief="flat", 
    borderwidth=0, 
    bg="#1e2227", 
    width=20, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white"
)

MSTxt=canvas.create_text(root.winfo_width()/2, (root.winfo_height()/2)-70,
    text="", 
    font=("Arial", 20), 
    fill="white",
    state="normal"
)

IPc=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2),
    window=IPe, 
    state="normal"
)

PORTc=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2)+50,
    window=PORTe, 
    state="normal"
)

VldIP=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2)+150, 
    state="normal",
    window=Button(root, 
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=9, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Connect",
        command=ConnMS
    )
)

USRe=Entry(root, 
    text="Username", 
    font=("Arial", 20), 
    relief="flat", 
    borderwidth=0, 
    bg="#1e2227", 
    width=20, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white"
)

PASSe=Entry(root, 
    text="Password", 
    font=("Arial", 20), 
    relief="flat", 
    borderwidth=0, 
    bg="#1e2227", 
    width=20, 
    highlightthickness=1, 
    highlightbackground='black', 
    fg="white"
)

USRc=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2),
    window=USRe, 
    state="normal"
)

PASSc=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2)+50,
    window=PASSe, 
    state="normal"
)

VldCONN=canvas.create_window(root.winfo_width()/2, (root.winfo_height()/2)+150, 
    state="normal",
    window=Button(root, 
        font=("Arial", 20), 
        relief="flat", 
        borderwidth=0, 
        bg="#1e2227", 
        width=9, 
        highlightthickness=1, 
        highlightbackground='black', 
        fg="white", 
        text="Connect",
        command=login
    )
)

canvas.itemconfigure(But1, state="hidden")
canvas.itemconfigure(But2, state="hidden")
canvas.itemconfigure(But3, state="hidden")
canvas.itemconfigure(Manual, state="hidden")
canvas.itemconfigure(Auto, state="hidden")
canvas.itemconfigure(HostPub, state="hidden")
canvas.itemconfigure(HostPrv, state="hidden")
canvas.itemconfigure(Ti, state="hidden")
canvas.itemconfigure(IPc, state="hidden")
canvas.itemconfigure(PORTc, state="hidden")
canvas.itemconfigure(VldIP, state="hidden")
canvas.itemconfigure(USRc, state="normal")
canvas.itemconfigure(PASSc, state="normal")
canvas.itemconfigure(VldCONN, state="normal")

IPe.insert(0, "Server IP")
PORTe.insert(0, "Server PORT")
USRe.insert(0, "Username")
PASSe.insert(0, "Password")


GPage=canvas.create_window(2, 80, anchor="nw", width=root.winfo_width()-5, height=root.winfo_height()-82)

def act():
    while 1:
        root.update()
        canvas.itemconfigure(GPage, width=root.winfo_width()-5, height=root.winfo_height()-122)
        canvas.coords(Auto, root.winfo_width()/2-150, root.winfo_height()/2)
        canvas.coords(Manual, root.winfo_width()/2+150, root.winfo_height()/2)
        canvas.coords(HostPub, root.winfo_width()/2-150, root.winfo_height()/2)
        canvas.coords(HostPrv, root.winfo_width()/2+150, root.winfo_height()/2)
        canvas.coords(cred, root.winfo_width()-60, root.winfo_height()-30)
        canvas.coords(Tt, root.winfo_width()/2, canvas.coords(Tt)[1])
        canvas.coords(But1, (root.winfo_width()*(1/3))-root.winfo_width()/6, canvas.coords(But1)[1])
        canvas.coords(But2, (root.winfo_width()*(2/3))-root.winfo_width()/6, canvas.coords(But2)[1])
        canvas.coords(But3, (root.winfo_width()*(3/3))-root.winfo_width()/6, canvas.coords(But3)[1])
        But1B['width']=round(root.winfo_width()/49)
        But2B['width']=round(root.winfo_width()/49)
        But3B['width']=round(root.winfo_width()/49)
        canvas.coords(Ti, root.winfo_width()/2, root.winfo_height()/2)
        for i in allsrv:
            canvas.coords(globals()[i], root.winfo_width()/2, canvas.coords(globals()[i])[1])
    
t=threading.Thread(target=act)
t.setDaemon(True)
t.start()

canvas.pack(expand=True, fill="both")
root.protocol("WM_DELETE_WINDOW", stop)
root.mainloop()