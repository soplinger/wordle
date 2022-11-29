"""These are custom exceptions use to control the flow of the wordle game on the server"""

class WordleGameTimout(Exception):
    def __init__(self):
        self.msg = "Game did not recieve a response and timed out"

    def __str__(self) -> str:
        return repr(self.msg)

class WordleGameEmptyGuess(Exception):
    def __init__(self):
        self.msg = "Game recieved an empty guess and stopped"

    def __str__(self) -> str:
        return repr(self.msg)