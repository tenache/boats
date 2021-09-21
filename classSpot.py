# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:22:19 2021

@author: Usuario
"""
from classRower import rower
import random as rd
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