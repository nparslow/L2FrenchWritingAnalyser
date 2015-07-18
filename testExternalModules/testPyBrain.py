__author__ = 'nparslow'


from pybrain.tools.shortcuts import buildNetwork

from pybrain.structure import TanhLayer
from pybrain.structure import SoftmaxLayer

from pybrain.datasets import SupervisedDataSet # to set up data

from pybrain.supervised.trainers import BackpropTrainer # to train

from pybrain.utilities import percentError


v = 50000 # vocab size
d = 100 # reduced dimensionality vocab size
h = 60 # hidden layer size : todo how big should it be???

# simple feed-forward network
# 2 inputs, 3 hidden and 1 output neurons, hidden = sigmoid by default
# bias=True means use a bias
net = buildNetwork(2, 3, 1, hiddenclass=TanhLayer,  bias=True) # outclass=SoftmaxLayer,

ds = SupervisedDataSet(2, 1) # 2-D input params, one-D output param

# add data:, pair of tuples, 1st is input, second is output
for i in range(100): # with only 4 datapoints it won't learn
    ds.addSample((0, 0), (0,))
    ds.addSample((0, 1), (1,))
    ds.addSample((1, 0), (1,))
    ds.addSample((1, 1), (0,))


trainer = BackpropTrainer(net, ds) # , weightdecay=0.1

a = trainer.train() # train for one full epoch
print a # a double, proportional to the error

b = trainer.trainUntilConvergence() # train until convergence # by default the validation proportion is 0.25
# so the example in the quickstart guide will never work with just 4 data points!!!!
# dataset=None, maxEpochs=None, verbose=None, continueEpochs=10, validationProportion=0.25
print b # tuple containing errors for each training epoch

print net.activate( (0, 0) )
print net.activate( [0, 0] )
print net.activate([0, 1])
print net.activate([1, 0])
print net.activate([1, 1])

print net.params

trnresult = percentError( trainer.testOnClassData(),
                              ds )
print trnresult