from subprocess import *
from random import randint

n = 300
web = Popen(["python", "Neural networks.py"],
            stdin = PIPE,
            stdout = PIPE,
            text = True)
tr = int(input("Number of transones: "))
web.stdin.write(str(tr)+"\n")
web.stdin.flush()
web.stdin.write(input("% of transones connected to one: ")+"\n")
web.stdin.flush()
web.stdin.write(input("Memory length: ")+"\n")
web.stdin.flush()
limit = float(input(f"% of last {n} rounds to be correct: "))
perc = [0 for i in range(n)]
t = 0
sym = ["$\n", "€\n"]
while True:
    t = min(t+1, n)
    ran = randint(0,1)
    web.stdin.write(sym[ran])
    web.stdin.flush()
    for i in range(n-1):
        perc[i] = perc[i+1]
    right = False
    for i in range(tr):
        a = web.stdout.readline()
        if "01111\n" == a[(len(a)-6):len(a)] and not ran:
            web.stdin.write("STOP\n")
            web.stdin.flush()
            right = True
            break
        elif "11110\n" == a[(len(a)-6):len(a)] and ran:
            web.stdin.write("STOP\n")
            web.stdin.flush()
            right = True
            break
        else:
            web.stdin.write("\n")
            web.stdin.flush()
    print(i)
    if right:
        web.stdin.write("DOPAMINE\n")
        perc[n-1] = 1
    else:
        web.stdin.write("PAIN\n")
        perc[n-1] = 0
    web.stdin.flush()
    print(sym[ran][0],"|",a)
    print(sum(perc)/t,"\n")
    if sum(perc)/t > limit and t == n:
        break
input()

