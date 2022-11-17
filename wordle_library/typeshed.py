from collections import namedtuple

ServerAddress = namedtuple('server_address', "hostname, port", defaults=["127.0.0.1", 20001])