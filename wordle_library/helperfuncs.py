from socket import socket
from wordle_library.colors import Colors
from wordle_library.typeshed import ServerAddress

def try_send(sender: socket, msg: bytes, debug: bool = False):
    """ Attempts to send a message and will catch exceptions thrown by sendto() before exiting

        Args:
            `sender` : socket that is sending the msg
            `msg` : the message that is being sent in bytes, str must be encoded
    """
    try:
        print(f"Sending msg: {msg}")
        bytes_sent = sender.send(msg)
        info = sender.getpeername()
        print(f"Bytes sent: {bytes_sent}/{len(msg)} to location: {info}")
    except socket.gaierror as e:    #TODO change error message or delete
        print_err(f"Error: {e}")
        exit(-1)
    except socket.error as e:
        print_err(f"Error: {e}")
        exit(-1)

def print_err(msg: str):
    """Prints `msg` in red text to easily distinguish from normal messages"""
    print(f"{Colors.Red}{msg}{Colors.Normal}")