from socket import socket
import time
from wordle_library.colors import Colors

MAX_BUFFER_SIZE = 1024
TIMEOUT_SECS = 10000 

def try_send(sender: socket, msg: str):
    """ Attempts to send a message and will catch exceptions thrown by sendto() 
        if an exception is caught, the thread calling will stop

        Args:
            `sender` : socket that is sending the msg
            `msg` : the message that is being sent in bytes, str must be encoded
    """
    try:
        sender.send(msg.encode(errors='replace'))
    except Exception as e:
        print_err(f"Error while sending: {e}")
        sender.close()
        exit(-1)

def recv_full(reciever: socket) -> str:
    """ Attempts to recieves a message and ensure it is complete and whole
        Checks last byte recieved is a %
        Returns message as a string with % stripped
    """
    reciever.settimeout(TIMEOUT_SECS)
    response = bytearray()
    part = bytearray()
    while True:
        try:
            part = reciever.recv(MAX_BUFFER_SIZE)
        except Exception as e:
            print_err(f"Connection ended during recieving, closing socket")
            reciever.close()
            exit(-1)

        response.extend(part)
        lastbyte = response[len(response) - 1]

        # checks lastbyte is % which is 37 in ascii
        if lastbyte == 37:
            return response.decode(errors='replace').strip('%')


def print_err(msg: str):
    """Prints `msg` in red text to easily distinguish from normal messages"""
    log(f"{Colors.Red}{msg}{Colors.Normal}")

def log(msg: str):
    """Logs a message to console with relavent info such as time sent and color"""
    print(f"{time.asctime()} | {msg}")