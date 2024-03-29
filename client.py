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
                            ServerAddress, print_err, try_send, recv_full)

MAX_BUFFER_SIZE = 1024

def main():
    print(Colors.Normal, end="")   # set terminal colors to print in white
    server_addr, name = parse_cmdline_args()
    print(f"Welcome {name}")

    try:
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)   # Create a TCP socket
        client_socket.connect(server_addr)
    except socket.error as e:
        print_err(f"Error while creating socket: {e}")
        exit(-1)

    ready_msg = HELLO + f" {name}%"
    try_send(client_socket, ready_msg)

    while True:
        # get the word from the server
        word_response = recv_full(client_socket)
        run_wordle(client_socket, word_response.lower())

        # recieves a message asking to play again to ensure
        recv_full(client_socket)
        choice = input("Would you like to play again? (y/n): ")
        if str.lower(choice) == 'y':
            try_send(client_socket, AGAIN)
            continue
        else:
            try_send(client_socket, BYE)
            break

def run_wordle(client_socket: socket.socket, word: str):
    """Starts a game of wordle and prints the color coded outcome of the game"""
    is_winner, num_attempts = start_game(word, client_socket)
    outcome_msg = f"{WIN} {num_attempts}%" if is_winner else f"{LOSE} {num_attempts}%"
    try_send(client_socket, outcome_msg)

def parse_cmdline_args() -> tuple():
    """ Usage: python client.py <hostname:optional> <port#:optional> <username:optional>"""
    server_addr = ServerAddress()   # a tuple containing info about a server including host and port
    name = "Guest#" + str(random.randint(0, 1000000000))

    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        print(f"Custom hostname entered: {hostname}")
        server_addr = server_addr._replace(hostname=hostname)

    if len(sys.argv) > 2 and sys.argv[2].isnumeric():
        port = int(sys.argv[2])
        print(f"Custom port entered: {port}")
        server_addr = server_addr._replace(port=port)

    if len(sys.argv) > 3:
        # removes spaces to keep names a single word
        name = sys.argv[3].replace(' ', '')

    return server_addr, name


if __name__ == "__main__":
    main()