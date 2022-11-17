

class AccountModel:
    # for now username is the id, in the future this may change when passwords are added
    username: str   # Unique username that correlates to one user
    solves: int # Solved the word before running out of attempts
    plays: int  # Amount of games started and finished
    guesses_made: int   # Amout of guesses cumulatively used in games
    # losses = plays - solves
    # win rate = solves / plays