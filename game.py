""" Wordle game 
    Starts with the function start_game
    The same function will return the outcome of the game
"""
from enum import Enum
from socket import socket
from wordle_library import Colors
from typing import Tuple

MAX_ATTEMPTS = 5

def start_game(word: str, socket: socket) -> Tuple[bool, int]:
    """ Start the game of wordle and commence gameplay
        word <- the word trying to be guessed by the user
        Returns True if the player wins the game, False if the player exceeds max attempts
    """
    print("======Game Start======")

    prev_guesses = []
    is_winner = False
    num_attempts = 0 

    while num_attempts < MAX_ATTEMPTS:
        if prev_guesses:
            for g in prev_guesses:
                print(g.output())

        guess = input("> ")
        if len(guess) != 5:
            print("Guess must be 5 characters")
            continue
        if not guess.isalpha():
            print("Guess must only contain letters")
            continue
        num_attempts += 1

        guess = W_Guess(guess)  # convert guess into wordle guess with the result encapsulated
        is_winner = guess.check(word)
        if is_winner:
            print(guess.output())
            print(f"You got the word in {num_attempts} attempt")
            print("======Game Finish======")
            return True, num_attempts

        prev_guesses.append(guess)
        socket.try_send()


    # All attempts used up, you lose
    print(f"Darn you couldn't guess {word}")
    print("======Game Finish======")
    return False, 5

class W_GuessType(Enum):
    CorrectPosCorrectLetter = 1
    WrongPosCorrectLetter = 2
    WrongPosWrongLetter = 3


class W_Guess:
    def __init__(self, word: str):
        self.word = word    # word being guessed
        # parallel array to word showing which letter matches
        self.result = [W_GuessType.WrongPosWrongLetter for _ in range(5)] 

    def check(self, correct_word: str) -> bool:
        "Returns True if word matches exactly, otherwise false and updates result with status of guess"
        exact_match = True
        for idx, (guess_letter, correct_letter) in enumerate(zip(self.word, correct_word)):
            if guess_letter == correct_letter:
                self.result[idx] = W_GuessType.CorrectPosCorrectLetter
            elif guess_letter in correct_word:
                exact_match = False
                self.result[idx] = W_GuessType.WrongPosCorrectLetter
            else:
                exact_match = False
                self.result[idx] = W_GuessType.WrongPosWrongLetter

        return exact_match 
    
    def output(self) -> str:
        """Returns a colored string of the guess based on the result of the word"""
        output = ""
        for idx, letter in enumerate(self.word):
            if self.result[idx] == W_GuessType.CorrectPosCorrectLetter:
                color = Colors.Green
            elif self.result[idx] == W_GuessType.WrongPosCorrectLetter:
                color = Colors.Yellow
            else:
                color = Colors.Red
            output += f"{color}{letter}"
        output += Colors.Normal   # reset terminal to display white text
        return output
