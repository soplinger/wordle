# server.py created by Sean Oplinger on 10/26/22
# edits and revisions by Sean Oplinger and Benjamin Lloyd
import random
import socket
import threading
from typing import Tuple

from wordle_library import print_err, try_send
from wordle_library.response_strs import AGAIN, BYE, LOSE, PLAYING, STALE, WIN

HOSTNAME = "127.0.0.1"
PORT = 20001
MAX_BUFFER_SIZE = 1024
TIMEOUT_SECS = 10000
MAX_CONNECTIONS = 100

def main():
    try:
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # allows the socket to reuse a previous socket on the same address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOSTNAME, PORT))
    except socket.error as e:
        print_err(f"Error while creating socket: {e}")
        exit(-1)

    print("TCP Server created and listening...")

    server_socket.listen(MAX_CONNECTIONS)

    while (True):
        new_socket, _ = server_socket.accept()
        thread = threading.Thread(target=user_handler, args=[new_socket])
        thread.start()

def user_handler(sender: socket.socket):
    sender.settimeout(TIMEOUT_SECS)

    # Initial connection message and username obtained
    response = sender.recv(MAX_BUFFER_SIZE)
    print(f"Recieved {response}") #debug statement
    responses = response.decode().split()

    username: str = ""
    # Setup identity for client by username, password checking would be cool too :0
    if len(responses) < 2:
        info = sender.getpeername()
        print(f"Client {info} did not send a username generating a random name")
        username = "Guest#" + random.randint(0, 1000000000)
    username = responses[1]

    while True:     # Gameplay loop, player can solve more puzzles
        outcome, num_attempts = start_game(sender, username)

        if outcome == WIN:
            # record data
            pass
        elif outcome == LOSE:
            # record data
            pass
        elif outcome == STALE:
            exit(-1)
    
        try_send(sender, AGAIN)

        response = sender.recv(MAX_BUFFER_SIZE)
        response = response.decode()
        if response == AGAIN:
            continue
        elif response == BYE:
            exit(-1)

def start_game(sender: socket.socket, username: str) -> Tuple[str, int]:
    """ Runs the serverside of the wordle game\n
        Sends the client the word and waits for health checks sent by the client after each guess\n
        The game will end if stale data or no response is given 
        
        Returns:
            `status`, `num_attempts` <- the outcome of the game and how many turns the game lasted
    """
    # Send a word for the client to use in gameplay
    try_send(sender, random.choice(words))

    responses = [PLAYING]

    while True:
        # recieve playing messages as a keep alive 
        try:
            response: bytes = sender.recv(MAX_BUFFER_SIZE)
        except socket.timeout:
            print(f"{username} was inactive for {TIMEOUT_SECS} seconds, ending session")
            return STALE, -1

        responses = response.decode().split()
        if len(responses) < 1:
            print(f"{username} sent an empty response, closing connection")
            return STALE, -1

        print(f"responses[0]={responses[0]}")   # debug statement
        if responses[0] == WIN or responses[0] == LOSE:
            print(f"Client: {username} {responses[0]} and finished in {responses[1]} attempts")
            return responses[0], responses[1]

with open("dict.txt", "r") as file:
    allText = file.read()
    words = list(map(str, allText.split()))

if __name__ == "__main__":
    main()