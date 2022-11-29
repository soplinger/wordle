from collections import namedtuple

ServerAddress = namedtuple('server_address', "hostname, port", defaults=["127.0.0.1", 20001])
"""A tuple containing information necessary to create a connection including hostname and port number"""