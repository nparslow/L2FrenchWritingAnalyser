__author__ = 'nparslow'

import theanets
import numpy as np

# for alternatives using Theano:
# https://github.com/gwtaylor/theano-rnn/blob/master/basic_rnn_example.py
# https://groups.google.com/forum/#!topic/theano-users/OcdVuTZ19Dc



# goal is to remember first K values then reproduce them after T time steps

BATCH_SIZE = 32

exp = theanets.Experiment( # Experiment covers training and evaluation
    theanets.recurrent.Regressor, # recurrent regression model
    layers=(1, ('lstm', 10), 1), # 3 layers, first = 1 input unit,
                                # second = LSTM (long short-term-memory) with 10 units (recurrent)
                                # 1 output layer
                                # note there are other ways of specifying layers
    batch_size=BATCH_SIZE)

# need input and output arrays, each has 3 dimensions (time, batch_size, no. inputs/outputs in dataset)

T = 20
K = 3

def generate(): # s is training, t is validation?
    # make a 2 x T x BATCH_SIZE x 1 array of normal randoms, then split into s & t, each with T*BATCH_SIZE x 1
    s, t = np.random.randn(2, T, BATCH_SIZE, 1).astype('f')
    # take the first K lines of s, and set to same as last K lines of t but with remade random, not sure why
    #print t[-K:].shape
    s[:K] = t[-K:] = np.random.randn(K, BATCH_SIZE, 1)
    return [s,t]

# train
exp.train(generate, optimize='rmsprop')

# Experiment.save and Experiment.load
# save_every, save_progress
