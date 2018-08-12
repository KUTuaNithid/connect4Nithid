#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 20:19:38 2018

@author: Arpit
"""
from players.testPlayer import TestPlayer

class Evaluator:
    def __init__(self, game):
        self.game = game
        self.t1 = None
        self.t2 = None
        self.env = None
    
    def evaluate(self, model1, model2):
        if self.t1 is None:
            from environment import Environment
            self.t1 = TestPlayer(model1, self.game, epsilon=0.05)
            self.t2 = TestPlayer(model2, self.game, epsilon=0.05)
            self.env = Environment(self.game, self.t1, self.t2, training=False, observing=False)
        else:
            self.t1.brain.load_weights(model1)
            self.t2.brain.load_weights(model2)
            
        self.game.save()
        self.game.clearStats(True)
        
        for _ in range(500):
           self.env.runGame()
        
        wins = self.game.getTotalWins()
        if wins[0]*1.05 < wins[1]:
            result = False
        else:
            result = True
            
        self.env.printEnv()
        self.game.load()
        return result