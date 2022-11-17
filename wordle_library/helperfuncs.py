from socket import socket
import time
from wordle_library.colors import Colors
from wordle_library.typeshed import ServerAddress

def try_send(sender: socket, msg: str, debug: bool = False):
    """ Attempts to send a message and will catch exceptions thrown by sendto() 
        if an exception is caught, the thread calling will stop

        Args:
            `sender` : socket that is sending the msg
            `msg` : the message that is being sent in bytes, str must be encoded
    """
    try:
        if debug:
            log(f"Sending msg: {msg}")
        
        bytes_sent = sender.send(msg.encode(errors='replace'))
        
        if debug:
            info = sender.getpeername()
            log(f"Bytes sent: {bytes_sent}/{len(msg)} to location: {info}")
    except Exception as e:
        print_err(f"Error while sending: {e}")
        sender.close()
        exit(-1)

def print_err(msg: str):
    """Prints `msg` in red text to easily distinguish from normal messages"""
    log(f"{Colors.Red}{msg}{Colors.Normal}")

def log(msg: str):
    """Logs a message to console with some extra information"""
    print(f"{time.asctime()} | {msg}")