#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 17:53:30 2018

@author: Arpit
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os.path
import tensorflow as tf
from keras import backend as K

class Brain:
    def __init__(self, name, game, model=None):
        self.filename = str(name) + '.h5'
        self.stateCnt, self.actionCnt = game.getStateActionCnt()
        
        self.session = tf.Session()
        K.set_session(self.session)
        K.manual_variable_initialization(True)

        if model is None:
            self.model = self._buildModel()
        else:
            self.model = model
        
        model._make_predict_function()
        model._make_train_function()
        
        self.session.run(tf.global_variables_initializer())
        self.default_graph = tf.get_default_graph()

    def _buildModel(self):
        model = Sequential()
        model.add(Dense(units = int((self.stateCnt + self.actionCnt)/2),
                      kernel_initializer='random_uniform',
                      bias_initializer='random_uniform',
                      activation = 'relu',
                      input_dim = self.stateCnt))
        model.add(Dense(units = self.actionCnt,
                      kernel_initializer='random_uniform',
                      bias_initializer='random_uniform',
                      activation = 'linear'))
        model.compile(optimizer = 'rmsprop', loss = 'logcosh', metrics = ['accuracy'])
        return model
    
    def predict(self, s):
        with self.default_graph.as_default():
            return self.model.predict(s)

    def train(self, x, y, batch_size, verbose):
        with self.default_graph.as_default():
            self.model.fit(x, y, batch_size=batch_size, verbose=verbose)
        
    def save(self):
        with self.session:
            self.model.save(self.filename)
        
    def load(self, filename):
        filename = str(filename) + '.h5'
        if os.path.exists(filename):
            print (filename + " model loaded")
            self.model = load_model(filename)
        else:
            print("Error: file " + filename + " not found")