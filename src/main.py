#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 18:46:51 2018

@author: Arpit
"""
import time
from games.c4Game import C4Game
#from games.t3Game import T3Game
from player import Player

start = time.time()

def observeSample(lastS, lastA):
    p = p1 if (game.turnCnt + flag) % 2 == 0 else p2
    
    r = game.getReward(p.name)
    s_ = game.getCurrentState() if not game.isOver() else None

    sample = (lastS, lastA, r, s_)
    p.observe(sample, game.gameCnt)
    p.replay()
    
debug = False

game = C4Game(6,7)
#game = T3Game()
stateCnt, actionCnt = game.getStateActionCnt()
p1 = Player(1, stateCnt, actionCnt, debug)
p2 = Player(2, stateCnt, actionCnt, debug)

while not debug or game.gameCnt < 2:
    game.newGame()
    
    if game.gameCnt % 2 == 0:
        game.setFirstToPlay(2)
        game.p2act()
    
    while not game.isOver():
        s = game.getCurrentState()
        a = p1.act(s, game.getIllMoves())
        s_, r = game.getNextState(a)
        sample = (s, a, r, s_)
        
        p1.observe(sample, game)
        p1.replay()

    flag = 0
#    if game.gameCnt % 2 == 0:
#        game.setFirstToPlay(2)
#        flag = 1
#        
#    lastS = None
#    lastA = None
#    while not game.isOver():
#        p = p1 if (game.turnCnt + flag) % 2 == 0 else p2
#        
#        s = game.getCurrentState()
#        a = p.act(s, game.getIllMoves())
#        game.step(a)
#
#        if lastS is not None:
#            observeSample(lastS, lastA)
#        
#        lastS = s
#        lastA = a
#        
#    game.turnCnt += 1
#    observeSample(lastS, lastA)
    
    if game.gameCnt % 100 == 0 or debug:
        game.printGame()
        print ("Exploration Rate: " + str(p1.epsilon))
        print ("Learning Rate: " + str(p1.alpha))
        game.clearStats()
        print("Time since beginning: " + str(time.time() - start))

if debug:
    w1 = p1.ANN.ann.get_weights()
    sample1 = p1.memory.sample(64)
    locals().update(p1.logs)
