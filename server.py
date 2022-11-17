# server.py created by Sean Oplinger on 10/26/22
import socket
import random
import sys
import json


def userHandler(newSocket, address):

    receivedData = newSocket.recv(1024)
    print(f"recieved {receivedData}")

    bytesToSend = str.encode(random.choice(words))
    newSocket.send(bytesToSend)

    receivedData = newSocket.recv(1024)
    responses = receivedData.decode().split()

    print(responses)

    match responses[0]:
        case 'WIN':
            print(f"client correct took {responses[1]} attempts")
        case 'LOSE':
            print(f"client lost took {responses[1]} attempts")

    newSocket.close()


with open("dict.txt", "r") as file:
    allText = file.read()
    words = list(map(str, allText.split()))

localIP = "156.12.184.62"
localPort = 20001
bufferSize = 1024

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

TCPServerSocket.bind((localIP, localPort))

print("TCP Server Listening")

TCPServerSocket.listen(10)

while (True):

    newSocket, address = TCPServerSocket.accept()
    userHandler(newSocket, address)
