#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 15:16:06 2018

@author: Arpit
"""
import numpy as np
import matplotlib.pyplot as plt

class GraphPlot:
    def __init__(self, name, xCnt=1, yCnt=1, labels=None):
        self.name = name
        self.xCnt = xCnt
        self.yCnt = yCnt
        self.labels = labels
        
        self.X = []
        self.Ys = np.empty((yCnt,), dtype=object)
        for i,v in enumerate(self.Ys): self.Ys[i] = list()

    def add(self, X, Y):
        self.X.append(X)
        
        for i in range(self.yCnt):
            self.Ys[i].append(Y[i])
    
    def show(self):
        plt = self.save(True)
        plt.draw()
        plt.show()
        plt.close(self.fig)
    
    def save(self, show=False):
        self.fig = plt.figure()
        for i in range(self.yCnt):
            plt.plot(self.X, self.Ys[i], label=self.labels[i] if self.labels is not None else i)
        
        plt.legend(loc = "best")
        plt.savefig('/Users/Arpit/Desktop/' + str(self.name) + '.png')
       
        if not show: plt.close(self.fig)
        
        return plt