""" server.py created by Sean Oplinger on 10/26/22
    edits and revisions by Sean Oplinger and Benjamin Lloyd
    
    This file contains the code to run a wordle server compatible with the provided client or
    any client that follows the server protocol.
"""
import random
import socket
import sys
import threading
from typing import Tuple

from wordle_exceptions import WordleGameEmptyGuess, WordleGameTimout
from wordle_library import (AGAIN, BYE, LOSE, PLAYING, WIN, Colors,
                            ServerAddress, log, print_err, recv_full, try_send)

MAX_CONNECTIONS = 100

def main():
    print(Colors.Normal, end="")   # set terminal colors to print in white
    server_addr = parse_cmdline_args()

    try:
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # allows the socket to reuse a previous socket on the same address rather than closing it after usage
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(server_addr)
    except Exception as e:
        print_err(f"Error while creating socket: {e}")
        exit(-1)
    else:
        log(f"TCP server established at {server_addr.hostname} on port {server_addr.port}")

    server_socket.listen(MAX_CONNECTIONS)

    while (True):   # upon a new connection to the socket, start a thread
        new_socket, _ = server_socket.accept()
        thread = threading.Thread(target=user_handler, args=[new_socket])
        thread.start()

def parse_cmdline_args() -> ServerAddress:
    """ Usage: python server.py <port#:optional>"""
    server_addr = ServerAddress()   # a tuple containing info about a server including host and port #
    if len(sys.argv) == 2 and sys.argv[1].isnumeric():
        server_addr = server_addr._replace(port=int(sys.argv[1]))
        print(f"Server configured to port# {server_addr.port}")
    else:
        print(f"No valid port# entered falling back to default: {server_addr.port}")
    return server_addr

def user_handler(sender: socket.socket):
    """ Function that will send and recieve messages with a client connected via the `sender` socket
        This will orchestrate a Wordle game as well as replays and clean up
    """
    # Initial connection message and username obtained
    response = recv_full(sender)
    responses = response.split()

    # Setup identity for client by username
    if len(responses) < 2:
        info = sender.getpeername()
        log(f"Client from {info} did not send a username, closing connection")
        cleanup(sender)

    username = responses[1]
    log(f"Client: {username} has established a connection to server, starting first game")

    while True:     # Gameplay loop, player can solve more puzzles by recieving new words from the server
        try:
            start_game(sender, username)
        except Exception as e:
            print_err(f"Client: {username} finished with error: {e}")
            cleanup(sender)

        try_send(sender, AGAIN)

        response = recv_full(sender)
        if response == AGAIN:
            log(f"Client: {username} has started a new game")
            continue
        elif response == BYE:
            log(f"Client: {username} has ended their playing session")
            cleanup(sender)

def cleanup(socket: socket.socket):
    """ Closes a socket and exits current thread"""
    socket.close()
    exit(0)

def start_game(sender: socket.socket, username: str) -> Tuple[str, int]:
    """ Runs the serverside of the wordle game\n
        Sends the client the word and waits for health checks sent by the client after each guess\n
        The game will end if stale data or no response is given 
        
        Returns:
            `(status, num_attempts)` <- the outcome of the game and how many turns the game lasted

        Errors:
            Will throw errors if gameplay does not proceed as intended `WordleGameTimeout` and `WordleGameEmptyGuess`
    """
    # Send a word for the client to use in gameplay
    try_send(sender, f"{random.choice(words)}%")

    responses = [PLAYING]

    while True:
        # recieve playing messages from user to know they still have a healthy connection 
        try:
            response = recv_full(sender)
        except socket.timeout:
            raise WordleGameTimout

        responses = response.split()
        if len(responses) < 1:
            raise WordleGameEmptyGuess

        if responses[0] == WIN or responses[0] == LOSE:
            color = Colors.Green if responses[0] == WIN else Colors.Red
            log(f"Client: {username} finished with outcome: {color}{responses[0].strip('%')}{Colors.Normal} | # of attempts: {responses[1]}")
            return responses[0], responses[1]
        else:
            log(f"Keep alive recieved from {username}")


with open("dict.txt", "r") as file:
    # will keep the file opened until the program ends
    allText = file.read()
    words = list(map(str, allText.split()))

if __name__ == "__main__":
    main()