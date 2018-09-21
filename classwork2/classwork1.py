import random
import string
def gener_alpha():
    alpha = string.ascii_lowercase
    alpha = list(alpha)
    return alpha  
    
def main():
    alpha = gener_alpha()
    letter = random.choice(alpha)
    print(letter)
    index = ord(letter)
    while True:
        user_g = input("Guess the letter:  ")
        if user_g == letter:
            print("Correct!")
            break
        elif user_g in alpha:
            index_user = ord(user_g)
            if index_user > index:
                print("Correct letter is to the left")
                continue
            else:
                print("Correct letter is to the right")
                continue
        else:
            print("Try again")
            continue
            
    
if __name__ == '__main__':
    main()
