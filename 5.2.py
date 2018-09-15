import random
def main():
    pattern = "{}{}{}"
    nouns = ['masha','we','glasha', 'homework','gas','sun','bunny','pencil']
    verbs = ['gets','put','present','buys']
    num = random.randint(1, 10)
    sentence = "{} {} {}."
    while num != 0:
        subject = random.choice(nouns).title()
        object1 = random.choice(nouns)
        verb = random.choice(verbs)
        sent = sentence.format(subject,verb,object1)
        print(sent)
        num = num - 1
            
    
if __name__ == '__main__':
    main()
