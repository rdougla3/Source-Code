import socket

host = '127.0.0.1'
port = 18000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

while True:
    msg = input('Input a message for the server\n')
    command = msg.split(' ')
    client.sendall(msg.encode('ascii'))
    response = client.recv(1024).decode()
    header,body = response.split(":")
    request = header.split(" ")[0]

    if(request == "REGISTRATION"):
        print(body) 
    elif(request == "PLAYERQUERY"):
        playercount = header.split(" ")[1]
        output = "Current Players: " + playercount + "\n"
        if int(playercount) > 0:
            for line in body.split("\n"):
                if(line != ""):
                    print(line)
                    output += "Username: " + line.split(" ")[0] + "\tAdrress: " + line.split(" ")[1] + "\tPort: " + line.split(" ")[2] + "\n"
        print(output)
    elif(request == "GAMEQUERY"):
        gamecount = header.split(" ")[1]
        output = "Current Games: " + gamecount + "\n"
        if int(gamecount) > 0:
            for line in body.split("\n"):
                if(line != ""):
                    gameid = line.split(" ")[0]
                    players = line.split(" ")[1]
                    dealer = players[0]
                output += "Game id: " + gameid + "Dealer: " + dealer + "Players: " + players + "\n"
                "Dealer: " + line.split(" ")[1]
        print(output)
