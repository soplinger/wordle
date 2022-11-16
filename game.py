""" Wordle game based on the popular game, Wordle
    Starts with the function start_game
    The same function will return the outcome of the game
"""
from enum import Enum

MAX_ATTEMPTS = 5

def start_game(word: str) -> bool:
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
        if not guess.isalpha:
            print("Guess must only contain letters")
            continue

        guess = W_Guess(guess)  # convert guess into wordle guess with the result encapsulated
        is_winner = guess.check(word)
        prev_guesses.append(guess)
        if is_winner:
            print(f"You got the word in {num_attempts}")
            print("======Game Finish======")
            return True

    # All attempts used up, you lose
    print(f"Darn you couldn't guess {word}")
    print("======Game Finish======")
    return False

class W_GuessType(Enum):
    CorrectPosCorrectLetter = 1
    WrongPosCorrectLetter = 2
    WrongPosWrongLetter = 3


class W_Guess:
    def __init__(self, word: str):
        self.word = word    # word being guessed
        self.result = [W_GuessType.WrongPosWrongLetter for _ in range(5)] # parallel array to word showing which letter matches

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
        # for result in enumerate(self.result): # debug for printing status
        #     print(f"{result[0]}:{result[1]}")
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

class Colors:
    Green = "\033[92m"  # correct pos correct letter
    Yellow = "\033[33m" # wrong pos correct letter
    Red = "\033[31m"    # wrong pos wrong letter
    Normal = "\033[0m"  # the usual color(white) for the terminal

if __name__ == "__main__":
    start_game("quinn")