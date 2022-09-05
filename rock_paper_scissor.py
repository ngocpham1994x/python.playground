import random as rd


def rps():
    user = input("What you choice? 'rock', 'paper', 'scissor'?  ")
    computer = rd.choice(['rock', 'paper', 'scissor'])

    print (f"Computer choice is:  {computer}")

    if user == computer:
        print ("It's a tie.")
    elif (user == 'rock' and computer == 'scisssor') or \
        (user == 'paper' and computer == 'rock') or \
        (user == 'scissor' and computer == 'paper'):
        print ("Yayy, User wins !")
    else:
        print ("Computer wins")

def main():

    rps()

if __name__ == '__main__':
    main()
