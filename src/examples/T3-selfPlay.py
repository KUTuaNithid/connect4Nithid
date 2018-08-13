#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:02:25 2018

@author: Arpit
"""

from games.t3Game import T3Game
from environment import Environment
from players.zeroPlayer import ZeroPlayer
from memory.dictTree import DictTree
from brains.zeroBrain import ZeroBrain
from keras.utils import plot_model
from collections import deque

game = T3Game(3, isConv=True)
hidden_layers = [
	{'filters':32, 'kernel_size': (2,2)}
	 , {'filters':32, 'kernel_size': (2,2)}
	]

player_config = {"tree":DictTree(), "longTermMem":deque(maxlen=5000), "load_weights":False, 
                 "epsilon":0.20, "dirAlpha":0.3, "simCnt":40, "iterPer":40,
                 "turnsToTau0":4}
brain_config = {"learning_rate":0.001, "momentum":0.9, "batch_size":32, "epochs":5,
                "hidden_layers":hidden_layers}
env_config = {"switchFTP":False, "evaluate":True, "evalPer":200}

brain = ZeroBrain("1", game, hidden_layers = hidden_layers, **brain_config)
plot_model(brain.model, show_shapes=True, to_file='/Users/Arpit/Desktop/model.png')

p1 = ZeroPlayer(1, game, brain=brain, **player_config)
p2 = ZeroPlayer(2, game, brain=brain, **player_config)
env = Environment(game, p1, p2, **env_config)
env.run()
