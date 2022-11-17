import random
import socket
import sys 
from wordle_library import try_send, print_err, ServerAddress, Colors, HELLO, WIN, LOSE
from game import start_game
from wordle_library.response_strs import AGAIN, BYE

MAX_BUFFER_SIZE = 1024

def main():
    print(Colors.Normal)
    server_addr = ServerAddress()
    # Argument Parsing VVVVVV
    # User may pass a custom hostname or port and will be set for the server address
    # as well they may add a custom username for hiscore tracking
    name = "Guest#" + str(random.randint(0, 1000000000))
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        print(f"Custom Hostname: {hostname}")
        server_addr = server_addr._replace(hostname=hostname)

        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                port = sys.argv[2]
                print(f"Custom port entered: {port}")
                server_addr = server_addr._replace(port=port)
                if len(sys.argv) > 3:
                    name = sys.argv[2]
                    print(f"Welcome user {name}")
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

    # Send a "hello name" to establish a identity on the server 
    try_send(client_socket, ready_msg)

    # get the word and start a game
    response = client_socket.recv(MAX_BUFFER_SIZE)
    # msg = f"Message from Server {response}"
    # print(msg)  # print out solution
    while True:
        outcome = start_game(response.decode(), client_socket)
        outcome_msg = f"{WIN} {outcome[1]}" if outcome[0] else f"{LOSE} {outcome[1]}"
        try_send(client_socket, outcome_msg)

        response = client_socket.recv(MAX_BUFFER_SIZE)
        choice = input("Would you like to play again? (y/n): ")
        if str.lower(choice) == 'y':
            try_send(client_socket, AGAIN)
            continue
        else:
            try_send(client_socket, BYE)
            exit(0)



if __name__ == "__main__":
    main()