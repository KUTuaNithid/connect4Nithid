#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 18:23:00 2018

@author: Arpit
"""

from games.c4Game import C4Game
from environment import Environment
from players.minimaxC4Player import MinimaxC4Player
from players.pgPlayer import PGPlayer
from mathEq import MathEq
from pgBrain import Brain
from optimizer import Optimizer
from myThread import MyThread
from keras.layers import Input, Dense
from keras.models import Model, load_model
import games.c4Solver as C4Solver
import os.path

GAMMA = 0.99
N_STEP_RETURN = 3
GAMMA_N = GAMMA ** N_STEP_RETURN
MIN_BATCH = 1024
ROWS = 6
COLUMNS = 7
filename = "pgbrain67"

game = C4Game(ROWS, COLUMNS, name="dummy")

l_input = Input( batch_shape=(None, game.stateCnt) )
l_dense = Dense(48, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(l_input)
l_dense = Dense(48, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(l_dense)
l_dense = Dense(24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(l_dense)
l_dense = Dense(24, kernel_initializer='random_uniform', bias_initializer='random_uniform', activation='relu')(l_dense)

out_actions = Dense(game.actionCnt, activation='softmax')(l_dense)
out_value   = Dense(1, activation='linear')(l_dense)

model = Model(inputs=[l_input], outputs=[out_actions, out_value])

if os.path.exists(filename + ".h5"):
    model = load_model(filename + ".h5")
    print (filename + " model loaded")
    
model._make_predict_function()	# have to initialize before threading

brain = Brain(filename, game, model=model, min_batch=MIN_BATCH, gamma=GAMMA, n_step=N_STEP_RETURN, gamma_n=GAMMA_N)

config = {}
config[1] = {"min":0.05, "max":0.05, "lambda":0}
config[2] = {"min":0.05, "max":0.25, "lambda":0}
config[3] = {"min":0.05, "max":0.35, "lambda":0}
config[4] = {"min":0.05, "max":0.45, "lambda":0}

eq2 = MathEq({"min":0.05, "max":0.45, "lambda":0})

i = 1
threads = []
while i <= 4:
    name = "test" + str(i)
    game = C4Game(ROWS, COLUMNS, name=name)
    p1 = PGPlayer(name, game, brain=brain, eEq=MathEq(config[i]))
    p2 = MinimaxC4Player(2, game, eEq=eq2, solver=C4Solver)

    env = Environment(game, p1, p2, ePlot=False)
    threads.append(MyThread(env))
    i += 1

opts = [Optimizer(brain) for i in range(2)]
for o in opts:
    o.start()
for t in threads:
    t.start()