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
from envThread import EnvThread
from memory.pMemory import PMemory
from brain import Brain
#from keras import optimizers

loadWeights = True
randBestMoves = False

GAMMA = 0.99
N_STEP_RETURN = 13

memory = PMemory(2000)
goodMemory = PMemory(2000)
threads = []
ROWS = 5
COLUMNS = 6
BATCH_SIZE = 64

#make first move by minimax random otherwise perfect play 

game = C4Game(ROWS, COLUMNS, name="dummy")

ann = Sequential()
ann.add(Dense(units = 45, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu', input_dim = game.stateCnt))
ann.add(Dense(units = 25, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = 16, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'relu'))
ann.add(Dense(units = game.actionCnt, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation = 'linear'))

#rmsprop = optimizers.RMSprop(lr=0.005, decay=0.99)
ann.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])

brain = Brain('c4Async', game, model=ann, loadWeights=loadWeights)

config = {}
config[1] = {"min":0.05, "max":0.05, "lambda":0}
config[2] = {"min":0.05, "max":0.25, "lambda":0}
config[3] = {"min":0.05, "max":0.35, "lambda":0}
config[4] = {"min":0.05, "max":0.45, "lambda":0}

eq2 = MathEq({"min":0, "max":0, "lambda":0.00001})

i = 1
threads = []
while i <= 4:
    name = "asyncDQN45-1" + str(i)
    game = C4Game(ROWS, COLUMNS, name=name)

    p1 = QPlayer(name, game, brain=brain, eEq=MathEq(config[i]),
                 memory=memory, goodMemory=goodMemory, targetNet=False, batch_size=BATCH_SIZE,
                 gamma=GAMMA, n_step=N_STEP_RETURN)
    p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver, rand=randBestMoves)

    env = Environment(game, p1, p2, ePlot=False)
    threads.append(EnvThread(env))
    i += 1

for t in threads:
    t.start()
