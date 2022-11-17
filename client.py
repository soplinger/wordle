import socket
import sys 
from wordle_library import try_send, print_err, ServerAddress 
from game import start_game

MAX_BUFFER_SIZE = 1024

def main():
    server_addr = ServerAddress()
    # User may pass a custom hostname or port and will be set for the server address
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        print(f"Custom Hostname: {hostname}")
        server_addr = server_addr._replace(hostname=hostname)

        if len(sys.argv) > 2:
            port = sys.argv[2]
            print(f"Custom port entered: {port}")
            server_addr = server_addr._replace(port=port)


    ready_msg = "Hello Sean"
    ready_bytes_msg = str.encode(ready_msg)

    # Create a UDP socket
    try:
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        client_socket.connect(server_addr)
    except socket.error as e:
        print_err(f"Error while creating socket: {e}")
        exit(-1)

    # Send a "hello" to establish a connection with the client, client also is binded to server_addr
    try_send(client_socket, ready_bytes_msg)

    response, _ = client_socket.recvfrom(MAX_BUFFER_SIZE)
    msg = f"Message from Server {response}"
    print(msg)  # print out solution

    outcome = start_game(response.decode(), client_socket)

if __name__ == "__main__":
    main()