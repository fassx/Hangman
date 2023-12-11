import random
import re
import time
from pathlib import Path
from subprocess import call

class HangmanGame:
    HANGMAN_GRAPHICS = [
        """
        ############
        ######_____#
        ######|###|#
        ##########|#
        ##########|#
        ##########|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        ##########|#
        ##########|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        ######|###|#
        ##########|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        #####/|###|#
        ##########|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        #####/|\##|#
        ##########|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        #####/|\##|#
        #####/####|#
        ##########|#
        #####------#
        ############
        """,
        """
        ############
        ######_____#
        ######|###|#
        ######O###|#
        #####/|\##|#
        #####/#\##|#
        ##########|#
        #####------#
        ############
        """
    ]

    def __init__(self, words_file, max_guesses=6):
        self.words_file = Path(words_file)
        self.max_guesses = max_guesses
        self.word = ""
        self.correct = []
        self.wrong = []

    def clear_screen(self):
        call("clear" if Path("/usr/bin/clear").exists() else "cls", shell=True)

    def fetch_hangman_word(self):
        if self.words_file.exists():
            with self.words_file.open() as file:
                words = [line.strip() for line in file]
            if not words:
                raise ValueError("The words file is empty.")
            return random.choice(words)
        else:
            raise FileNotFoundError("The words file does not exist.")

    def get_guess(self):
        while True:
            guess = input("Enter guess: ")
            if re.match(r'^[a-zA-Z]$', guess):
                return guess
            else:
                print("Invalid input! Please enter a single letter.")

    def print_hangman(self, stage):
        try:
            print(self.HANGMAN_GRAPHICS[stage])
        except:
            print("#WORN#: HANGMAN GRAPHICS ERROR")

    def print_word(self):
        for x in self.word:
            if x in self.correct:
                print(x, end="")
            else:
                print("+", end="")
        print("")

    def is_correct(self, guess):
        if guess in self.correct or guess in self.wrong:
            print("You already guessed that letter!")

        elif guess in self.word:
            self.correct.append(guess)
            print("Correct!")
            
        else:
            self.wrong.append(guess)
            print("Wrong!")

    def compare_word(self):
        return set(self.word) == set(self.correct)

    def play(self):
        self.clear_screen()
        self.word = self.fetch_hangman_word()
        self.correct = []
        self.wrong = []
        print("#" * 20)
        print("Welcome to Hangman!")
        print("#" * 20)
        time.sleep(2)

        while len(self.wrong) < self.max_guesses:
            self.clear_screen()
            self.print_hangman(len(self.wrong))
            self.print_word()
            remaining_guesses = self.max_guesses - len(self.wrong)
            print(f"\nYou have {remaining_guesses} guesses remaining.")
            guess = self.get_guess()
            self.is_correct(guess)
            time.sleep(1.5)
            if self.compare_word():
                self.clear_screen()
                print("Congratulations! You won!")
                time.sleep(2)
                self.clear_screen()
                return

        self.clear_screen()
        print("#" * 40)
        print(f"Sorry, you lost! The word was '{self.word}'.")
        print("#" * 40)
        time.sleep(4)
        self.clear_screen()


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir / "words.txt"
    game = HangmanGame(file_path)
    game.play()