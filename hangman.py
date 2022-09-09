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


def hangman(char, word, reveal):
    alphabet = set(string.ascii_lowercase)
    indices = []
    index = 0

    if char not in alphabet:
        print ("===UH OH! INCORRECT INPUT..!===")

    else:
        while index < len(word):
            index = word.find(char, index)
            if index == -1:
                break
            indices.append(index)
            index = index + 1

        for value in indices:
            print (f"Letter {char} in posotion  {value}")
            reveal = reveal[:value] + char + reveal[value+1 : ]

    return reveal


def main():

    guessed_char = set()

    # pick a word
    word = choose_word()
    print (f'\nA word was chosen!')
    # print (word)
    reveal = '_' * len(word)
    print (reveal)

    lives = len(word) + 3

    # start playing
    for i in range(lives) :
        # initial info
        if '_' in reveal:
            print (f'You have {lives - i} times left to guess.')
        else:
            print (f"Wow, you guessed the word   '{reveal}'")
            break

        # pick a char
        print (f"\nGuessed list: {guessed_char}")
        char = input("Does the word have this char?  ")

        # check if the char has been guessed, if yes -> hangman()
        if char not in guessed_char:
            reveal = hangman(char, word, reveal)
            guessed_char.add(char)

        # if no -> loose a live

        print (reveal)


    # final check
    if '_' in reveal:
        print ("You lost...!")
        print (f"The word is   '{word}'")
    else:
        print ("You won! Yayy")


if __name__ == '__main__':
    main()




