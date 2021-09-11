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


#class rower has speed and a dominance factor. 
class rower:
    def __init__(self,maxSpeed = 9, domFacts = 2):
        self.rowerSpeed = rd.randint(0,maxSpeed)
        self.dominance = rd.randint(0,domFacts)
#Two rowers make up one "spot". The dominant one of the two will determine the speed added to the boat it is in. 
class spot:
    def __init__(self,position,maxSpeed = 9, domFacts = 2):
        self.position = position
        self.rower0 = rower(maxSpeed,domFacts)
        self.rower1 = rower(maxSpeed,domFacts)
        if self.rower0.dominance > self.rower1.dominance:
            self.dominantOne = self.rower0
        elif self.rower0.dominance < self.rower1.dominance:
            self.dominantOne = self.rower1
        else:
            self.dominantOne = rd.choice([self.rower0,self.rower1])
        self.spotSpeed = self.dominantOne.rowerSpeed

class boat:
    def __init__(self,cofactors,maxSpeed = 9, domFacts=2, boatSize=9):
        self.spotS = []
        self.boatSpeed = 0
        self.allRowers = {}
        for location in range(boatSize):
            boatSeat = spot(location,maxSpeed,domFacts)
            self.spotS.append(boatSeat)
        for location in self.spotS:
            self.boatSpeed += location.spotSpeed
            for locationII in self.spotS:
                i = location.spotSpeed
                j = locationII.spotSpeed
                rowerInteraction = cofactors[i,j]
                self.boatSpeed += rowerInteraction
#add some randomness to your life:
        self.boatSpeed += np.random.normal(0,0.2,(1,1))

class boatGen:
    def __init__(self,maxSpeed=9,domFacts=2,boatSize=9,numBoats=1000):
        self.allBoats = []
        self.allGenRowers = {}
        for i in range(boatSize):
            self.allGenRowers[i] = {}
            for j in range(maxSpeed + 1):
                self.allGenRowers[i][j] = 0
        self.cofactors = np.random.normal(0,0.2,(boatSize+1,boatSize+1))
        for i in range(numBoats):
            rowBoat = boat(self.cofactors,maxSpeed,domFacts,boatSize)
            self.allBoats.append(rowBoat)
            for allele in rowBoat.allRowers:
                self.allGenRowers[allele] += rowBoat.allRowers[allele]
        self.allBoats.sort(key=op.attrgetter('boatSpeed'),reverse=True)
        for ind in self.allBoats:
            for locus in ind.spotS:
                allele0 = locus.rower0.rowerSpeed
                allele1 = locus.rower1.rowerSpeed
                print('locus position is ' + str(locus.position))
                print('allele is ' + str(allele0))
                self.allGenRowers[locus.position][allele0] += 1
                self.allGenRowers[locus.position][allele1] += 1
    #def select(self):
        
            
a = boatGen(numBoats=10)              
for individual in a.allBoats:
    print('speed is ' + str(individual.boatSpeed))

      

