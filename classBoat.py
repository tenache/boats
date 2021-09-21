# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:22:36 2021

@author: Usuario
"""
from classSpot import spot
import numpy as np
import random as rd
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
