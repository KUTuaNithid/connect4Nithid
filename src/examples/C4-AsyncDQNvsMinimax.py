#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 00:37:35 2018

@author: Arpit
"""

from games.c4Game import C4Game
from environment import Environment
from players.minimaxC4Player import MinimaxC4Player
from players.qPlayer import QPlayer
import games.c4Solver as C4Solver
from keras.models import Sequential
from keras.layers import Dense
from mathEq import MathEq
from myThread import MyThread
from memory.pMemory import PMemory
from brain import Brain

memory = PMemory(20000)
goodMemory = PMemory(20000)
threads = []
ROWS = 4
COLUMNS = 5

game = C4Game(ROWS, COLUMNS, name="dummy")

ann = Sequential()
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

brain = Brain('whatever', game, model=ann)

config = {}
config[1] = {"min":0.05, "max":0.05, "lambda":0}
config[2] = {"min":0.05, "max":0.25, "lambda":0}
config[3] = {"min":0.05, "max":0.35, "lambda":0}
config[4] = {"min":0.05, "max":0.45, "lambda":0}

eq2 = MathEq({"min":0, "max":0, "lambda":0})

i = 1
threads = []
while i <= 4:
    name = "asyncDQN" + str(i)
    game = C4Game(ROWS, COLUMNS, name=name)

    p1 = QPlayer(name, game, brain=brain, eEq=MathEq(config[i]), memory=memory, goodMemory=goodMemory, targetNet=False)
    p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)

    env = Environment(game, p1, p2, ePlot=False)
    threads.append(MyThread(env))
    i += 1

for t in threads:
    t.start()