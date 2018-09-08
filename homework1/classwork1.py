import random
import string
def gener_random_letter():
    alpha = string.ascii_lowercase
    alpha = list(alpha)
    letter = random.choice(alpha)
    return letter  

"""def get_word_hint(d):
    
    return word, hint"""
    
def main():
    let = gener_random_letter()
    print(let)
    while True:
        user_g = input("Guess the letter:  ")
        if user_g == let:
            print("Correct!")
            break
        else:
            print("Try again")
            continue
            
    
if __name__ == '__main__':
    main()
