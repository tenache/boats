# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:11:25 2021

@author: Usuario
"""
#spot is analogous to locus
#rower in analogous to allele
import random as rd
import numpy as np
import operator as op
import matplotlib.pyplot as plt


#class rower has speed and a dominance factor. 
class rower:
    def __init__(self,maxSpeed = 5, domFacts = 2):
        self.rowerSpeed = rd.randint(0,maxSpeed)
        self.dominance = rd.randint(0,domFacts)
#Two rowers make up one "spot". The dominant one of the two will determine the speed added to the boat it is in. 
class spot:
    def __init__(self,position,maxSpeed = 9, domFacts = 2,rowers = None):
        self.position = position
        if rowers == None:
            self.rower0 = rower(maxSpeed,domFacts)
            self.rower1 = rower(maxSpeed,domFacts)
        else:
            self.rower0 = rowers[0]
            self.rower1 = rowers[1]
        if self.rower0.dominance > self.rower1.dominance:
            self.dominantOne = self.rower0
        elif self.rower0.dominance < self.rower1.dominance:
            self.dominantOne = self.rower1
        else:
            self.dominantOne = rd.choice([self.rower0,self.rower1])
        self.spotSpeed = self.dominantOne.rowerSpeed

class boat:
    def __init__(self,cofactors,maxSpeed = 5, domFacts=2, boatSize=9, rowers = None):
        self.boatSpeed = 0
        self.cofactors = cofactors
        if rowers == None:
            self.spotS = []
            for location in range(boatSize):
                boatSeat = spot(location,maxSpeed,domFacts)
                self.spotS.append(boatSeat)
        else:
            self.spotS = rowers
        self.calculateSpeed()
    def calculateSpeed(self):
        for c,location in enumerate(self.spotS):
            self.boatSpeed += location.spotSpeed
            for d,locationII in enumerate(self.spotS):
                i = location.spotSpeed
                j = locationII.spotSpeed
                rowerInteraction = self.cofactors[c,d][i,j]
                self.boatSpeed += rowerInteraction
#add some randomness to your life:
        chance =  np.random.normal(0,10,(1,1))[0][0]  # numpy returns array or random numbers with normal distributions. accessing array to get a normal random number  
        self.boatSpeed += chance
    def makeGamets(self):
        gamete = []
        for location in self.spotS:
            gamete.append(rd.choice([location.rower0,location.rower1]))
        return gamete

class boatGen:
    def __init__(self,maxSpeed=7,domFacts=2,boatSize=9,numBoats=1000,panmixis = True):
        self.panmixis = panmixis
        self.numBoats = numBoats
        self.maxSpeed = maxSpeed
        self.domFacts = domFacts
        self.boatSize = boatSize
        self.allBoats = [] # a list of all the class instances of boats generating ghere
        self.allGenRowers = {} #This variable gives us a summary of all rowers and their numbers
        self.cofactors = np.empty((self.boatSize,self.boatSize),dtype=np.ndarray)
        for i in range(self.boatSize):#i represents the position on the boat (the locus)
            self.allGenRowers[i] = {}#First we generate the empty dictionaries for all possibilities
            for j in range(self.maxSpeed + 1):#j is the allele, the name of the genes. In this case is also speed. 
                self.allGenRowers[i][j] = [0]
        for i in range(self.boatSize):
            for j in range (self.boatSize):
                self.cofactors[i,j]=np.random.normal(0,15,(self.maxSpeed +1,self.maxSpeed+1))
        for i in range(numBoats):#here we generate the boats
            rowBoat = boat(self.cofactors,maxSpeed,domFacts,boatSize)
            self.allBoats.append(rowBoat)
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
        #print(f'all boats are before select:{len(self.allBoats)}')
        midWay = int(self.numBoats/2)
        #print(f'midway is{midWay} , and numBoats is {self.numBoats}')
        del self.allBoats[0:midWay]
        #print(f'all boats are after select:{len(self.allBoats)}')
        self.calculateRowers()
        self.numBoats = len(self.allBoats)
        self.calculateFitness()
    def mate(self):
        #print('inside mate, minimum?')
        bachellors = self.allBoats.copy()
        rd.shuffle(bachellors)#take away if we want panmixis
        #print('bachellor length is ' + str(len(bachellors)))
        marriedBoats = []
        while len(bachellors) > 1:#This loops divides boats into pair of boats
            #print('Am I not getting into this loop?') 
            if len(bachellors) < 7 or self.panmixis ==True:
                husband = bachellors.pop(rd.randint(0,len(bachellors) -1))
                wife = bachellors.pop(rd.randint(0,len(bachellors) - 1))
            elif self.panmixis == False:#take away if we want panmixis
                husband = bachellors.pop(rd.randint(0,5))
                wife = bachellors.pop(rd.randint(0,5))
            marriedBoats.append([husband,wife])
            #print(husband)
        self.allBoats = []#Don't want to get stuck with an odd number of boats, so if there's a single bachellor without a mate, it's gone
        for c,pair in enumerate(marriedBoats):
            #print('Am I getting into this loop?')#Here they should do the nasty (exchange rowers)
            for i in range(4):
                #print(f'i is {i}')
                #print('Am I even here?')
                sperm = pair[0].makeGamets()
                egg   = pair[1].makeGamets()
                rowers = []
                for place in range(self.boatSize):
                    #print('Am I here?')
                    allele0 = sperm[place]
                    allele1 = egg[place]
                    rowers.append(spot(position=place,rowers=[allele0,allele1]))
                    child = boat(self.cofactors, self.maxSpeed, self.domFacts, self.boatSize, rowers )
                self.allBoats.append(child)
                #print(f'number of boats is {len(self.allBoats)}, i is {i}, c is {c}')

        #print(self.allBoats)
        self.allBoats.sort(key=op.attrgetter('boatSpeed'))#returns boats ordered from slowest to fastest
        self.calculateRowers()
        self.numBoats = len(self.allBoats)
        self.calculateFitness()
    def calculateFitness(self):
        self.fitness = 0
        for boat in self.allBoats:
            self.fitness += boat.boatSpeed

                
     
a = boatGen(numBoats=5000)              
for individual in a.allBoats:
    print('speed is ' + str(individual.boatSpeed))
print(a.allGenRowers)
#a.select()
#a.mate()
# print(a.allGenRowers)
allGenerations = a.allGenRowers
allSpeeds = [a.fitness]

numberOfGenerations = 100
for i in range(numberOfGenerations):

    a.select()
    a.mate()
    allSpeeds.append(a.fitness)
    for j in range(a.boatSize):
        for z in range(a.maxSpeed + 1):
            allGenerations[j][z] = allGenerations[j][z] + a.allGenRowers[j][z]
allPlots = {}
figures = []
#plt.figure()
for locus in range(a.boatSize):
    figures.append(plt.figure())
    legend = []
    allPlots[locus] = []
    for allele in range(a.maxSpeed + 1):
        allPlots[locus].append(plt.plot(allGenerations[locus][allele]))
        legend.append(f'locus:{locus},allele:{allele}')
    plt.legend(legend, loc = 'upper left')
    plt.show()
        
        
speedFigure = plt.figure()
boatSpeedPlot = plt.plot(allSpeeds)

    


      

