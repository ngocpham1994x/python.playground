import random as rd
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
    reveal = '_' * len(word)

    for i in range(len(word)):
        char = input("Does the word have this char?  ")
        if char in word:
            reveal[]
    print (reveal)

    # for i, letter in enumerate(word):
    #     for char in alphabet:
    #         if letter == char:
    #             reveal[i] = letter
    #         else 


def main():

    word = choose_word()
    hangman(word)

if __name__ == '__main__':
    main()
