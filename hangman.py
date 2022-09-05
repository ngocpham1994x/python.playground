import random as rd
from readline import append_history_file
import requests
import string

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

def choose_word():
    response = requests.get(word_site)
    WORDS = response.content.decode('utf-8').splitlines()

    word = rd.choice(WORDS).lower()

    return word


def hangman(word):
    alphabet = list(string.ascii_lowercase)

    for letter in word:
        for char in alphabet:
            if letter == char:
                


def main():

    word = choose_word()
    hangman()

if __name__ == '__main__':
    main()
