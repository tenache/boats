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
    def __init__(self,maxSpeed=7,domFacts=2,boatSize=9,demeSize=20,demes=1,migrationP=1):
        self.migrationP = migrationP
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
        deme = -1
        for i in range(self.demes):#here we generate the boats
            deme += 1
            for j in range(self.demeSize):
                rowBoat = boat(self.cofactors,maxSpeed,domFacts,boatSize)
                rowBoat.deme = deme
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
                self.allGenRowers[locus.position][allele0][0] += 1#add rowers in boat to the allgenRowers summary
                self.allGenRowers[locus.position][allele1][0] += 1#remember there are two rowers per "spot" or position in the boat
    def select(self):#selects the best half of boats
        self.allBoats.sort(key=op.attrgetter('boatSpeed'))
        midWay = int(self.numBoats/2)
        quarterWay = int(self.numBoats/4)
        del self.allBoats[0:quarterWay]#delete inadequeate boats
        quarterSpeed = self.allBoats[0].boatSpeed
        #self.allBoats = []
        for i,deme in enumerate(self.allDemes):#this loops eliminates boats from allDemes
            j = 0
            demeLen = len(deme)
            deme.sort(key=op.attrgetter('boatSpeed'))
            quartDWay = int(demeLen/4) + 1
            quartDSpeed = deme[quartDWay].boatSpeed
            for z in range(demeLen):
#This selects partly by deme, partly by total population. I'm not sure how good a representation of biology this is
#but I am trying to mimic the fact that there are several pressures, applied by members 
#of same species but also selected by other factors
                if deme[j].boatSpeed < quarterSpeed or deme[j].boatSpeed < quartDSpeed :
                    del self.allDemes[i][j]
                    if len(deme) == 0:
                        print(f'deme {i} has gone extinct')
                        del self.allDemes[i]
                        self.demes -= 1
                else:
                    j += 1
            self.allDemes[i].sort(key=op.attrgetter('boatSpeed'))
            self.allBoats += deme
        sumDeme = 0
        for deme in self.allDemes:
            sumDeme += len(deme)
        for i in range(sumDeme - midWay):
            randDeme = rd.randint(0,len(self.allDemes) - 1)
            del self.allDemes[randDeme][0]#a bit of randomness never hurt anyone

        self.allBoats = []
        for deme in self.allDemes:
            self.allBoats += deme
        
        self.calculateRowers()
        self.numBoats = len(self.allBoats)
        self.calculateFitness()
    def migrate(self):
        for i,deme in enumerate(self.allDemes):
#Determine how many times each deme will migrate. Directly proportional to the number 
#of  boats each deme has and the proportion of all the boats in the generation. 
            demeMigrPow=round((len(deme)**2/self.numBoats)*self.migrationP*rd.random()) 
            for j in range(demeMigrPow):#the range can be anything from 0 to large numbers
                randDeme = rd.randint(0,self.demes -1)
                try:#just in case there is an error regarding number of boats from previously called methods. 
                    randBoat = rd.randint(0,len(deme) - 1)
                except ValueError:
                    print('no Boats in this deme, error')
                try:
                    deme[randBoat].deme = randDeme
                    self.allDemes[randDeme].append(deme.pop(randBoat))#appends a random boat from the current deme to a random deme. 
                    if len(deme) == 0:
                        del self.allDemes[i]
                        self.demes -= 1
                        print(f'deme number {i} has gone extinct')
                except IndexError:
                    print(f'randBoat is {randBoat},deme length is {len(deme)}')
    def mate(self):
        bachellors = self.allDemes.copy()#do I need the bachellors still? 
        for deme in bachellors:
            rd.shuffle(deme)#this will allow mating to be random (panmictic) within the deme.
        marriedBoats = []#married boats will have the same structure as allDemes, but boats wil be organized in the reproductive pairs
        for d,deme in enumerate(bachellors):
            marriedBoats.append([])
            while len(deme) > 1:#keep popping from the bachellors and appending it to the married boats in pairs
                husband = deme.pop(rd.randint(0,len(deme) -1))
                wife = deme.pop(rd.randint(0,len(deme)- 1))
                marriedBoats[d].append([husband,wife])
        self.allDemes = []#Don't want to get stuck with an odd number of boats, so if there's a single bachellor without a mate, it's gone
        for d,deme in enumerate(marriedBoats):
            self.allDemes.append([])
            for c,pair in enumerate(deme):
                for i in range(4):
                    sperm = pair[0].makeGamets()#makeGamets gives us something that has one rower per place on the boat
                    egg   = pair[1].makeGamets()#I'm not separating in sexes, so egg and sperm are just names. 
                    rowers = []
                    for place in range(self.boatSize):
                        allele0 = sperm[place]
                        allele1 = egg[place]
                        rowers.append(spot(position=place,rowers=[allele0,allele1]))
                    child = boat(self.cofactors, self.maxSpeed, self.domFacts, self.boatSize, rowers )
                    self.allDemes[d].append(child)
            if len(bachellors[d]) == 1:#this section is to assure that the same number of boats we had originally remain after mating. 
                for i in range(2):
                    self.allDemes[d].append(bachellors[d][0])#one lucky bachellor gets to reproduce asexually
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
