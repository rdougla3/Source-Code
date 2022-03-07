import socket
import threading

users = {}
games = {}

class User():
    name = ""
    address = 0
    port = 0

    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port

class Game():
    id = 0
    dealer = ""
    players = {}

class ClientThread(threading.Thread):
    def __init__(self, clientaddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("new connection")

    def run(self):
        while True:
            response = ""
            data = self.csocket.recv(2048)
            msg = data.decode()
            
            command = msg.split(' ')

            if(command[0] == "register"):
                response = execute_register(command)
                print("new request: ", msg)
            elif(command[0] == "query" and command[1] == "players"):
                print("new request: ", msg)
                response = execute_query_players()
            elif(command[0] == "query" and command [1] == "games"):
                print("new request: ", msg)
                response = execute_query_games()            
            elif(command[0] == "de-register"):
                print("new request: ", msg)
                response = execute_deregister(command[1])

            if(response != ""):
                print("responding: ", response)
                self.csocket.send(response.encode('ascii'))                

def execute_register(command):
    name = command[1]
    address = command[2]
    port = command[3]
    new_user = User(command[1], command[2], command[3])

    if(name == "" or address == 0 or port == 0):
        return "REGISTRATION:FAILURE\n"
    for username in users.keys():
        if name == username:
            return "REGISTRATION:FAILURE\n"
    else:
        new_user = User(name, address, port)
        users.update({name: new_user})
        print(users)
        return "REGISTRATION:SUCCESS\n"

def execute_query_players(): 
    output = "PLAYERQUERY " + str(len(users)) + ":"
    for username in users.keys():
        user = users.get(username)
        output += user.name + " " + str(user.address) + " " + user.port + " \n"
    print(output)
    return output

def execute_query_games():
    output = "GAMEQUERY " + str(len(games)) + ":"
    for gamelog in games.keys():
        game = games.get(gamelog)
        output += " " + str(game.id) + " "
        #add each player to the output message, starting with the dealer (#1)
        for player in game.players:
            output += " " + player.name + ","
    return output

def execute_deregister(username):
    for game in games:
        for player in game.players:
            if(username == player.name):
                return "REGISTRATION:FAILURE\n"    
    users.pop(username)
    return "REGISTRATION:SUCCESS"

def Main():
    port = 18000
    host = '127.0.0.1'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))

    while True:
        server.listen(1)
        clientsocket, clientaddress = server.accept()
        newthread = ClientThread(clientaddress, clientsocket)
        newthread.start()

if __name__ == '__main__':
    Main()