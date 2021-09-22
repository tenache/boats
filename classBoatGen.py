# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:22:48 2021

@author: Usuario
"""
import numpy as np
import random as rd
from classBoat import boat
import operator as op
from classSpot import spot



class boatGen:
    def __init__(self,maxSpeed=7,domFacts=2,boatSize=9,demeSize=20,demes=1):
        self.demes = demes
        self.demeSize = demeSize
        self.numBoats = demeSize * self.demes
        self.maxSpeed = maxSpeed
        self.domFacts = domFacts
        self.boatSize = boatSize
        self.allDemes = []
        self.allBoats = [] # a list of all the class instances of boats generating ghere
        self.allGenRowers = {} #This variable gives us a summary of all rowers and their numbers
        self.cofactors = np.empty((self.boatSize,self.boatSize),dtype=np.ndarray)
        for i in range(self.boatSize):#i represents the position on the boat (the locus)
            self.allGenRowers[i] = {}#First we generate the empty dictionaries for all possibilities
            for j in range(self.maxSpeed + 1):#j is the allele, the name of the genes. In this case is also speed. 
                self.allGenRowers[i][j] = [0]
        for i in range(self.boatSize):
            for j in range (self.boatSize):
                self.cofactors[i,j]=np.random.normal(0,self.maxSpeed,(self.maxSpeed +1,self.maxSpeed+1))
        for i in range(self.numBoats):#here we generate the boats
            rowBoat = boat(self.cofactors,maxSpeed,domFacts,boatSize)
            self.allBoats.append(rowBoat)
        place = 0
        for i in range(self.demes):
            self.allDemes.append(self.allBoats[place:place + self.demeSize])
            place += self.demeSize
        self.allBoats.sort(key=op.attrgetter('boatSpeed'))#returns boats ordered from slowest to fastest
        self.calculateRowers()
        self.calculateFitness()

    def calculateRowers(self):
        self.allGenRowers = {} #This variable gives us a summary of all rowers and their numbers
        for i in range(self.boatSize):#i represents the position on the boat (the locus)
            self.allGenRowers[i] = {}#First we generate the empty dictionaries for all possibilities
            for j in range(self.maxSpeed + 1):#j is the allele, the name of the genes. In this case is also speed. 
                self.allGenRowers[i][j] = [0]
        for ind in self.allBoats:#for each boat in the generation...
            for locus in ind.spotS:#for each rower in said boat...
                allele0 = locus.rower0.rowerSpeed
                allele1 = locus.rower1.rowerSpeed
                #print('locus position is ' + str(locus.position))
                #print('allele is ' + str(allele0))
                self.allGenRowers[locus.position][allele0][0] += 1#add rowers in boat to the allgenRowers summary
                self.allGenRowers[locus.position][allele1][0] += 1#remember there are two rowers per "spot" or position in the boat
    def select(self):#selects the best half of boats
        self.allBoats.sort(key=op.attrgetter('boatSpeed'))
        midWay = int(self.numBoats/2)
        del self.allBoats[0:midWay]
        midSpeed = self.allBoats[0].boatSpeed
        for i,deme in enumerate(self.allDemes):
            j = 0
            demeLen = len(deme)
            for z in range(demeLen):
                if deme[j].boatSpeed < midSpeed:
                    del self.allDemes[i][j]
                else:
                    j += 1
        self.calculateRowers()
        self.numBoats = len(self.allBoats)
        self.calculateFitness()
    def migrate(self):
        for i,deme in enumerate(self.allDemes):
            randDeme = rd.randint(0,self.demes -1)
            try:
                randBoat = rd.randint(0,len(deme) - 1)
            except ValueError:
                print('no Boats in this deme, error')
            try:
                self.allDemes[randDeme].append(deme.pop(randBoat))
                if len(deme) == 0:
                    del self.allDemes[i]
                    print(f'deme number {i} has gone extinct')
            except IndexError:
                print(f'randBoat is {randBoat},deme length is {len(deme)}')
    def mate(self):
        bachellors = self.allDemes.copy()
        for deme in self.allDemes:
            rd.shuffle(deme)#take away if we want panmixis
        marriedBoats = []
        for d,deme in enumerate(bachellors):
            marriedBoats.append([])
            while len(deme) > 1:
                # try:
                husband = deme.pop(rd.randint(0,len(deme) -1))
                wife = deme.pop(rd.randint(0,len(deme)- 1))
                marriedBoats[d].append([husband,wife])
        self.allDemes = []#Don't want to get stuck with an odd number of boats, so if there's a single bachellor without a mate, it's gone
        for d,deme in enumerate(marriedBoats):
            self.allDemes.append([])
            #print(f'length of deme is{len(deme)} ')
            for c,pair in enumerate(deme):
                #print('Am I getting into this loop?')#Here they should do the nasty (exchange rowers)
                for i in range(4):
                    sperm = pair[0].makeGamets()
                    egg   = pair[1].makeGamets()
                    rowers = []
                    for place in range(self.boatSize):
                        allele0 = sperm[place]
                        allele1 = egg[place]
                        rowers.append(spot(position=place,rowers=[allele0,allele1]))
                    child = boat(self.cofactors, self.maxSpeed, self.domFacts, self.boatSize, rowers )
                    self.allDemes[d].append(child)
                #print(len(self.allDemes[d]))
        self.allBoats = []
        for deme in self.allDemes:
            self.allBoats = self.allBoats + deme
        self.allBoats.sort(key=op.attrgetter('boatSpeed'))#returns boats ordered from slowest to fastest
        self.calculateRowers()
        self.numBoats = len(self.allBoats)
        self.calculateFitness()
    def calculateFitness(self):
        self.fitness = 0
        for eachBoat in self.allBoats:
            self.fitness += eachBoat.boatSpeed
