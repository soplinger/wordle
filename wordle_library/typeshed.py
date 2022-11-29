from collections import namedtuple

ServerAddress = namedtuple('server_address', "hostname, port", defaults=["127.0.0.1", 20001])
"""Contains a tuple of information necessary to connect to a server including hostname and port number"""