def pars(text):
    data = []
    lines = text.splitlines()
    lines.pop(0)
    for line in lines:
        l = line.strip().split(',')
        l[0] = int(l[0])
        l[1] = float(l[1])
        data.append(l)
    return data

def occupation_distribution(data):
    jobs = []
    occup = {}
    for el in data:
        jobs.append(el[2])
    freq = {}
    for job in jobs:
       if job in occup:    
           occup[job] += 1
       else:  
           occup[job] = 1
    return occup
    
def main():
    text = """Subject,Height,Occupation
1,74.37000326528938,Psychologist
2,67.49686206937491,Psychologist
3,74.92356434760966,Psychologist
4,64.62372198999978,Psychologist
5,67.76787900026083,Linguist
6,61.50397707923559,Psychologist
7,62.73680961908566,Psychologist
8,68.60803984763902,Linguist
9,70.16090500135535,Psychologist
10,76.81144438287173,Linguist"""
    data = pars(text)
    for d in data:
        print(d)
    print(occupation_distribution(data))
if __name__ == '__main__':
    main()
