__author__ = 'nparslow'

from  pylearn2.datasets.dense_design_matrix import DenseDesignMatrix
#from numpy.random import randint
from random import randint
import numpy as np
from pylearn2.models import mlp
from pylearn2.training_algorithms import sgd
from pylearn2.termination_criteria import EpochCounter
import theano


class XOR(DenseDesignMatrix):
    def __init__(self):
        self.class_names = ['0', '1']
        X = [[randint(0,1), randint(0,1)] for _ in range(1000)]
        y = []
        for a, b in X:

            if a + b == 1:
                y.append([0,1]) # first column for Y = ouput a zero (T/F), second column is output a one (T/F),
                #  i.e. softmax style
            else:
                y.append([1,0])
            #print a, b, a+b, y[-1]
        X = np.array(X)
        y = np.array(y)
        super(XOR, self).__init__(X=X, y=y)

ds = XOR()
#exit(0)

hidden_layer = mlp.Sigmoid(layer_name='hidden', dim=2, irange=.1, init_bias=1.)
# Sigmoid, initial weights -0.1 to 0.1  (irange), bias added with initial value 1.

output_layer = mlp.Softmax(2, 'output', irange=0.1)
# softmax output layer, 2 nodes, sum of all nodes will be 1

trainer = sgd.SGD(learning_rate=.05, batch_size=10, termination_criterion=EpochCounter(400))
# i.e. stop after 400 epochs


# initialise the network
layers = [hidden_layer, output_layer]
ann = mlp.MLP(layers, nvis=2)
trainer.setup(ann, ds)


# train until criteria is reached
while True:
    trainer.train(dataset=ds)
    ann.monitor.report_epoch()
    ann.monitor()
    if not trainer.continue_learning(ann):
        break


# test it works:
inputs = np.array([[0, 0]])
print ann.fprop(theano.shared(inputs, name='inputs')).eval()
inputs = np.array([[0, 1]])
print ann.fprop(theano.shared(inputs, name='inputs')).eval()
inputs = np.array([[1, 0]])
print ann.fprop(theano.shared(inputs, name='inputs')).eval()
inputs = np.array([[1, 1]])
print ann.fprop(theano.shared(inputs, name='inputs')).eval()