# server.py created by Sean Oplinger on 10/26/22
import socket
import random

with open("dict.txt", "r") as file:
    allText = file.read()
    words = list(map(str, allText.split()))

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

print("UDP Server Listening")

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    bytesToSend = str.encode(random.choice(words))

    UDPServerSocket.sendto(bytesToSend, address)
