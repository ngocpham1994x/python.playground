import random as rd
import requests
import string


word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

def choose_word():
    response = requests.get(word_site)
    WORDS = response.content.decode('utf-8').splitlines()

    word = rd.choice(WORDS).lower()
    while '-' in word or ' ' in word:
        word = rd.choice(WORDS).lower()

    return word


def hangman(word, reveal):

    alphabet = set(string.ascii_lowercase())
    guessed_char = set()
    indices = []
    index = 0
    char = ''

    char = input("Does the word have this char?  ")
 
    if len(char) > 1 or len(char) == 0:
        print ("Incorrect input: char is too long or no input.")

    else:
        while index < len(word):
            index = word.find(char, index)
            if index == -1:
                break
            guessed_char.add(char)
            indices.append(index)
            index = index + 1

        for value in indices:
            print (f"Letter {char} in posotion  {value}")
            reveal = reveal[:value] + char + reveal[value+1 : ]

    return reveal


def main():

    word = choose_word()
    print (f'\nA word was chosen!\n {word}')
    reveal = '_' * len(word)

    for i in range(len(word)):
        reveal = hangman(word, reveal)
        # print (reveal)

        if '_' in reveal:
            print (f'You have {len(word)-i-1} times to guess.')
        else:
            print (f"Wow, you guessed the word   '{reveal}'")
            break

    print ("Game's done!")


if __name__ == '__main__':
    main()




