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
#Example 1
game = C4Game(4, 5, name="test1")

ann = Sequential()
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

eq1 = MathEq({"min":0, "max":0.05, "lambda":0})
eq2 = MathEq({"min":0, "max":0.25, "lambda":0})

brain = Brain('whatever', game, model=ann)

p1 = QPlayer(1, game, brain=brain, eEq=eq1, memory=memory, goodMemory=goodMemory, targetNet=False)
p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)
env = Environment(game, p1, p2)
threads.append(MyThread(env))

#Example 2
game = C4Game(4, 5, name="test2")

ann = Sequential()
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

eq1 = MathEq({"min":0, "max":0.25, "lambda":0})
eq2 = MathEq({"min":0, "max":0.05, "lambda":0})
eq2 = MathEq({"min":0, "max":0.25, "lambda":0})

p1 = QPlayer(1, game, brain=brain, eEq=eq1, memory=memory, goodMemory=goodMemory, targetNet=False)
p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)
env = Environment(game, p1, p2)
#env.run()
threads.append(MyThread(env))

#Example 3
game = C4Game(4, 5, name="test3")

ann = Sequential()
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

eq1 = MathEq({"min":0, "max":0.35, "lambda":0})
eq2 = MathEq({"min":0, "max":0.05, "lambda":0})
eq2 = MathEq({"min":0, "max":0.25, "lambda":0})

p1 = QPlayer(1, game, brain=brain, eEq=eq1, memory=memory, goodMemory=goodMemory, targetNet=False)
p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)
env = Environment(game, p1, p2)
threads.append(MyThread(env))

#Example 4
game = C4Game(4, 5, name="test4")

ann = Sequential()
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

eq1 = MathEq({"min":0, "max":0.45, "lambda":0})
eq2 = MathEq({"min":0, "max":0.05, "lambda":0})
eq2 = MathEq({"min":0, "max":0.25, "lambda":0})

p1 = QPlayer(1, game, brain=brain, eEq=eq1, memory=memory, goodMemory=goodMemory, targetNet=False)
p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)
env = Environment(game, p1, p2)
threads.append(MyThread(env))

for t in threads:
    t.start()