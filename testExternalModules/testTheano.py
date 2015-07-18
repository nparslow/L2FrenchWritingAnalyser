__author__ = 'nparslow'

from theano import *

import theano.tensor as T

from theano import function
from theano import pp

import numpy as np

'''
simple arithmetic example
'''

'''
x = T.dscalar('x') # name 'x' is optional but helps with debugging
y = T.dscalar('y')
z = x + y # z will be defined as a variable associated with a computation
f = function([x,y], z) # this will be compiled into C code
# input and output can be single variables or lists of variables

print f(2,3)
print f(16.3, 12.1)

print type(x)
print pp(z)
print z.eval({x: 16.3, y: 12.1}) # eval can do some of the stuff that function can do
'''

'''
matrices example
'''
'''
x = T.dmatrix('x')
y = T.dmatrix('y')
z = x + y
f = function([x,y], z)

print f([[1,2], [3,4]], [[10,20], [30,40]])

print f(np.array([[1,2], [3,4]]), np.array([[10,20], [30,40]]))
'''

'''
exercise
'''
'''
a = theano.tensor.vector() # declare variable
b = theano.tensor.vector()
#out = a + a ** 10 # build symbolic expression
out = a **2 + b**2 + 2*a*b
#f = theano.function([a], out) # compile function
f = theano.function([a, b], out) # compile function
#print f([0,1,2])
print f([0,1,2],[1,2,3])
'''


'''
logistic function
'''
'''
x = T.dmatrix('x')
s = 1 / (1 + T.exp(-x))
logistic = function([x], s)
print logistic([[0,1], [-1, -2]]) # performed element-wise as each element of s is performed element-wise

# logistic = (1+tanh(x/2))/2
s2 = (1 + T.tanh(x/2)) / 2
logistic2 = function([x], s2)
print logistic2([[0,1], [-1, -2]])

# computing more than one thing at the same time
a, b = T.dmatrices('a', 'b') # can define multiple variables at the same time with the plural form
diff = a - b
abs_diff = abs(diff)
diff_squared = diff**2
f = function([a,b], [diff, abs_diff, diff_squared]) # output = all three
print f([[1,1], [1,1]], [[0,1], [2,3]])
'''

'''
setting a default value for an argument
'''
'''
from theano import Param
x, y = T.dscalars('x', 'y')
z = x + y
f = function([x, Param(y, default=1)], z) # inputs with defaults must follow ones without
print f(33), f(33,2)

# can set a param by name:
x,y,w = T.dscalars('x', 'y', 'w')
z = (x+y) * w
f = function([x, Param(y, default=1), Param(w, default=2, name='w_by_name')], z)
print f(33), f(33,2), f(33, 0, 1), f(33, w_by_name=1), f(33, w_by_name=1, y=0) # note y also by name
'''

'''
function with an internal state (e.g. an accumulator)
'''
'''
from theano import shared
state = shared(0) # shared between mulitple functions, use .get_value() and .set_value()
inc = T.iscalar('inc')
accumulator = function([inc], state, updates=[(state, state+inc)])
# updates takes a list of 2-tuples (shared variable, new expression)
# or a dictionary mapping shared variable to new expression
print state.get_value()
print accumulator(1) # note this will print the state value before the function is applied ????
print state.get_value()
print accumulator(300)
print state.get_value()
state.set_value(-1) # to change the value of the shared variable
print accumulator(3)
print state.get_value()

decrementer = function([inc], state, updates=[(state, state - inc)])
print decrementer(2)
print state.get_value()

# if you have a function using a state, but you want to use a non-state value:
fn_of_state = state * 2 + inc
# The type of foo must match the shared variable we are replacing with 'givens'
foo = T.scalar(dtype=state.dtype)
skip_shared = function([inc, foo], fn_of_state, givens=[(state, foo)]) # swap foo for state
print skip_shared(1,3)
print state.get_value()
'''

'''
random numbers
'''
'''
from theano.tensor.shared_randomstreams import RandomStreams
from theano import function
srng = RandomStreams(seed=234)
rv_u = srng.uniform((2,2)) # random stream of 2x2 matrices
rv_n = srng.normal((2,2))
f = function([], rv_u)
g = function([], rv_n, no_default_updates=True)  # not updating rv_n.rng
nearly_zeros = function([], rv_u + rv_u - 2 * rv_u) # same rv_u value will be used 3 times internally
f_val0 = f()
f_val1 = f()
print f_val0, f_val1 # different values each time
g_val0 = g()
g_val1 = g()
print g_val0, g_val1 # no update so same value each time

# seeding streams
rng_val = rv_u.rng.get_value(borrow=True) # Get the rng for rv_u
rng_val.seed(89234) # seeds the generator
rv_u.rng.set_value(rng_val, borrow=True) # Assign back seeded rng

state_after_v0 = rv_u.rng.get_value().get_state()
nearly_zeros() # this affects rv_u's generator
v1 = f()
rng = rv_u.rng.get_value(borrow=True)
rng.set_state(state_after_v0)
rv_u.rng.set_value(rng, borrow=True)
v2 = f()  # v2 != v1
v3 = f()  # v3 == v1
print v1, v2, v3

# copying a random state
import theano
import numpy
import theano.tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams
from theano.tensor.shared_randomstreams import RandomStreams

class Graph():
    def __init__(self, seed=123):
        self.rng = RandomStreams(seed)
        self.y = self.rng.uniform(size=(1,))

g1 = Graph(seed=123)
f1 = theano.function([], g1.y)

g2 = Graph(seed=987)
f2 = theano.function([], g2.y)

print 'By default, the two functions are out of sync.'
print 'f1() returns ', f1()
print 'f2() returns ', f2()

def copy_random_state(g1, g2):
    if isinstance(g1.rng, MRG_RandomStreams):
        g2.rng.rstate = g1.rng.rstate
    for (su1, su2) in zip(g1.rng.state_updates, g2.rng.state_updates):
        su2[0].set_value(su1[0].get_value())

print 'We now copy the state of the theano random number generators.'
copy_random_state(g1, g2)
print 'f1() returns ', f1()
print 'f2() returns ', f2()
'''

'''
Logistic Regression
'''
'''
import numpy
import theano
import theano.tensor as T
rng = numpy.random

N = 400 # no. of data points
feats = 784 # no. of features
D = (rng.randn(N, feats), rng.randint(size=N, low=0, high=2)) # D = data, note 'high=2' means max is 1 (i.e. y is 0 or 1)
#print D
training_steps = 10000

# Declare Theano symbolic variables
x = T.matrix("x")
y = T.vector("y")
w = theano.shared(rng.randn(feats), name="w")
b = theano.shared(0., name="b")
print "Initial model:"
print w.get_value(), b.get_value()

# Construct Theano expression graph
p_1 = 1 / (1 + T.exp(-T.dot(x, w) - b))   # Probability that target = 1
prediction = p_1 > 0.5                    # The prediction thresholded
xent = -y * T.log(p_1) - (1-y) * T.log(1-p_1) # Cross-entropy loss function
cost = xent.mean() + 0.01 * (w ** 2).sum()# The cost to minimize (with regularisation term)
gw, gb = T.grad(cost, [w, b])             # Compute the gradient of the cost
                                          # (we shall return to this in a
                                          # following section of this tutorial)

# Compile
train = theano.function(
          inputs=[x,y],
          outputs=[prediction, xent],
          updates=((w, w - 0.1 * gw), (b, b - 0.1 * gb)))
predict = theano.function(inputs=[x], outputs=prediction)

# Train
for i in range(training_steps):
    pred, err = train(D[0], D[1])

print "Final model:"
print w.get_value(), b.get_value()
print "target values for D:", D[1]
print "prediction on D:", predict(D[0])
'''

'''
to show the graph
'''
import theano
import theano.tensor as T

import numpy

import os

rng = numpy.random

N = 400
feats = 784
D = (rng.randn(N, feats).astype(theano.config.floatX),
rng.randint(size=N,low=0, high=2).astype(theano.config.floatX))
training_steps = 10000

# Declare Theano symbolic variables
x = T.matrix("x")
y = T.vector("y")
w = theano.shared(rng.randn(feats).astype(theano.config.floatX), name="w")
b = theano.shared(numpy.asarray(0., dtype=theano.config.floatX), name="b")
x.tag.test_value = D[0]
y.tag.test_value = D[1]
#print "Initial model:"
#print w.get_value(), b.get_value()


# Construct Theano expression graph
p_1 = 1 / (1 + T.exp(-T.dot(x, w) - b)) # Probability of having a one
prediction = p_1 > 0.5 # The prediction that is done: 0 or 1
xent = -y * T.log(p_1) - (1 - y) * T.log(1 - p_1) # Cross-entropy
cost = xent.mean() + 0.01 * (w ** 2).sum() # The cost to optimize
gw,gb = T.grad(cost, [w, b])

# Compile expressions to functions
train = theano.function(
            inputs=[x, y],
            outputs=[prediction, xent],
            updates=[(w, w - 0.01 * gw), (b, b - 0.01 * gb)],
            name="train")
predict = theano.function(inputs=[x], outputs=prediction,
            name="predict")

if any([x.op.__class__.__name__ in ['Gemv', 'CGemv'] for x in
        train.maker.fgraph.toposort()]):
    print 'Used the cpu'
elif any([x.op.__class__.__name__ == 'GpuGemm' for x in
         train.maker.fgraph.toposort()]):
    print 'Used the gpu'
else:
    print 'ERROR, not able to tell if theano used the cpu or the gpu'
    print train.maker.fgraph.toposort()


for i in range(training_steps):
    pred, err = train(D[0], D[1])
#print "Final model:"
#print w.get_value(), b.get_value()

print "target values for D"
print D[1]

print "prediction on D"
print predict(D[0])


# Print the picture graphs
# after compilation
if not os.path.exists('pics'):
    os.mkdir('pics')
theano.printing.pydotprint(predict,
                           outfile="pics/logreg_pydotprint_predic.png",
                           var_with_name_simple=True)
# before compilation
#theano.printing.pydotprint_variables(prediction,
theano.printing.pydotprint(prediction,
                           outfile="pics/logreg_pydotprint_prediction.png",
                           var_with_name_simple=True)
theano.printing.pydotprint(train,
                           outfile="pics/logreg_pydotprint_train.png",
                           var_with_name_simple=True)

# same thing but as text (not picture)
# pretty printing
theano.printing.pprint(prediction)

# debug printing
theano.printing.debugprint(prediction) # pre-compilation
theano.printing.debugprint(predict) # post-compilation