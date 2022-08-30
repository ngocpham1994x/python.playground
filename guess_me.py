import random as rd

def guess_me(from_num, to_num):
    number = rd.randint(from_num, to_num)
    print("Number for guessing is generated! Now please guess.")

    print(f"Guess the number between {from_num} and {to_num}")

    


def main():
    print("Provide a range so that the program can choose a number for you")
    from_num = int(input("from: "))
    to_num = int(input("to: "))

    guess_me(from_num, to_num)



if __name__ == '__main__':
    main()
