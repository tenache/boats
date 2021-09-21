# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:21:41 2021

@author: Usuario
"""
import random as rd
#class rower has speed and a dominance factor. 
class rower:
    def __init__(self,maxSpeed = 5, domFacts = 2):
        self.rowerSpeed = rd.randint(0,maxSpeed)
        self.dominance = rd.randint(0,domFacts)
#Two rowers make up one "spot". The dominant one of the two will determine the speed added to the boat it is in. 
