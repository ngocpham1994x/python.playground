import tkinter as tk
import random as rd

# user guesses the number generated by computer
def guess_me():
    print("Provide a range so that the program can choose a number for you")
    from_num = int(input("from: "))
    to_num = int(input("to: "))

    num = rd.randint(from_num, to_num)
    print("Number for guessing is generated! Now please guess.")

    # do-while emulate:
    while True:
        user_guess = int(input(f"Guess the number between {from_num} and {to_num}: "))

        if user_guess < num:
            print('This is too low. Guess again.')
        elif user_guess > num:
            print('This is too high. Guess again.')
        else:
            print('Congrats!!!! You got it!')
            break

# computer guesses the number generated by user
def let_me_guess():
    print("Provide a high bound so the program knows where to start off with.")
    low_bound = 1
    high_bound = int(input("high bound: "))

    while True:
        if low_bound != high_bound:
            computer_guess = rd.randint(low_bound, high_bound)
        else:
            computer_guess = low_bound

        answer = input(f'{computer_guess} is too low, or too high, or it is the correct number you are thinking of?').lower()
        if answer in ['l', 'low']:
            low_bound = computer_guess
        elif answer in ['h', 'high']:
            high_bound = computer_guess
        else:
            print('Congrats!!!! Computer, you got it!')
            break

def main():

    guess_me()
    print('====================================')
    let_me_guess()

if __name__ == '__main__':
    main()
