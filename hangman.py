from platform import python_branch
import random as rd
import requests
import string

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

def choose_word():
    response = requests.get(word_site)
    WORDS = response.content.decode('utf-8').splitlines()

    word = rd.choice(WORDS).lower()

    return word


def hangman(word, reveal):

    indices = []
    index = 0
    char = ''

    char = input("Does the word have this char?  ")
    while index < len(word):
        index = word.find(char, index)
        if index == -1:
            break
        indices.append(index)
        index = index + 1

    for value in indices:
        print (f"Letter {char} in posotion  {value}")
        reveal[value] = char
    
    return reveal


def main():

    word = choose_word()
    print (f'\nA word was chosen!\n {word}')
    reveal = '_' * len(word)
    for i in range(len(word)):
        reveal = hangman(word, reveal)
        print (reveal)
    
    if '_' in reveal:
        print ('You loose..')
    else:
        print (f"Wow, you guessed the word   '{reveal}'")

if __name__ == '__main__':
    main()




