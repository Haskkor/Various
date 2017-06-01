from enum import Enum

class State(Enum):

    INCORRECT = 0
    ALREADY_WRONG = 1
    CORRECT = 2
    ALREADY_GUESSED = 3

class Hangman:

    def __init__(self, word_to_guess, lives):
        self.word_to_guess = word_to_guess
        self.lives = lives
        self.wrong_letters = []
        self.current_word = "_" * len(word_to_guess)

    def play(self, letter):
        if letter.lower() in self.word_to_guess.lower():
            if letter.lower() not in self.current_word.lower():
                self.current_word = self.print_dashed(letter)
                return State.CORRECT
            else:
                return State.ALREADY_GUESSED
        else:
            if letter.lower() not in self.wrong_letters:
                self.wrong_letters.append(letter.lower())
                self.lives -= 1
                return State.INCORRECT
            else:
                return State.ALREADY_WRONG

    def win(self):
        return "_" not in self.current_word

    def loose(self):
        return self.lives <= 0

    # Print the dashed word
    def print_dashed(self, guessed_letter):
        working_word = ""
        for i, letter in enumerate(self.word_to_guess):
            if self.current_word[i] == "_":
                if letter.lower() == guessed_letter.lower():
                    working_word += letter
                else:
                    working_word += "_"
            else:
                working_word += self.current_word[i]
        return working_word

    # Print all the wrong letters
    def print_wrong_letters(self):
        to_print = ""
        for letter in self.wrong_letters:
            to_print += letter
            to_print += " "
        return to_print

def console_work():
    hangman = Hangman("Powershop", 5)
    while not hangman.win() and not hangman.loose():
        print(hangman.current_word)
        letter = input("Enter a letter : ")
        state = hangman.play(letter)
        if state == State.CORRECT:
            print("Ok.")
        elif state == State.ALREADY_GUESSED:
            print("Already guessed.")
        elif state == State.INCORRECT:
            print("Wrong.")
            print(hangman.print_wrong_letters())
        elif state == State.ALREADY_WRONG:
            print("Still wrong.")
            print(hangman.print_wrong_letters())
    if hangman.win():
        print("You win")
    else:
        print("You loose")

console_work()