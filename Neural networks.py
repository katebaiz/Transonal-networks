from random import random, randint

class transone:
    def __init__(self, s):
        self.dens = 0
        self.axon = 0
        self.sodium = 1
        self.count = [0 for _ in range(mem)]
        self.t = 0
        self.s = s
        self.act = 0
    def clear(self):
        self.dens = 0
    def choice(self):
        self.t = min(mem, self.t+1)
        self.act = self.act - 1
        for i in range(mem-1):
            self.count[i] = self.count[i+1]
        if (self.dens > 0.2*self.s*(sum(self.count)/self.t) and self.sodium) or self.act < -0.5*mem:
            self.count[mem - 1] = 1
            self.sodium = 0
            self.axon = 1
            self.act = mem
        else:
            self.count[mem-1] = 0
            self.sodium = 1
            self.axon = 0
    def recv(self, signal):
        self.dens += signal
    def set(self, signal):
        self.axon = signal

class synapse:
    def __init__(self, presyn, postsyn):
        self.postsyn = postsyn
        self.presyn = presyn
        self.weight = random()*(randint(0,1)*2-1)
        self.b1 = 0
        self.b2 = 0
        self.act = 0
    def send(self):
        if self.b1: self.postsyn.recv(self.weight)
    def resolve_1(self):
        self.b1 = self.presyn.axon
        self.act = self.presyn.act
        if self.act < -0.5*mem+1: self.weight = min(1, self.weight + 0.1*random())
    def resolve_2(self):
        self.b2 = self.postsyn.axon
    def change(self):
        if self.b1 and self.b2:
            self.weight = min(1, self.weight+0.05)
        elif self.b1 and not self.b2:
            self.weight = max(-1, self.weight-0.05)
    def signal(self, signal):
        if signal and self.act > 0: self.weight = max(-1, min(1, self.weight*1.12))
        if (not signal) and self.act > 0: self.weight = max(-1, min(1, self.weight*0.95))

n = int(input())
perc = float(input())
mem = int(input())
transones = [transone(n*perc) for _ in range(n)]
synapses = []
for i in transones:
    i.set(randint(0,1))
    for j in range(int(n*perc)):
        while True:
            b = randint(0, n-1)
            if transones[b] != i:
                synapses.append(synapse(i, transones[b]))
                break
while True:
    a = input().upper()
    if a == "DOPAMINE":
        for i in synapses:
            i.signal(1)
        continue
    elif a == "PAIN":
        for i in synapses:
            i.signal(0)
        continue
    for i in range(len(a)):
        sym = bin(ord(a[i]))
        sym = sym[2:len(sym)]
        q = 0
        w = len(sym)
        for j in range(w):
            transones[j].set(int(sym[j]))
        for j in range(n):
            for t in transones:
                t.clear()
            for s in synapses:
                s.resolve_1()
                s.send()
            for t in transones:
                t.choice()
            for s in synapses:
                s.resolve_2()
                s.change()
            char = ""
            for j in transones:
                char += str(j.axon)
            print(char)
            if input() == "STOP": break
