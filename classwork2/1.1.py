import random
import string
def mean(vals):
        summ = 0
        for v in vals:
            summ +=vals
            count += 1
        if count != 0:
            m = summ/count
            return m
        else:
            return "Not defined"  
    
def main():
    vals = []
    user_inp = 9
    while user_inp != ' ':
        user_inp = input("Enter value")
        vals.append(user_inp)
    print(mean(vals))
            
    
if __name__ == '__main__':
    main()
