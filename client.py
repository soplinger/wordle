""" client.py created by Benjamin Lloyd on 11/3/2022
    revisions made by Benjamin Lloyd and Sean Oplinger

    This file contains the client code of the Wordle application, it can interact with a Wordle server
    provided that it uses the same messaging protocol designed into this application
"""
import random
import socket
import sys

from game import start_game
from wordle_library import (AGAIN, BYE, HELLO, LOSE, WIN, Colors,
                            ServerAddress, print_err, try_send)

MAX_BUFFER_SIZE = 1024

def main():
    print(Colors.Normal, end="")   # set terminal colors to print in white
    server_addr = ServerAddress()   # a tuple containing info about a server including host and port #

    # Argument Parsing VVVVVV
    # User may pass a custom hostname or port and will be set for the server address
    # as well they may add a custom username for easier identification of clients
    name = "Guest#" + str(random.randint(0, 1000000000))
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        print(f"Custom hostname entered: {hostname}")
        server_addr = server_addr._replace(hostname=hostname)

        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                port = int(sys.argv[2])
                print(f"Custom port entered: {port}")
                server_addr = server_addr._replace(port=port)
                if len(sys.argv) > 3:
                    name = sys.argv[2]
            elif sys.argv[2]:
                name = sys.argv[2]

    print(f"Welcome user {name}")
    ready_msg = HELLO + f" {name}"

    try:
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)   # Create a TCP socket
        client_socket.connect(server_addr)
    except socket.error as e:
        print_err(f"Error while creating socket: {e}")
        exit(-1)

    # Send a "hello <name>" to establish a identity on the server 
    try_send(client_socket, ready_msg)

    # get the word and start a game
    response = client_socket.recv(MAX_BUFFER_SIZE)

    while True:
        outcome = start_game(response.decode().lower(), client_socket)
        is_winner = outcome[0]
        outcome_msg = f"{WIN} {outcome[1]}" if is_winner else f"{LOSE} {outcome[1]}"
        try_send(client_socket, outcome_msg)

        response = client_socket.recv(MAX_BUFFER_SIZE)
        choice = input("Would you like to play again? (y/n): ")
        if str.lower(choice) == 'y':
            try_send(client_socket, AGAIN)
            continue
        else:
            try_send(client_socket, BYE)
            break


if __name__ == "__main__":
    main()