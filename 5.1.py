    
def main():
    pattern = "{}{}"
    consonants = ['p','t','k']
    vowels = ['a','o']
    for c in consonants:
        for v in vowels:
            print(pattern.format(c,v))
            
    
if __name__ == '__main__':
    main()
